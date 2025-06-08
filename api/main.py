from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

# Load trained model
model = joblib.load("../model/energy_model_xgb.pkl")

# Create FastAPI app
app = FastAPI(
    title="Smart Energy Forecast API",
    description="Predicts energy consumption based on sensor input",
    version="1.0"
)

# Define input schema
class EnergyInput(BaseModel):
    temperature: float
    humidity: float
    occupancy: int   # 0 or 1
    hour: int        # 0 to 23
    dayofweek: int   # 0 (Monday) to 6 (Sunday)

# Define response schema
class EnergyPrediction(BaseModel):
    predicted_energy_kwh: float

@app.get("/")
def read_root():
    return {"message": "Welcome to Smart Energy Forecast API!"}

@app.post("/predict", response_model=EnergyPrediction)
def predict_energy(data: EnergyInput):
    """
    Predict energy consumption (kWh) based on input features.
    """
    features = np.array([[data.temperature, data.humidity, data.occupancy, data.hour, data.dayofweek]])
    prediction = model.predict(features)[0]
    return {"predicted_energy_kwh": round(float(prediction), 3)}
