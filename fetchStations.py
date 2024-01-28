#import necessary libs
from requests import get
import json
from pprint import pprint

print("start")


#return weather data based on weather API
def getWeather(apiKey, city):
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'imperial'  # You can change units to metric if you prefer C
    }

    #if no errors, return the data
    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        # Extract weather information
        main_weather = data['weather'][0]['main']
        return main_weather
    except Exception as e:
        print(f"Error: {e}")
        return None

def is_raining(weather):
    return weather.lower() == 'rain'

    
if __name__ == "__main__":
    # API key obtained from OpenWeatherMap.com
    api_key = '45263cd86f74a5ca24f3d8cf1290a62a'
    city = 'Los Angeles'
    weather = getWeather(api_key, city)

    if weather:
        if is_raining(weather):
            print("It is raining.")
        else:
            print("It is not raining.")
    else:
        print("Failed to fetch weather data.")
    
