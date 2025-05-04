from locust import HttpUser, task, between
import random, json

class FastApiUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def predict(self):
        payload = {
            "num_lab_procedures": random.randint(1,132),
            "num_medications": random.randint(1,81),
            "time_in_hospital": random.randint(1,14)
        }
        self.client.post("/predict", json=payload)