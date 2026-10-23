# LAB 1 - EXERCISE 1
# Study Open Meteo Free Weather API: https://open-meteo.com/ 
# Write a Python program for tomorrow's hourly weather forecast in Fisciano (SA)
# Use only standard requests, do not install custom client libraries
# Fisciano coordinates: Latitude: 40.77 – Longitude: 14.79

import requests

# WMO Weather Codes
wmo = {
	0: "Clear sky",
	1: "Mainly clear",
	2: "Partly cloudy",
	3: "Overcast",
	45: "Fog",
	48: "Depositing rime fog",
	51: "Light drizzle",
	53: "Moderate drizzle",
	55: "Dense drizzle",
	56: "Light freezing drizzle",
	57: "Dense freezing drizzle",
	61: "Slight rain",
	63: "Moderate rain",
	65: "Heavy rain",
	66: "Light freezing rain",
	67: "Heavy freezing rain",
	71: "Slight snowfall",
	73: "Moderate snowfall",
	75: "Heavy snowfall",
	77: "Snow grains",
	80: "Slight rain showers",
	81: "Moderate rain showers",
	82: "Violent rain showers",
	85: "Slight snow showers",
	86: "Heavy snow showers",
	95: "Thunderstorm",
	96: "Thunderstorm with slight hail",
	97: "Heavy thunderstorm",
	99: "Thunderstorm with heavy hail"
}

url = "https://api.open-meteo.com/v1/forecast"
params = {
  "latitude": 40.7717, 
  "longitude": 14.7945, 
  "timezone": "Europe/Rome",
  "forecast_days": 2,
  "hourly": ["weather_code", "temperature_2m"]
}

print("Requesting information...")
response = requests.get(url, params = params)
print("Status code:", response.status_code)

if response.status_code == 200:
  time = response.json()["hourly"]["time"]
  temperature = response.json()["hourly"]["temperature_2m"]
  condition = response.json()["hourly"]["weather_code"]

  print("\nWeather forecast for tomorrow {} in Fisciano:\n".format(time[24][:10]))
  print("Time   Temp.   Condition")
  for i in range(24, len(time)):
    print ("{}  {}°C  {}".format(time[i][11:], temperature[i], wmo[condition[i]]))