import mlflow, os
from config import MLFLOW_TRACKING_URI
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

def load_production_model(name:str):
    model_uri = f"models:/{name}/Production"
    return mlflow.pyfunc.load_model(model_uri), model_uri