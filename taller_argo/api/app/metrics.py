from prometheus_client import Counter, generate_latest

# Contador de ejemplo
request_counter = Counter('api_requests_total', 'Total de solicitudes API')

def generate_metrics():
    return generate_latest(request_counter)