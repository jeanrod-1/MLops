from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import os

app = FastAPI()

MODEL_DIR = "models"

class IrisData(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float
    model_name: str = "rf_model.joblib"

def load_model(model_name: str):
    model_path = os.path.join(MODEL_DIR, model_name)
    if os.path.exists(model_path):
        return joblib.load(model_path)  # Se carga en cada predicción
    return None

@app.get("/predict")
def predict(sepal_length: float, sepal_width: float, petal_length: float, petal_width: float, model_name: str = "rf_model.joblib"):
    model = load_model(model_name)
    if model is None:
        raise HTTPException(status_code=404, detail=f"Model '{model_name}' not found.")
    
    prediction = model.predict([[sepal_length, sepal_width, petal_length, petal_width]])
    return {"model": model_name, "prediction": int(prediction[0])}

@app.get("/list_models")
def list_models():
    models = [f for f in os.listdir(MODEL_DIR) if f.endswith(".joblib")]
    return {"available_models": models}
