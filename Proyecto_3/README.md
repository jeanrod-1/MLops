# Construir imagenes: 
sudo docker build -t jeanrod1/fastapi:latest -f api/Dockerfile .
sudo docker build -t jeanrod1/streamlit:latest ./ui

# Iniciar sesión en docker hub
sudo docker login

# Sube las imágenes
sudo docker push jeanrod1/fastapi:latest
sudo docker push jeanrod1/streamlit:latest


# Configurar kubectl
sudo usermod -a -G microk8s estudiante
newgrp microk8s

# Revisar los espacios
microk8s kubectl get all --all-namespaces

# Crear los namespaces
microk8s kubectl create namespace mlops

# Desplejar airflow
mkdir -p ./dags ./logs ./plugins
echo -e "AIRFLOW_UID=$(id -u)" > .env
mkdir -p ./models

sudo docker-compose -f docker-compose.airflow.yaml up airflow-init 
sudo docker-compose -f docker-compose.airflow.yaml up --build


sudo microk8s enable hostpath-storage


Despliegue en Kubernetes:
# 1. Namespace + secretos
<!-- kubectl apply -f k8s/00-namespace.yaml -->
sudo microk8s kubectl apply -f k8s/secrets.yaml && \
sudo microk8s kubectl apply -f k8s/postgres.yaml && \
sudo microk8s kubectl apply -f k8s/minio.yaml && \
sudo microk8s kubectl apply -f k8s/mlflow.yaml && \
sudo microk8s kubectl apply -f k8s/fastapi.yaml && \
sudo microk8s kubectl apply -f k8s/streamlit.yaml && \
sudo microk8s kubectl apply -f k8s/prometheus.yaml && \
sudo microk8s kubectl apply -f k8s/grafana.yaml && \
sudo microk8s kubectl apply -f k8s/locust.yaml  

