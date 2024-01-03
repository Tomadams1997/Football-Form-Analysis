import requests
import json


def callApi(key, league_codes, year):
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    headers = {
	"X-RapidAPI-Key": key,
	"X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }
    params = {
    "league": league_codes,  
    "season": year
    }
    
    season = requests.get(url, headers=headers, params=params)
    if season.status_code == 200:

        json_response = season.json()        

        file_path = f'/Users/tomadams/Documents/FootballAPI V2/Datasets/OriginalData/season_{league_codes}_{year}_results.json'  
        with open(file_path, 'w') as file:
            json.dump(json_response, file, indent=4)
        print(f"Updated JSON data saved to '{file_path}'")
    else:
        print("Failed to retrieve data. Status code:", season.status_code)
        
        