import requests
import json

#Define a unique user-agent
headers = {"User-Agent": "WeatherAppProject"}

#Lookup grid endpoints via lat/lon
point_url = "https://api.weather.gov/points/39.0997,-94.5786"
point_response = requests.get(point_url, headers = headers)

if point_response.status_code == 200:
    print("Success")
else:
    print(f"Point lookup failed: {point_response.status_code}")
    exit()

point_json = point_response.json()

#Extract the exact forecast endpoint and call it
forcast_url = point_json["properties"]["forecast"]
forcast_response = requests.get(forcast_url, headers = headers)

if forcast_response.status_code == 200:
    forecast_data = forcast_response.json()
    print("Forecast success")
else:
    print(f"Forecast Failed: {forcast_response.status_code}")

with open("data_raw//raw_data.json", "w") as f:
    json.dump(forecast_data, f, indent = 4)