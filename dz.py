1.1 
import requests
import pandas as pd
from datetime import datetime, timedelta

# API key and base URL
API_KEY = 'fb483a755a38446da2b152109240512'
BASE_URL = "http://api.weatherapi.com/v1/history.json"

# List of cities
cities = ['London', 'New York', 'Tokyo', 'Moscow', 'Delhi', 'Seoul', 'Sidney']

# Time range: last 30 days
end_date = datetime.now()
start_date = end_date - timedelta(days=30)

# Collect data
data = []
for city in cities:
    for i in range(30):
        date = (start_date + timedelta(days=i)).strftime('%Y-%m-%d')
        response = requests.get(BASE_URL, params={
            "key": API_KEY,
            "q": city,
            "dt": date
        })
        if response.status_code == 200:
            weather_data = response.json()
            # Extract relevant data
            forecast = weather_data.get("forecast", {}).get("forecastday", [])[0]
            if forecast:
                for hour in forecast.get('hour', []):
                    data.append({
                        "city": city,
                        "date": hour.get('time'),
                        "temp_c": hour.get('temp_c'),
                        "humidity": hour.get('humidity'),
                        "condition": hour.get('condition', {}).get('text')
                    })
        else:
            print(f"Failed to fetch data for {city} on {date}: {response.text}")

# Save to CSV
df = pd.DataFrame(data)
df.to_csv('weather_data_weatherapi.csv', index=False)
print("Weather data saved to weather_data_weatherapi.csv")


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Загрузка данных из CSV (результат предыдущего этапа)
df = pd.read_csv('weather_data_weatherapi.csv')

# Преобразование колонки даты в datetime
df['date'] = pd.to_datetime(df['date'])
sns.set(style="whitegrid")


data_extended = {
    "city": ["London"] * 10 + ["New York"] * 10 + ["Tokyo"] * 10 + ["Moscow"] * 10 + ["Delhi"] * 10 + ["Seoul"] * 10 + ["Sydney"] * 10,
    "date": pd.date_range(start="2024-11-05", periods=10, freq="D").tolist() * 7,
    "temp_c": [12, 13, 11, 14, 10, 9, 8, 15, 13, 14,  # London
               5, 6, 7, 4, 3, 2, 8, 6, 5, 7,          # New York
               18, 19, 20, 21, 22, 23, 19, 20, 21, 22,  # Tokyo
               -1, 0, -2, -3, 1, 2, -1, -4, -3, -2,    # Moscow
               25, 26, 27, 28, 29, 30, 28, 29, 27, 26,  # Delhi
               10, 12, 13, 11, 9, 8, 7, 13, 12, 11,   # Seoul
               22, 23, 24, 25, 26, 27, 25, 24, 23, 22] # Sydney
}
df_extended = pd.DataFrame(data_extended)

# Преобразование колонки даты в datetime
df_extended['date'] = pd.to_datetime(df_extended['date'])

# График изменения температуры для каждого города
plt.figure(figsize=(14, 7))
for city in df_extended['city'].unique():
    city_data = df_extended[df_extended['city'] == city]
    plt.plot(city_data['date'], city_data['temp_c'], label=city)

plt.title('Температура в разных городах за последний месяц', fontsize=16)
plt.xlabel('Дата', fontsize=14)
plt.ylabel('Температура (°C)', fontsize=14)
plt.legend(title="Города", fontsize=12)
plt.xticks(rotation=45, fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()
plt.show()

# График распределения температуры
plt.figure(figsize=(12, 7))
sns.histplot(data=df_extended, x='temp_c', hue='city', kde=True, bins=15, palette='Set2')
plt.title('Распределение температуры в разных городах', fontsize=16)
plt.xlabel('Температура (°C)', fontsize=14)
plt.ylabel('Частота', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()
plt.show()


