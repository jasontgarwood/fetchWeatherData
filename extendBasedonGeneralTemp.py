#import necessary libs
import requests
import RPi.GPIO as GPIO
import time

################# Init Servos ####################
servo1_pin = 17  
servo2_pin = 18  

# Set up GPIO mode and pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo1_pin, GPIO.OUT)
GPIO.setup(servo2_pin, GPIO.OUT)

# Create PWM instances for servos
servo1_pwm = GPIO.PWM(servo1_pin, 50)  # 50 Hz PWM frequency
servo2_pwm = GPIO.PWM(servo2_pin, 50)

# Start PWM
servo1_pwm.start(0)
servo2_pwm.start(0)

################# Helper Functions ####################
def rotate_servos():
    # Rotate servo 1 
    servo1_pwm.ChangeDutyCycle(7.5)  

    # Rotate servo 2
    servo2_pwm.ChangeDutyCycle(0) 
    servo2_pwm.ChangeDutyCycle(3)  

def return_to_nuetral():
   
    # Rotate Servo 1
    servo1_pwm.ChangeDutyCycle(0)  
    servo1_pwm.ChangeDutyCycle(3) 

    # Rotate servo 2
    servo2_pwm.ChangeDutyCycle(7.5)  

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
            return_to_nuetral() 
        elif temperature >= 50:  # Above 80 degrees
            print("It is warm.")
            rotate_servos()  
        else:
            print(f"The weather is {weather} and the temperature is {temperature} degrees.")
    else:
        print("Failed to fetch weather data.")