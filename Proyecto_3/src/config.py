import os

POSTGRES = {
    "user": "mlops",
    "password": "mlops",
    "db": "diabetes",
    "host":"127.0.0.1",  # Ip del host, local: 172.30.173.0
    "port": 5432, 
}

RAW_SCHEMA = "raw"
CLEAN_SCHEMA = "clean"

MLFLOW_TRACKING_URI = "http://mlflow:5000"
S3_BUCKET = "mlflow"