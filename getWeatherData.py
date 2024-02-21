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

################# Main Function ####################
if __name__ == "__main__":
    
    api_key = 'YOUR API KEY' #API key from OpenWeatherMap.com
    city = 'Los Angeles' #Update this with the city!!!
    weather, temperature = getWeather(api_key, city)

    if weather is not None and temperature is not None:
        if weather.lower() == 'rain':
            print("It is raining.")
            ##SQUIRT WATER
        elif temperature < 32:  # Below freezing
            print("It is cold.")
            # Extend servo
            pi.set_servo_pulsewidth(17, 2000)  # GPIO pin 17, 2000 us pulse width for clockwise rotation
            pi.set_servo_pulsewidth(18, 2000)  # GPIO pin 18, 2000 us pulse width for clockwise rotation
            time.sleep(0.5)
        elif temperature > 80:  # Above 80 degrees
            print("It is warm.")
            # Shrink servo
            pi.set_servo_pulsewidth(17, 1000)  # GPIO pin 17, 1000 us pulse width for counter-clockwise rotation
            pi.set_servo_pulsewidth(18, 1000)  # GPIO pin 18, 1000 us pulse width for counter-clockwise rotation
            time.sleep(0.5)
        else:
            print(f"The weather is {weather} and the temperature is {temperature} degrees.")
    else:
        print("Failed to fetch weather data.")

# Cleanup pigpio
pi.stop()