#import necessary libs
import requests
import RPi.GPIO as GPIO
import time

################# Init Servos ####################
servo1_pin = 17  # 
servo2_pin = 18  # 

# Set up the GPIO pins as output
GPIO.setup(servo1_pin, GPIO.OUT)
GPIO.setup(servo2_pin, GPIO.OUT)

# Create PWM objects for the servos and start them
servo1 = GPIO.PWM(servo1_pin, 50)  # 50 Hz frequency
servo2 = GPIO.PWM(servo2_pin, 50)  # 50 Hz frequency
servo1.start(0)
servo2.start(0)


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
    
    api_key = '2f04170956655be916577719726c9d24' #API key from OpenWeatherMap.com
    city = 'Los Angeles' #Update this with the city!!!
    weather, temperature = getWeather(api_key, city)

    if temperature is not None:
        if temperature < 50:  # Below 60 degrees
            print("It is cold.")
            ##Shrink SERVOa
        elif temperature >= 50:  # Above 80 degrees
            print("It is warm.")
            # Rotate servo 1 half turn counterclockwise
            servo1.ChangeDutyCycle(2.5)  
            time.sleep(1)  # Adjust sleep time according to servo speed
            servo1.ChangeDutyCycle(0)  
            
            # Rotate servo 2 half turn clockwise
            servo2.ChangeDutyCycle(7.5) 
            time.sleep(1)  # Adjust sleep time according to servo speed
            servo2.ChangeDutyCycle(0)  
        else:
            print(f"The weather is {weather} and the temperature is {temperature} degrees.")
    else:
        print("Failed to fetch weather data.")