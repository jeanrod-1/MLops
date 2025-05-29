from fastapi import FastAPI
from pydantic import BaseModel
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response
from utils.mlflow_registry import load_production_model
from mlflow.tracking import MlflowClient
from fastapi.responses import JSONResponse
import os
import base64

app = FastAPI(title="House Prices API")

model, model_uri = load_production_model("house_prices_model")

REQUEST_COUNT = Counter("req_count", "Total requests")
REQUEST_LAT = Histogram("req_latency_seconds", "Latency")

client = MlflowClient()

class HouseFeatures(BaseModel):
    bed: int
    bath: int
    acre_lot: float
    house_size: int

@app.on_event("startup")
def _startup():
    global model, model_uri

@app.get("/health")
def health():
    return {"status": "ok", "model": model_uri}

@app.post("/predict")
def predict(entry: HouseFeatures):
    REQUEST_COUNT.inc()
    with REQUEST_LAT.time():
        df = entry.model_dump()
        import pandas as pd
        X = pd.DataFrame([df])
        print(X)
        y = model.predict(X)[0]
    return {"predicted_price": float(y), "model": model_uri}

@app.get("/metrics")
def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/model-history")
def model_history():
    experiment = client.get_experiment_by_name("house-prices-v1")
    runs = client.search_runs(experiment.experiment_id, order_by=["start_time DESC"])
    result = []

    for run in runs:
        info = run.info
        data = run.data
        result.append({
            "run_id": info.run_id,
            "status": data.tags.get("production_status", "unknown"),
            "mae": data.metrics.get("mae"),
            "mse": data.metrics.get("mse"),
            "r2": data.metrics.get("r2"),
            "params": data.params,
            "rejection_reason": data.tags.get("rejection_reason"),
            "start_time": info.start_time
        })

    return result

@app.get("/current-model")
def get_current_model():
    client = MlflowClient()
    prod_model = client.get_latest_versions("house_prices_model", stages=["Production"])[0]
    return {
        "run_id": prod_model.run_id,
        "model_name": prod_model.name,
        "version": prod_model.version
    }

@app.get("/production-plot")
def get_production_plot():
    client = MlflowClient()
    model_name = "house_prices_model"
    
    # Buscar el modelo en producción
    latest_production = client.get_latest_versions(model_name, stages=["Production"])
    if not latest_production:
        return JSONResponse(status_code=404, content={"error": "No hay modelo en producción."})
    
    run_id = latest_production[0].run_id
    artifact_path = f"shap_summary.png"
    local_path = client.download_artifacts(run_id, artifact_path)

    # Leer imagen y codificar en base64
    with open(local_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    
    return {"run_id": run_id, "image_base64": encoded}