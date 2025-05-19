import requests
import time
import random

while True:
    data = {"features": [random.uniform(4.0, 8.0) for _ in range(4)]}
    try:
        requests.post("http://api-service/predict", json=data)
    except Exception as e:
        print(e)
    time.sleep(1)
