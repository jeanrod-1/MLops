# api/app/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response

# Inicializar la app
app = FastAPI()

# Cargar modelo
model = joblib.load("app/model.pkl")

# Métricas Prometheus
predict_counter = Counter("predict_requests_total", "Número total de peticiones a /predict")

# Clase para la entrada del modelo (ajústala con tus features reales)
class PatientData(BaseModel):
    race: str
    gender: str
    age: str
    time_in_hospital: int
    num_lab_procedures: int
    num_procedures: int
    num_medications: int
    number_outpatient: int
    number_emergency: int
    number_inpatient: int
    number_diagnoses: int
    max_glu_serum: str
    A1Cresult: str
    insulin: str
    change: str
    diabetesMed: str

@app.post("/predict")
def predict(data: PatientData):
    try:
        # Registrar métrica
        predict_counter.inc()

        # Convertir entrada a DataFrame
        input_df = pd.DataFrame([data.dict()])
        
        # Hacer predicción
        prediction = model.predict(input_df)

        return {"prediction": prediction[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)