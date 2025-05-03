## CAMBIAR!!

Construir imagenes en Kubernetes: 
# Suponiendo tu usuario de Docker Hub = myuser
<!-- sudo docker build -t myuser/airflow:latest   ./airflow -->
sudo docker build -t jeanrod1/fastapi:latest -f api/Dockerfile .
sudo docker build -t jeanrod1/streamlit:latest ./ui

# Iniciar sesión en docker hub
sudo docker login

# Sube las imágenes
<!-- sudo docker push myuser/airflow:latest -->
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

<!-- sudo microk8s kubectl port-forward svc/postgres 5432:5432 -n mlops -->

sudo docker-compose exec airflow-webserver airflow connections add postgres_mlops \
    --conn-type postgres \
    --conn-host 10.43.101.194 \
    --conn-port 30007 \
    --conn-login mlops \
    --conn-password mlops \
    --conn-schema diabetes

sudo microk8s enable hostpath-storage


Despliegue en Kubernetes:
# 1. Namespace + secretos
<!-- kubectl apply -f k8s/00-namespace.yaml -->
sudo microk8s kubectl apply -f k8s/secrets.yaml


# 2. Backing services
sudo microk8s kubectl apply -f k8s/postgres.yaml && \
sudo microk8s kubectl apply -f k8s/minio.yaml && \
sudo microk8s kubectl apply -f k8s/mlflow.yaml &&
<!-- microk8s kubectl apply -f k8s/airflow.yaml -->


# 3. Inferencia + UI
sudo microk8s kubectl apply -f k8s/fastapi.yaml
sudo microk8s kubectl apply -f k8s/streamlit.yaml

# 4. Observabilidad
sudo microk8s kubectl apply -f k8s/prometheus.yaml
sudo microk8s kubectl apply -f k8s/grafana.yaml


Pruebas de carga: kubectl apply -f k8s/10-locust.yaml    logs: kubectl -n mlops logs job/locust


Limpiar: 
docker compose down -v               # entorno local

kubectl delete namespace mlops       # Kubernetes


