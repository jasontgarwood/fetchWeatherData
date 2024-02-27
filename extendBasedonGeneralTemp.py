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
        temperature = data['main']['temp']
        return main_weather, temperature 
    
    except Exception as e:
        print(f"Error: {e}") #fancy way to print error messages
        return None

################# Main Function ####################
if __name__ == "__main__":
    
    api_key = 'YOUR API KEY' #API key from OpenWeatherMap.com
    city = 'Los Angeles' #Update this with the city!!!
    weather = getWeather(api_key, city)

    if temperature is not None:
        if temperature < 60:  # Below 60 degrees
            print("It is cold.")
            ##Shrink SERVO
        elif temperature > 80:  # Above 80 degrees
            print("It is warm.")
            ##Extend SERVO
        else:
            print(f"The weather is {weather} and the temperature is {temperature} degrees.")
    else:
        print("Failed to fetch weather data.")