from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI(title="API Penguins")

model = joblib.load('model.joblib')

class PenguinData(BaseModel):
    culmen_length_mm: float
    culmen_depth_mm: float
    body_mass_g: float

@app.post("/predict")
def predict(penguin: PenguinData):
    data = np.array([[penguin.culmen_length_mm, penguin.culmen_depth_mm, penguin.body_mass_g]])
    prediction = model.predict(data)
    return {"prediction": prediction[0]}

@app.get("/")
def read_root():
    return {"message": "API Penguins en funcionamiento"}