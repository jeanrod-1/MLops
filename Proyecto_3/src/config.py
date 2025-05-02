import os

POSTGRES = {
    "user": os.getenv("POSTGRES_USER", "mlops"),
    "password": os.getenv("POSTGRES_PASSWORD", "mlops"),
    "db": os.getenv("POSTGRES_DB", "diabetes"),
    "host": os.getenv("POSTGRES_HOST", "10.43.101.194"),  # Ip del host, local: 172.30.173.0
    "port": 30007, 
}

RAW_SCHEMA = "raw"
CLEAN_SCHEMA = "clean"

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_URI", "http://mlflow:5000")
S3_BUCKET = os.getenv("S3_BUCKET", "mlflow")