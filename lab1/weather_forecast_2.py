# LAB 1 - EXERCISE 2
# Study Open Meteo Free Weather API: https://open-meteo.com/ 
# Ask for a city name
# Ask to select a city from a list of matching locations
# Write the tomorrow's hourly weather forecast for the selected location
# Use the geocoding endpoint of Open Meteo

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

def searchLocation():
  url = "https://geocoding-api.open-meteo.com/v1/search"

  while True:
    location = input("Enter location name: ")
    params = {
      "name": location, 
      "language": "it", 
    }
    response = requests.get(url, params = params)

    if response.status_code == 200 and "results" in response.json():
      results = response.json()["results"]
      print("\nMatching locations:")
      for i, r in enumerate(results):
        print ("{}. {}, {} ({}), lat: {}, lon: {}".
              format(i, r["name"], r["country"], r.get("admin1"), r["latitude"], r["longitude"]))
      while True:
        try:
          index = int(input("Select location index: "))
          if index >= 0 and index < len(results): 
            return results[index]["name"], results[index]["latitude"], results[index]["longitude"]
        except: pass
    else:
      print("Location not found.")

def printForecast(name, latitude, longitude):
  url = "https://api.open-meteo.com/v1/forecast"
  params = {
    "latitude": latitude, 
    "longitude": longitude, 
    "timezone": "Europe/Rome",
    "forecast_days": 2,
    "hourly": ["weather_code", "temperature_2m"]
  }
  response = requests.get(url, params = params)

  if response.status_code == 200:
    time = response.json()["hourly"]["time"]
    temperature = response.json()["hourly"]["temperature_2m"]
    condition = response.json()["hourly"]["weather_code"]

    print("\nWeather forecast for tomorrow {} in {}:\n".format(time[24][:10], name))
    print("Time   Temp.   Condition")
    for i in range(24, len(time)):
      print ("{}  {}°C  {}".format(time[i][11:], temperature[i], wmo[condition[i]]))

name, latitude, longitude = searchLocation()
printForecast(name, latitude, longitude)