FROM python:3.10-slim
RUN pip install mlflow boto3 psycopg2-binary
CMD ["mlflow", "server", "--backend-store-uri", "postgresql://mlflow:mlflow@db/mlflow", "--default-artifact-root", "s3://mlflow/", "--host", "0.0.0.0", "--port", "5000"]