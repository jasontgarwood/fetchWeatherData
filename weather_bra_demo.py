import RPi.GPIO as GPIO
import time

################# init Servos ####################
# GPIO pins for the servos
servo1_pin = 18
servo2_pin = 17

# Set up GPIO
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


# Function to move servo to a specific angle
def move_servo(current_state_index):
    if current_state_index == 1:
    # Rotate servo 1 
        servo1_pwm.ChangeDutyCycle(11.5)  

        # Rotate servo 2
        servo2_pwm.ChangeDutyCycle(0) 
        servo2_pwm.ChangeDutyCycle(3)  

    else:
        # Rotate Servo 1
        servo1_pwm.ChangeDutyCycle(0)  
        servo1_pwm.ChangeDutyCycle(3) 

        # Rotate servo 2
        servo2_pwm.ChangeDutyCycle(11.5)  

        # Function to move servo to a specific angle

def move_servo_slow(current_state_index):
    if current_state_index == 1:
        # Rotate servo 1 
        
        slow_rotate(servo1_pwm, 11.5, 2)  

        # Rotate servo 2
        
        slow_rotate(servo2_pwm, 3, 2)  

    else:
        # Rotate Servo 1
        print("rotating to 3")
        servo1_pwm.ChangeDutyCycle(0)
        slow_rotate(servo1_pwm, 3, 3)
        

        # Rotate servo 2
        
        slow_rotate(servo2_pwm, 11.5, 2)


def slow_rotate(servo_pwm, target_duty_cycle, duration):
    current_duty_cycle = servo_pwm._last_cycle if hasattr(servo_pwm, '_last_cycle') else 0  
    steps = int(duration * 50)  # Calculate the number of steps based on duration
    duty_step = (target_duty_cycle - current_duty_cycle) / steps  # Calculate step size
    
    for _ in range(steps):
        current_duty_cycle += duty_step  
        servo_pwm.ChangeDutyCycle(current_duty_cycle)
        time.sleep(duration / steps)  
    servo_pwm.ChangeDutyCycle(target_duty_cycle)  
       

################# Main Functions ####################
def main():
    
    current_state_index = 0  # Index to keep track of current state

    try:
        while True:
            command = input("Press 'f' for normal movement or 's' for slow movement: ").strip().lower()
            if command == 'f':
                current_state_index = (current_state_index + 1) % 2
                move_servo(current_state_index)
                print("Servos toggled to state with fast movement:")
            elif command == 's':
                current_state_index = (current_state_index + 1) % 2
                move_servo_slow(current_state_index)
                print("Servos toggled to state with slow movement:")
            else:
                print("Invalid command. Please press 'f' or 's'.")

            

    except KeyboardInterrupt:
        pass

    finally:
        # Clean up GPIO
        servo1_pwm.stop()
        servo2_pwm.stop()
        GPIO.cleanup()

if __name__ == "__main__":
    main()
