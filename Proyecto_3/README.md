## CAMBIAR!!

Construir imagenes en Kubernetes: 
# Suponiendo tu usuario de Docker Hub = myuser
sudo docker build -t myuser/airflow:latest   ./airflow
sudo docker build -t myuser/fastapi:latest   ./api
sudo docker build -t myuser/streamlit:latest ./ui

# Iniciar sesión en docker hub
sudo docker login

# Sube las imágenes
sudo docker push myuser/airflow:latest
sudo docker push myuser/fastapi:latest
sudo docker push myuser/streamlit:latest


# Configurar kubectl
sudo usermod -a -G microk8s estudiante
newgrp microk8s

# Revisar los espacios
microk8s kubectl get all --all-namespaces

# Crear los namespaces
microk8s kubectl create namespace mlops



Despliegue en Kubernetes:
# 1. Namespace + secretos
<!-- kubectl apply -f k8s/00-namespace.yaml -->
microk8s kubectl apply -f k8s/secrets.yaml


# 2. Backing services
microk8s kubectl apply -f k8s/postgres.yaml && \
microk8s kubectl apply -f k8s/minio.yaml && \
microk8s kubectl apply -f k8s/mlflow.yaml && \
microk8s kubectl apply -f k8s/airflow.yaml


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


