from fastapi import FastAPI
import mlflow.pyfunc
import pandas as pd

app = FastAPI()

# Cargar el modelo desde MLflow
model_uri = "models:/RandomForestModel/Production"
model = mlflow.pyfunc.load_model(model_uri)

@app.post("/predict/")
def predict(data: dict):
    df = pd.DataFrame([data])
    prediction = model.predict(df)
    return {"prediction": prediction.tolist()}
