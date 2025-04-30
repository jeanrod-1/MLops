from fastapi import FastAPI
from pydantic import BaseModel
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from utils.mlflow_registry import load_production_model

app = FastAPI(title="Diabetes API")

model, model_uri = load_production_model("diabetes_rf")

REQUEST_COUNT = Counter("req_count", "Total requests")
REQUEST_LAT = Histogram("req_latency_seconds", "Latency")

class Patient(BaseModel):
    # ejemplo con 3 features numéricas y uno categórico
    num_lab_procedures:int
    num_medications:int
    time_in_hospital:int
    race:str = "Caucasian"

@app.on_event("startup")
def _startup():
    global model,model_uri

@app.get("/health")
def health():
    return {"status":"ok", "model":model_uri}

@app.post("/predict")
def predict(entry:Patient):
    REQUEST_COUNT.inc()
    with REQUEST_LAT.time():
        df = entry.model_dump()
        import pandas as pd
        X = pd.DataFrame([df])
        y = model.predict(X)[0]
    return {"readmit_<30": bool(y), "model":model_uri}

@app.get("/metrics")
def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)