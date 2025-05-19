✅ PRERREQUISITOS

Asegúrate de tener:

    ✅ Cuenta de GitHub y un repositorio creado

    ✅ Docker instalado y configurado (con acceso a Docker Hub o similar)

    ✅ Clúster de Kubernetes activo (puede ser minikube, kind o cloud como GKE/EKS/AKS)

    ✅ Argo CD instalado y configurado en el clúster

    ✅ kubectl, kustomize, argocd CLI y helm instalados localmente

    ✅ Repositorio Git enlazado a Argo CD como source

🚀 PASO A PASO

sudo microk8s kubectl create namespace argo

sudo microk8s kubectl apply -n argo -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

(sudo microk8s kubectl apply -n argo -f install.yaml)


3. Crear Imágenes Docker

API:

cd api
docker build -t jeanrod1/fastapi-api:latest .
docker push jeanrod1/fastapi-api:latest

LoadTester:

cd loadtester
docker build -t jeanrod1/loadtester:latest .
docker push jeanrod1/loadtester:latest

5. Probar localmente con kubectl (opcional)

sudo microk8s kubectl apply -n argo -k manifests/
sudo microk8s kubectl get pods -n argo
sudo microk8s kubectl port-forward svc/api-service 8000:80 -n argo



7. Configurar Argo CD
a. Crear el App en Argo CD (una vez)

sudo microk8s kubectl apply -n argo -f argo-cd/app.yaml


b. Argo CD se encargará de:

    Detectar cambios en Git

    Aplicar automáticamente los manifiestos

    Mantener el estado deseado en K8s

8. Visualizar la Arquitectura

    FastAPI: http://<CLUSTER_IP>:<8080>/predict 
    (10.152.183.224)
    Prometheus: http://<CLUSTER_IP>:9090
    (10.152.183.253)
    Grafana: http://<CLUSTER_IP>:3000 (usuario/pass por defecto: admin/admin)
    (10.152.183.61)
    Argo: http://<CLUSTER_IP>:80 (usuario/pass por defecto: admin/admin)
    (10.152.183.127)
    sudo microk8s kubectl -n argo get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo

9. Ver Métricas en Grafana

    Entrar a Grafana

    Data Source: Prometheus (ya configurado)

    Crear dashboards con métricas como:

        http_requests_total

        response_latency_seconds

🧠 BONUS: Flujo CI/CD Completo

graph LR
A[Commit en GitHub] --> B[GitHub Actions]
B --> C[Entrena modelo y sube imágenes]
C --> D[Actualiza manifiestos]
D --> E[Push a GitHub]
E --> F[Argo CD detecta cambio]
F --> G[Aplica en Kubernetes]
G --> H[API desplegada con métricas]