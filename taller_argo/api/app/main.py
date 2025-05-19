from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import numpy as np
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response

app = FastAPI()

with open("app/model.pkl", "rb") as f:
    model = pickle.load(f)

class InputData(BaseModel):
    features: list

prediction_counter = Counter("predictions_total", "Total predictions made")

@app.post("/predict")
def predict(data: InputData):
    prediction_counter.inc()
    prediction = model.predict([np.array(data.features)])
    return {"prediction": int(prediction[0])}


# Endpoint para exponer métricas de Prometheus
@app.get("/metrics")
def metrics():
    """
    Endpoint para exponer métricas de Prometheus
    """
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)