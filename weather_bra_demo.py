import RPi.GPIO as GPIO
import time
import keyboard  # Keyboard module for capturing key presses

# GPIO pins for the servos
servo1_pin = 18
servo2_pin = 17

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo1_pin, GPIO.OUT)
GPIO.setup(servo2_pin, GPIO.OUT)

# Create PWM instances for the servos
servo1_pwm = GPIO.PWM(servo1_pin, 50)  # 50 Hz frequency
servo2_pwm = GPIO.PWM(servo2_pin, 50)

# Function to move servo to a specific angle
def move_servo(pwm, angle, slow=False):
    duty_cycle = (angle / 18) + 2
    pwm.start(duty_cycle)
    if slow:
        time.sleep(0.5)  # Adjust this value for slower movement
    else:
        time.sleep(0.1)  # Default movement speed
    pwm.stop()

# Main function to control the servos
def main():
    servo_states = [0, 160]  # Neutral and Active states for the servos
    current_state_index = 0  # Index to keep track of current state

    try:
        while True:
            if keyboard.is_pressed('f'):
                current_state_index = (current_state_index + 1) % len(servo_states)
                move_servo(servo1_pwm, servo_states[current_state_index])
                move_servo(servo2_pwm, servo_states[current_state_index])
                print("Servos toggled to state:", current_state_index)

            elif keyboard.is_pressed('s'):
                current_state_index = (current_state_index + 1) % len(servo_states)
                move_servo(servo1_pwm, servo_states[current_state_index], slow=True)
                move_servo(servo2_pwm, servo_states[current_state_index], slow=True)
                print("Servos toggled to state with slow movement:", current_state_index)

    except KeyboardInterrupt:
        pass

    finally:
        # Clean up GPIO
        servo1_pwm.stop()
        servo2_pwm.stop()
        GPIO.cleanup()

if __name__ == "__main__":
    main()
