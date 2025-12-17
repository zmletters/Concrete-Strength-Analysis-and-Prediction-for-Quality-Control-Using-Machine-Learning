import requests
import pandas as pd
from datetime import datetime

# --- Configuration ---
LAT = 3.13   # Subang Jaya Latitude
LON = 101.55 # Subang Jaya Longitude
FILENAME = "subang_history_detailed_with_rain_flag.csv"

# Timeframe
end_date_str = "31/12/2024"
start_date_str = "01/04/2024"
end_date = datetime.strptime(end_date_str, "%d/%m/%Y")
start_date = datetime.strptime(start_date_str, "%d/%m/%Y")

# --- API Endpoint ---
url = "https://archive-api.open-meteo.com/v1/archive"

daily_params = [
    "temperature_2m_max",
    "temperature_2m_min",
    "temperature_2m_mean",
    "precipitation_sum",          # Total Rain (mm)
    "relative_humidity_2m_mean",
    "wind_speed_10m_max",
    "wind_direction_10m_dominant",
    "surface_pressure_mean"
]

params = {
    "latitude": LAT,
    "longitude": LON,
    "start_date": start_date.strftime("%Y-%m-%d"),
    "end_date": end_date.strftime("%Y-%m-%d"),
    "daily": ",".join(daily_params),
    "timezone": "Asia/Singapore"
}

print("Fetching data...")

try:
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    daily_data = data['daily']

    df = pd.DataFrame({
        'Date': daily_data['time'],
        'Max Temp (C)': daily_data['temperature_2m_max'],
        'Min Temp (C)': daily_data['temperature_2m_min'],
        'Mean Temp (C)': daily_data['temperature_2m_mean'],
        'Rainfall (mm)': daily_data['precipitation_sum'],
        'Mean Humidity (%)': daily_data['relative_humidity_2m_mean'],
        'Max Wind Speed (km/h)': daily_data['wind_speed_10m_max'],
        'Wind Direction (deg)': daily_data['wind_direction_10m_dominant'],
        'Pressure (hPa)': daily_data['surface_pressure_mean']
    })

    # --- NEW LOGIC ADDED HERE ---
    # Create a new column 'Rained?'.
    # If Rainfall > 0.1mm, it puts 'Yes', otherwise 'No'.
    df['Rained?'] = df['Rainfall (mm)'].apply(lambda x: 'Yes' if x > 0.1 else 'No')

    df.to_csv(FILENAME, index=False)
    print(f"✅ Success! Data saved to '{FILENAME}'")
    print(df[['Date', 'Rainfall (mm)', 'Rained?']].head()) # Preview specific columns

except requests.exceptions.RequestException as e:
    print(f"Error: {e}")