# MLOps Deployment Guide

Este documento explica paso a paso cómo construir imágenes, desplegar servicios usando Docker, Airflow y Kubernetes, y cómo monitorear todo el sistema.

---

## 1. Construcción y despliegue de imágenes Docker

### 1.1 Construir imágenes
```bash
sudo docker build -t jeanrod1/fastapi:latest -f api/Dockerfile .
sudo docker build -t jeanrod1/streamlit:latest ./ui
```

### 1.2 Iniciar sesión en Docker Hub
```bash
sudo docker login
```

### 1.3 Subir las imágenes a Docker Hub
```bash
sudo docker push jeanrod1/fastapi:latest
sudo docker push jeanrod1/streamlit:latest
```

---

## 2. Desplegar Apache Airflow

### 2.1 Preparar entorno de directorios
```bash
mkdir -p ./dags ./logs ./plugins
echo -e "AIRFLOW_UID=$(id -u)" > .env
mkdir -p ./models
```

### 2.2 Inicializar y levantar Airflow
```bash
sudo docker-compose -f docker-compose.airflow.yaml up airflow-init 
sudo docker-compose -f docker-compose.airflow.yaml up --build
```

### 2.3 Ir a la interfaz de Airflow
Navegar a: [http://localhost:8080](http://localhost:8080)  
Loguearse con:
- **Usuario**: `airflow`
- **Contraseña**: `airflow`

![Airflow UI](images/airflow-dag.jpeg)

### 2.4 Ejecutar los DAGs
Ejecutar en el siguiente orden:
```
ingest >> preprocess >> train >> select_best
```

---

## 3. Configurar Kubernetes (microk8s)

### 3.1 Agregar usuario al grupo microk8s
```bash
sudo usermod -a -G microk8s estudiante
newgrp microk8s
```

### 3.2 Habilitar almacenamiento
```bash
sudo microk8s enable hostpath-storage
```

### 3.3 Revisar todos los recursos desplegados
```bash
microk8s kubectl get all --all-namespaces
```

### 3.4 Crear namespace para MLOps
```bash
microk8s kubectl create namespace mlops
```

---

## 4. Despliegue de servicios en Kubernetes

> Hicimos NodePort para habilitar los servicios fuera del clúster de Kubernetes y que Airflow pueda acceder a ellos.

```bash
sudo microk8s kubectl apply -f k8s/secrets.yaml && 
sudo microk8s kubectl apply -f k8s/postgres.yaml && 
sudo microk8s kubectl apply -f k8s/minio.yaml && 
sudo microk8s kubectl apply -f k8s/mlflow.yaml && 
sudo microk8s kubectl apply -f k8s/fastapi.yaml && 
sudo microk8s kubectl apply -f k8s/streamlit.yaml && 
sudo microk8s kubectl apply -f k8s/prometheus.yaml && 
sudo microk8s kubectl apply -f k8s/grafana.yaml && 
sudo microk8s kubectl apply -f k8s/locust.yaml
```

---

## 5. Verificación de Servicios

### 5.1 Ir a MLflow y revisar los experimentos y modelos registrados  
[http://172.30.173.0:30008](http://172.30.173.0:30008)  
![MLflow](images/mlflow-experiments.jpeg)

### 5.2 Ir a la API y revisar que funcione correctamente  
[http://172.30.173.0:30012](http://172.30.173.0:30012)  
![API](images/api.jpeg)

### 5.3 Ir a la UI de Streamlit, revisar que funcione correctamente y probarla  
[http://172.30.173.0:30010](http://172.30.173.0:30010)  
![Streamlit UI](images/ui.jpeg)

### 5.4 Ir a la UI de Grafana, revisar que funcione correctamente y probarla  
[http://172.30.173.0:30013](http://172.30.173.0:30013)  
![Grafana UI](images/grafana.jpeg)

### 5.5 Agregar el datasource de Prometheus en Grafana  
[http://172.30.173.0:30013](http://172.30.173.0:30013)  
![Add Prometheus](images/add-prometheus-grafana.jpeg)

### 5.6 Revisar dashboards que proporciona Prometheus desde Grafana  
[http://172.30.173.0:30013](http://172.30.173.0:30013)  
![Prometheus Charts](images/prometheus-charts.jpeg)

---

## 6. Pruebas de carga con Locust y monitoreo en Grafana

### 6.1 Ir a la UI de Locust y hacer pruebas de usuarios  
[http://172.30.173.0:30015](http://172.30.173.0:30015)  
![Locust 10k](images/locust-10000users-500rate.jpeg)

- Con **10.000 usuarios** y un rate de **500**, **todo se cae**, es demasiado.

![Locust 5k](images/locust-5000users-500rate.jpeg)

- Con **5.000 usuarios** y un rate de **500**, **funciona bien**, se puede incrementar más.

![Locust 8k](images/locust-optimal-8000users-500rate.jpeg)

- Con **8.000 usuarios** y un rate de **500**, **funciona perfecto**, más de eso **no aguanta**, se caería.

---

## ✅ Conclusiones

- Todos los servicios fueron integrados exitosamente: Airflow, MLflow, API, UI, Monitoreo y Pruebas de carga.
- Se utilizó `NodePort` para facilitar la conexión entre Airflow y los servicios externos al cluster.
- El sistema soporta hasta **8,000 usuarios concurrentes** con buena estabilidad, ideal para pruebas en producción.
