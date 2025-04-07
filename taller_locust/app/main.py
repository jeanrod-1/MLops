from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import time
import joblib

app = FastAPI(title="API de Inferencia Simple", version="1.0")

# Cargar el modelo solo una vez al iniciar
model = joblib.load('models/rf_model.joblib')

# Modelo Pydantic para validar los datos de entrada
class InputData(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

# Modelo Pydantic para la respuesta
class PredictionResponse(BaseModel):
    message: str
    input_data: dict
    prediction_result: float

@app.get("/")
def read_root():
    return {"message": "API de Inferencia lista"}

@app.post("/predict", response_model=PredictionResponse)
def predict(data: InputData):
    try:
        input_features = [[
            data.sepal_length,
            data.sepal_width,
            data.petal_length,
            data.petal_width
        ]]
        prediction = model.predict(input_features)[0]

        # Simulación simple
        print(f"Recibiendo datos: {data.dict()}")
        time.sleep(0.05)

        return PredictionResponse(
            message="Predicción generada exitosamente",
            input_data=data.dict(),
            prediction_result=prediction
        )
    except Exception as e:
        print(f"Error durante la predicción: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {e}")
