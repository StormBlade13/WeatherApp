import requests
import json

#A client for pulling historical weather data from NCEI's Climate Data Online API.
class NCEIClient:

    #Base URL
    URL = "https://www.ncei.noaa.gov/cdo-web/api/v2/data"

    def __init__(self):
        self.headers = {
            "token": "eFFEGOrfOnyNMTTvkclvbTIFFqkKlIGR",
            "User-Agent": "WeatherAppProject"
            }
        
    #Fetch a block of data from NCEI
    def fetch(self, start_date: str, end_date: str):

        #API parameters
        parameters = {
            "datasetid": "GHCND",
            "stationid": "GHCND:USW00003947",
            "startdate": start_date,
            "enddate": end_date,
            "limit": 1000}

        #API response
        response = requests.get(self.URL, headers = self.headers, params = parameters)

        #API error check
        if response.status_code == 200:
            print("Success")
        else:
            print(f"station lookup failed: {response.status_code}")
            exit()

        #Converts response to json
        data = response.json()

        return data

    #Saves raw json data
    def save(self, data):

        #Writes json to raw_data file
        with open("data_raw//raw_data.json", "w") as f:
            json.dump(data, f, indent = 4)