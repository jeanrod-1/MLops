from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import time  

app = FastAPI(title="API de Inferencia Simple", version="1.0")

# Modelo Pydantic para validar los datos de entrada
class InputData(BaseModel):
    feature1: float
    feature2: float
    feature3: float

# Modelo Pydantic para la respuesta
class PredictionResponse(BaseModel):
    message: str
    input_data: dict
    prediction_result: float

@app.get("/")
def read_root():
    """Endpoint raíz para verificar que la API está funcionando."""
    return {"message": "API de Inferencia lista"}

@app.post("/predict", response_model=PredictionResponse)
def predict(data: InputData):
    """
    Endpoint para recibir datos y simular una predicción.
    """
    try:
        # --- Inicio: Lógica de Inferencia Real (Reemplazar con el modelo real) ---
        # Aquí cargarías tu modelo (ej. desde un archivo .pkl)
        # model = load_model('path/to/your/model.pkl')
        # prediction = model.predict([[data.feature1, data.feature2, data.feature3]])

        # Simulación simple:
        print(f"Recibiendo datos: {data.dict()}")
        dummy_result = data.feature1 + data.feature2 + data.feature3
        time.sleep(0.05) # Simula tiempo de procesamiento

        print(f"Resultado de predicción simulada: {dummy_result}")
        return PredictionResponse(
            message="Predicción generada exitosamente",
            input_data=data.dict(),
            prediction_result=dummy_result
        )
    except Exception as e:
        print(f"Error durante la predicción: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {e}")