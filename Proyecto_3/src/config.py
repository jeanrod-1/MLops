import os

# PostgreSQL config
POSTGRES = {
    "user": "mlops",
    "password": "mlops",
    "db": "diabetes",
    # "host":"10.43.101.194",  # Ip de la VM
    "host": "172.30.173.0",  # Ip local: 172.30.173.0
    "port": 30007,
}

# Esquemas de base de datos
RAW_SCHEMA = "raw"
CLEAN_SCHEMA = "clean"

# MLflow Tracking
MLFLOW_TRACKING_URI = "http://172.30.173.0:30008"
S3_BUCKET = "mlflow"

# MinIO / S3 Backend config (usado por MLflow para artefactos)
AWS_ACCESS_KEY_ID = "minioadmin"
AWS_SECRET_ACCESS_KEY = "minioadmin"
MLFLOW_S3_ENDPOINT_URL = "http://172.30.173.0:30001"

# Set env variables (useful if imported before calling mlflow)
os.environ["AWS_ACCESS_KEY_ID"] = AWS_ACCESS_KEY_ID
os.environ["AWS_SECRET_ACCESS_KEY"] = AWS_SECRET_ACCESS_KEY
os.environ["MLFLOW_S3_ENDPOINT_URL"] = MLFLOW_S3_ENDPOINT_URL
