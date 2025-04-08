from locust import HttpUser, task, between
import random

class APIUser(HttpUser):
    """
    Clase de usuario que simula interacciones con la API de inferencia.
    """
    wait_time = between(0.5, 2.0) 

    @task 
    def make_prediction(self):
        """
        Tarea que envía una petición POST al endpoint /predict con datos aleatorios.
        """
        
        payload = {
            "sepal_length": round(random.uniform(0.0, 10.0), 2),
            "sepal_width": round(random.uniform(0.0, 5.0), 2),
            "petal_length": round(random.uniform(0.0, 2.0), 2),
            "petal_width": round(random.uniform(0.0, 2.0), 2)
        }

        headers = {'Content-Type': 'application/json'}

        with self.client.post("/predict", json=payload, headers=headers, catch_response=True) as response:

            if response.status_code == 200:
                try:
                    json_response = response.json()
                    if "prediction_result" in json_response:
                        response.success()
                        # print(f"✅ Predicción OK: {json_response['prediction_result']}")
                    else:
                        response.failure(f"Respuesta JSON inválida: falta 'prediction_result'. Contenido: {response.text}")
                except ValueError:
                    response.failure(f"Respuesta no es JSON válido. Código: {response.status_code}, Contenido: {response.text}")
            else:
                response.failure(f"Código de estado inesperado: {response.status_code}. Contenido: {response.text}")