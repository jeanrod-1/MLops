# MLOps Deployment Guide

Este documento explica paso a paso cómo construir imágenes, desplegar servicios usando Docker, Airflow y Kubernetes, y cómo monitorear todo el sistema.

---

## 1. Construcción y despliegue de imágenes Docker

### 1.1 Construir imágenes
```bash
docker build -t diabetes-api .
docker run -p 8000:8000 diabetes-api
