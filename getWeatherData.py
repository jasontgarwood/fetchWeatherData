#import necessary libs
import requests

################# Helper Functions ####################
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
        response = requests.get(url, params=params)
        data = response.json()

        #Extract weather information
        main_weather = data['weather'][0]['main']
        return main_weather
    
    except Exception as e:
        print(f"Error: {e}") #fancy way to print error messages
        return None
    

################# Main Function ####################
if __name__ == "__main__":
    
    api_key = '45263cd86f74a5ca24f3d8cf1290a62a' #API key from OpenWeatherMap.com
    city = 'Los Angeles' #Update this with the city!!!
    weather = getWeather(api_key, city)

    if weather:
        if weather.lower() == 'rain':
            print("It is raining.")
        else:
            print(weather)
            print("It is not raining")
    else:
        print("Failed to fetch weather data.")