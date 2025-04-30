## CAMBIAR!!


Ejecucion local: docker compose up --build


Construir imagenes en Kubernetes: 
# Suponiendo tu usuario de Docker Hub = myuser
docker build -t myuser/airflow:latest   ./airflow
docker build -t myuser/fastapi:latest   ./api
docker build -t myuser/streamlit:latest ./ui

# Sube las imágenes
docker push myuser/airflow:latest
docker push myuser/fastapi:latest
docker push myuser/streamlit:latest


Despliegue en Kubernetes:
# 1. Namespace + secretos
kubectl apply -f k8s/00-namespace.yaml
kubectl apply -f k8s/01-secrets.yaml

# 2. Backing services
kubectl apply -f k8s/02-postgres.yaml
kubectl apply -f k8s/03-minio.yaml
kubectl apply -f k8s/04-mlflow.yaml
kubectl apply -f k8s/05-airflow.yaml

# 3. Inferencia + UI
kubectl apply -f k8s/06-fastapi.yaml
kubectl apply -f k8s/07-streamlit.yaml

# 4. Observabilidad
kubectl apply -f k8s/08-prometheus.yaml
kubectl apply -f k8s/09-grafana.yaml


Pruebas de carga: kubectl apply -f k8s/10-locust.yaml    logs: kubectl -n mlops logs job/locust


Limpiar: 
docker compose down -v               # entorno local

kubectl delete namespace mlops       # Kubernetes


