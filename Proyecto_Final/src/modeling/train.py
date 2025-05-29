import pandas as pd
import sqlalchemy as sa
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from config import POSTGRES, CLEAN_SCHEMA, MLFLOW_TRACKING_URI, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, MLFLOW_S3_ENDPOINT_URL
from mlflow.tracking import MlflowClient
from minio import Minio
import shap
import matplotlib.pyplot as plt
import os

def setup_minio_bucket(minio_host: str, minio_port: int, access_key: str, secret_key: str, bucket_name: str):
    client = Minio(
        f"{minio_host}:{minio_port}",
        access_key=access_key,
        secret_key=secret_key,
        secure=False
    )
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)
        print(f"Bucket '{bucket_name}' creado exitosamente.")
    else:
        print(f"El bucket '{bucket_name}' ya existe.")

def setup_experiment(experiment_name: str, artifact_location: str = "s3://mlflow/"):
    setup_minio_bucket("172.30.173.0", "30001", AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, "mlflow")
    client = MlflowClient()
    experiment = client.get_experiment_by_name(experiment_name)
    if experiment is None:
        print(f"⚙️  Creando nuevo experimento: {experiment_name}")
        experiment_id = client.create_experiment(name=experiment_name, artifact_location=artifact_location)
    else:
        if experiment.lifecycle_stage == "deleted":
            print(f"⚠️  Restaurando experimento eliminado: {experiment_name}")
            client.restore_experiment(experiment.experiment_id)
        experiment_id = experiment.experiment_id
        print(f"✅ Usando experimento existente: {experiment_name} (ID: {experiment_id})")

    mlflow.set_experiment(experiment_name)
    return experiment_id

def _engine():
    p = POSTGRES
    return sa.create_engine(
        f"postgresql://{p['user']}:{p['password']}@{p['host']}:{p['port']}/{p['db']}"
    )

def get_best_mae(client, experiment_id):
    runs = client.search_runs(experiment_ids=[experiment_id], order_by=["metrics.mae ASC"])
    for run in runs:
        if "mae" in run.data.metrics:
            return run.data.metrics["mae"]
    return None  # No hay ningún modelo con MAE

def main():
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

    experiment_name = "house-prices-v1"
    experiment_id = setup_experiment(experiment_name)

    X = pd.read_sql_table("features", _engine(), schema=CLEAN_SCHEMA)
    y = pd.read_sql_table("labels", _engine(), schema=CLEAN_SCHEMA)["target"]

    print(X.head(2))
    print(y.head(2))

    train_frac = 0.8
    split = int(len(X) * train_frac)
    X_train, X_val = X.iloc[:split], X.iloc[split:]
    y_train, y_val = y.iloc[:split], y.iloc[split:]



    with mlflow.start_run():
        params = dict(n_estimators=200, max_depth=8, random_state=42)
        model = RandomForestRegressor(**params)
        model.fit(X_train, y_train)
        preds = model.predict(X_val)

        mse = mean_squared_error(y_val, preds)
        mae = mean_absolute_error(y_val, preds)
        r2 = r2_score(y_val, preds)

        mlflow.log_params(params)
        mlflow.log_metric("mse", mse)
        mlflow.log_metric("mae", mae)
        mlflow.log_metric("r2", r2)
        mlflow.sklearn.log_model(model, "model", registered_model_name="house_prices_model")

        print(f"MSE={mse:.3f}, MAE={mae:.3f}, R2={r2:.3f}")

        explainer = shap.Explainer(model)
        shap_values = explainer(X_val)
        shap.summary_plot(shap_values, X_val, show=False)
        os.makedirs("plots", exist_ok=True)
        plt.savefig("plots/shap_summary.png", bbox_inches="tight")
        mlflow.log_artifact("plots/shap_summary.png")

        run_id = "799f996bf30540178694cd99b2d771fc"
        # Establecer una etiqueta
        mlflow.set_tag(run_id, "production_status", "first_model")

        # Evaluación por MAE
        client = MlflowClient()
        best_mae = get_best_mae(client, experiment_id)
        model_name = "house_prices_model"
        run_id = mlflow.active_run().info.run_id
        runs = client.search_runs(experiment_ids=[experiment_id], order_by=["metrics.mae ASC"])
        print(f'Lenght of runs {len(runs)}')

        if len(runs) == 1:
            mlflow.set_tag("production_status", "first_model")
            print("Primer modelo entrenado, considerado candidato para producción.")

            # Promover directamente
            model_versions = client.search_model_versions(f"name='{model_name}'")
            matching_version = next(mv.version for mv in model_versions if mv.run_id == run_id)

            # Archivar otros modelos en producción
            for mv in model_versions:
                if mv.current_stage == "Production":
                    client.transition_model_version_stage(model_name, mv.version, "Archived")

            client.transition_model_version_stage(model_name, matching_version, "Production", archive_existing_versions=False)

        elif mae < best_mae:
            mlflow.set_tag("production_status", "candidate")
            print(f"Nuevo modelo con mejor MAE ({mae:.3f} < {best_mae:.3f}) → Candidato a producción.")

            model_versions = client.search_model_versions(f"name='{model_name}'")
            matching_version = next(mv.version for mv in model_versions if mv.run_id == run_id)

            for mv in model_versions:
                if mv.current_stage == "Production":
                    client.transition_model_version_stage(model_name, mv.version, "Archived")

            client.transition_model_version_stage(model_name, matching_version, "Production", archive_existing_versions=False)
            client.set_tag(run_id, "production_status", "promoted_to_production_better_mae")
        else:
            mlflow.set_tag("production_status", "rejected")
            mlflow.set_tag("rejection_reason", f"mae {mae:.3f} >= best mae {best_mae:.3f}")
            print(f"Modelo rechazado por mayor MAE ({mae:.3f} >= {best_mae:.3f})")

if __name__ == "__main__":
    main()
