# C:\Users\Ze Ming\Documents\PythonEnv\cp2\Scripts\activate.bat

import requests
import csv
import pandas as pd
from datetime import datetime, timedelta

# Subang Jaya Coordinates
LAT = 3.13
LON = 101.55

# Define dates: From 1 year ago to Yesterday
end_date = datetime.now() - timedelta(days=1)
start_date = end_date - timedelta(days=365)

url = "https://archive-api.open-meteo.com/v1/archive"

params = {
    "latitude": LAT,
    "longitude": LON,
    "start_date": start_date.strftime("%Y-%m-%d"),
    "end_date": end_date.strftime("%Y-%m-%d"),
    "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum"],
    "timezone": "Asia/Singapore"
}

print("Fetching historical data...")
response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    
    # The API returns 'daily' as a dictionary of lists (column-oriented)
    daily_data = data['daily']
    
    # Convert to DataFrame for easy CSV saving
    df = pd.DataFrame({
        'date': daily_data['time'],
        'max_temp_c': daily_data['temperature_2m_max'],
        'min_temp_c': daily_data['temperature_2m_min'],
        'rainfall_mm': daily_data['precipitation_sum']
    })
    
    filename = "subang_historical_observations_1year.csv"
    df.to_csv(filename, index=False)
    print(f"✅ Success! Data saved to {filename}")
    print(df.head())
else:
    print("Error fetching data:", response.text)