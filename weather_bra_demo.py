################# import Libs ####################
import RPi.GPIO as GPIO
import time
import threading

################# Init Servos ####################
servo1_pin = 17 #
servo2_pin = 18 #

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo1_pin, GPIO.OUT)
GPIO.setup(servo2_pin, GPIO.OUT)

# Setup and start PWM
servo1_pwm = GPIO.PWM(servo1_pin, 50)  # 50 Hz frequency
servo2_pwm = GPIO.PWM(servo2_pin, 50)
servo1_pwm.start(0)
servo2_pwm.start(0)

# Initial servo angles
servo1_angle = 0
servo2_angle = 0

################# Helper Functions ####################
# Function to set servo angle
def set_angle(pwm, angle):
    duty = angle / 18 + 2
    GPIO.output(pwm, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(pwm, False)
    pwm.ChangeDutyCycle(0)

# Function to toggle servo state
def toggle_servo(servo_pwm, servo_angle, active_angle, is_slow=False):
    global servo1_pwm, servo2_pwm, servo1_angle, servo2_angle
    if servo_angle == 0:
        if is_slow:
            for angle in range(0, active_angle + 1, 10):
                set_angle(servo_pwm, angle)
                time.sleep(0.1)
        else:
            set_angle(servo_pwm, active_angle)
        servo_angle = active_angle
    else:
        if is_slow:
            for angle in range(active_angle, 0, -10):
                set_angle(servo_pwm, angle)
                time.sleep(0.1)
        else:
            set_angle(servo_pwm, 0)
        servo_angle = 0
    return servo_angle

# Function to handle Enter key press
def on_enter_press():
    global servo1_pwm, servo1_angle, servo2_pwm, servo2_angle
    servo1_angle = toggle_servo(servo1_pwm, servo1_angle, 160)
    servo2_angle = toggle_servo(servo2_pwm, servo2_angle, 160)

# Function to handle Space key press
def on_space_press():
    global servo1_pwm, servo1_angle, servo2_pwm, servo2_angle
    servo1_angle = toggle_servo(servo1_pwm, servo1_angle, 160, is_slow=True)
    servo2_angle = toggle_servo(servo2_pwm, servo2_angle, 160, is_slow=True)

# Keyboard input thread
def key_input_thread():
    while True:
        key = input()
        if key == '':
            on_enter_press()
        elif key == ' ':
            on_space_press()

# Start keyboard input thread
input_thread = threading.Thread(target=key_input_thread)
input_thread.daemon = True
input_thread.start()

try:
    while True:
        # Keep the main thread running
        time.sleep(1)

except KeyboardInterrupt:
    servo1_pwm.stop()
    servo2_pwm.stop()
    GPIO.cleanup()
