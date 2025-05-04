import pandas as pd
import sqlalchemy as sa
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score
from config import POSTGRES, CLEAN_SCHEMA, MLFLOW_TRACKING_URI, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, MLFLOW_S3_ENDPOINT_URL
from mlflow.tracking import MlflowClient
from minio import Minio
from minio.error import S3Error

# Función para configurar el cliente de MinIO y crear el bucket si no existe
def setup_minio_bucket(minio_host: str, minio_port: int, access_key: str, secret_key: str, bucket_name: str):
    # Configura el cliente de MinIO
    client = Minio(
        f"{minio_host}:{minio_port}",
        access_key=access_key,
        secret_key=secret_key,
        secure=False  # Usa True si usas HTTPS
    )

    # Verifica si el bucket existe, y si no, lo crea
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)
        print(f"Bucket '{bucket_name}' creado exitosamente.")
    else:
        print(f"El bucket '{bucket_name}' ya existe.")

def setup_experiment(experiment_name: str, artifact_location: str = "s3://mlflow/"):
    # Si estás usando MinIO para los artefactos, crea el bucket antes de configurar el experimento
    setup_minio_bucket("172.30.173.0", "30001", AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, "mlflow")

    client = MlflowClient()
    experiment = client.get_experiment_by_name(experiment_name)

    if experiment is None:
        print(f"⚙️  Creando nuevo experimento: {experiment_name}")
        experiment_id = client.create_experiment(name=experiment_name, artifact_location=artifact_location)
    else:
        if experiment.lifecycle_stage == "deleted":
            print(f"⚠️  El experimento '{experiment_name}' estaba marcado como 'deleted'. Restaurando...")
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

def main():
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    
    experiment_name = "diabetes-readmit-v2"
    setup_experiment(experiment_name)           

    X = pd.read_sql_table("features", _engine(), schema=CLEAN_SCHEMA)
    y = pd.read_sql_table("labels", _engine(), schema=CLEAN_SCHEMA)["target"]
    X = X[['num_lab_procedures',
            'num_medications',
            'time_in_hospital']]
    
    print(X.head(2))
    print(y.head(2))


    train_frac = 0.8
    split = int(len(X) * train_frac)
    X_train, X_val = X.iloc[:split], X.iloc[split:]
    y_train, y_val = y.iloc[:split], y.iloc[split:]

    with mlflow.start_run():
        params = dict(n_estimators=200, max_depth=8, random_state=42)
        model = RandomForestClassifier(**params)
        model.fit(X_train, y_train)
        preds = model.predict(X_val)
        f1 = f1_score(y_val, preds)

        mlflow.log_params(params)
        mlflow.log_metric("f1", f1)
        mlflow.sklearn.log_model(model, "model", registered_model_name="diabetes_rf")

        print(f"F1={f1:.3f}")

if __name__ == "__main__":
    main()