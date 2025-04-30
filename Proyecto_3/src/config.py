import os

POSTGRES = {
    "user": os.getenv("POSTGRES_USER", "mlops"),
    "password": os.getenv("POSTGRES_PASSWORD", "mlops"),
    "db": os.getenv("POSTGRES_DB", "diabetes"),
    "host": os.getenv("POSTGRES_HOST", "postgres"),
    "port": 5432,
}

RAW_SCHEMA = "raw"
CLEAN_SCHEMA = "clean"

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_URI", "http://mlflow:5000")
S3_BUCKET = os.getenv("S3_BUCKET", "mlflow")