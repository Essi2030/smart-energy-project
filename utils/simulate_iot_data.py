import pandas as pd
import numpy as np

def generate_smart_energy_data(start_date="2024-01-01", days=30, seed=42):
    """
    Generate simulated IoT sensor data for a smart building.

    Parameters:
        start_date (str): Starting date for the data.
        days (int): Number of days to simulate (hourly resolution).
        seed (int): Random seed for reproducibility.

    Returns:
        pd.DataFrame: Simulated sensor data.
    """
    np.random.seed(seed)

    # Create hourly timestamps for the given number of days
    timestamps = pd.date_range(start=start_date, periods=24 * days, freq='H')

    # Simulate temperature (°C) and humidity (%)
    temperature = np.random.normal(loc=25, scale=5, size=len(timestamps))
    humidity = np.random.normal(loc=50, scale=10, size=len(timestamps))

    # Simulate occupancy: 0 = unoccupied, 1 = occupied
    occupancy = np.random.choice([0, 1], size=len(timestamps), p=[0.3, 0.7])

    # Simulate energy consumption based on time, occupancy and temperature
    hour_of_day = timestamps.hour
    base_consumption = 0.5 + 0.05 * hour_of_day
    occupancy_factor = 1 + 0.5 * occupancy
    temp_factor = 1 + 0.02 * (temperature - 25)

    energy_consumption = base_consumption * occupancy_factor * temp_factor
    energy_consumption = np.round(energy_consumption, 2)

    # Combine all into a DataFrame
    df = pd.DataFrame({
        "timestamp": timestamps,
        "temperature": temperature,
        "humidity": humidity,
        "occupancy": occupancy,
        "energy_consumption": energy_consumption
    })

    return df

if __name__ == "__main__":
    df = generate_smart_energy_data()
    output_path = "../data/sensor_data.csv"
    df.to_csv(output_path, index=False)
    print(f"✅ Simulated IoT data saved to '{output_path}'")
