import pandas as pd, sqlalchemy as sa, mlflow, mlflow.sklearn, os
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score
from config import POSTGRES, CLEAN_SCHEMA, MLFLOW_TRACKING_URI

def _engine():
    p = POSTGRES
    return sa.create_engine(
        f"postgresql://{p['user']}:{p['password']}@{p['host']}:{p['port']}/{p['db']}"
    )

def main():
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment("diabetes-readmit")

    X = pd.read_sql_table("features", _engine(), schema=CLEAN_SCHEMA)
    y = pd.read_sql_table("labels", _engine(), schema=CLEAN_SCHEMA)["target"]

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