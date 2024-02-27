#import necessary libs
import requests
import time
import pigpio

# Initialize pigpio
pi = pigpio.pi()

################# Helper Functions ####################
#return weather data based on weather API
def getWeather(apiKey, city):
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': apiKey,
        'units': 'imperial'  # You can change units to metric if you prefer Celsius
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
        return None, None

# Function to map temperature to extension length
def map_temperature_to_extension(temperature):
    # Assuming and extension ranges from 1000 to 2000 (adjust as needed)
    return ((temperature + 20) / 140) * (2000 - 1000) + 1000

# Function to extend linear actuators based on temperature
def extend_linear_actuators(temperature):
    extension_length = map_temperature_to_extension(temperature)
    pi.set_servo_pulsewidth(17, extension_length)  # GPIO pin 17, set extension length
    pi.set_servo_pulsewidth(18, extension_length)  # GPIO pin 18, set extension length

################# Main Function ####################
if __name__ == "__main__":
    
    api_key = 'YOUR API KEY' #API key from OpenWeatherMap.com
    city = 'Los Angeles' #Update this with the city!!!
    weather, temperature = getWeather(api_key, city)

    if temperature is not None:
        extend_linear_actuators(temperature)
        print(f"The weather is {weather} and the temperature is {temperature} degrees.")
    else:
        print("Failed to fetch weather data.")

# Cleanup pigpio
pi.stop()
