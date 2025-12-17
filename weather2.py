import requests
import pandas as pd
from datetime import datetime, timedelta

# --- Configuration ---
LAT = 3.13   # Subang Jaya Latitude
LON = 101.55 # Subang Jaya Longitude
FILENAME = "subang_history_detailed2.csv"

# Timeframe: Yesterday back to 1 year ago
end_date = datetime.now() - timedelta(days=1)
start_date = end_date - timedelta(days=365)

end_date_str = "31/12/2024"
start_date_str = "01/04/2024"
end_date = datetime.strptime(end_date_str, "%d/%m/%Y")
start_date = datetime.strptime(start_date_str, "%d/%m/%Y")

# --- API Endpoint ---
url = "https://archive-api.open-meteo.com/v1/archive"

# Define all the specific data points we want
daily_params = [
    "temperature_2m_max",           # Max Temp (°C)
    "temperature_2m_min",           # Min Temp (°C)
    "temperature_2m_mean",          # Mean Temp (°C)
    "precipitation_sum",            # Total Rain (mm)
    "rain_sum",                     # Rain specifically (excluding snow/hail)
    "relative_humidity_2m_mean",    # Average Humidity (%)
    "relative_humidity_2m_max",     # Max Humidity (%)
    "relative_humidity_2m_min",     # Min Humidity (%)
    "wind_speed_10m_max",           # Peak Wind Speed (km/h)
    "wind_direction_10m_dominant",  # Dominant Wind Direction (Degrees)
    "surface_pressure_mean"         # Atmospheric Pressure (hPa)
]

params = {
    "latitude": LAT,
    "longitude": LON,
    "start_date": start_date.strftime("%Y-%m-%d"),
    "end_date": end_date.strftime("%Y-%m-%d"),
    "daily": ",".join(daily_params), # Join list into comma-separated string
    "timezone": "Asia/Singapore"     # Matches Malaysia Time
}

print("Fetching detailed historical data...")

try:
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    # The 'daily' key contains the lists of data
    daily_data = data['daily']

    # Create a DataFrame
    # We map the API parameter names to friendlier Column Headers
    df = pd.DataFrame({
        'Date': daily_data['time'],
        'Max Temp (C)': daily_data['temperature_2m_max'],
        'Min Temp (C)': daily_data['temperature_2m_min'],
        'Mean Temp (C)': daily_data['temperature_2m_mean'],
        'Rainfall (mm)': daily_data['precipitation_sum'],
        'Mean Humidity (%)': daily_data['relative_humidity_2m_mean'],
        'Max Humidity (%)': daily_data['relative_humidity_2m_max'],
        'Min Humidity (%)': daily_data['relative_humidity_2m_min'],
        'Max Wind Speed (km/h)': daily_data['wind_speed_10m_max'],
        'Wind Direction (deg)': daily_data['wind_direction_10m_dominant'],
        'Pressure (hPa)': daily_data['surface_pressure_mean']
    })

    # LOGIC: If Rainfall is greater than 0.1mm, mark as 'Yes', otherwise 'No'
    # We use 0.1 instead of 0.0 to avoid 'trace' amounts or sensor noise.
    df['Rained'] = df['Rainfall (mm)'].apply(lambda x: 'Yes' if x > 10 else 'No')

    # Save to CSV
    df.to_csv(FILENAME, index=False)
    print(f"✅ Success! Detailed data saved to '{FILENAME}'")
    print("-" * 30)
    print(df.head()) # Show first 5 rows

except requests.exceptions.RequestException as e:
    print(f"Error fetching data: {e}")