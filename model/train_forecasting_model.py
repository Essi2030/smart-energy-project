import pandas as pd
import xgboost as xgb
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
import os

def add_time_features(df):
    """
    Extracts time-related features from the timestamp column.
    """
    df["hour"] = pd.to_datetime(df["timestamp"]).dt.hour
    df["dayofweek"] = pd.to_datetime(df["timestamp"]).dt.dayofweek
    return df

def train_model(data_path, model_output_path):
    """
    Train an XGBoost model to forecast energy consumption.
    """
    # Load data
    df = pd.read_csv(data_path)
    df = add_time_features(df)

    # Features and target
    features = ["temperature", "humidity", "occupancy", "hour", "dayofweek"]
    target = "energy_consumption"

    X = df[features]
    y = df[target]

    # Split into train and test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Train XGBoost Regressor
    model = xgb.XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=4)
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = mean_squared_error(y_test, y_pred) ** 0.5


    print(f"✅ Model trained!")
    print(f"📊 MAE:  {mae:.3f}")
    print(f"📊 RMSE: {rmse:.3f}")

    # Save model
    joblib.dump(model, model_output_path)
    print(f"💾 Model saved to: {model_output_path}")

if __name__ == "__main__":
    data_file = "../data/sensor_data.csv"
    model_file = "energy_model_xgb.pkl"
    train_model(data_file, model_file)
