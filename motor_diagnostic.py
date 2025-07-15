import RPi.GPIO as GPIO
import time

# GPIO Pin Configuration (same as robot_controller.py)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# RIGHT Motor Pins
ENA_PIN = 18
IN1_PIN = 27
IN2_PIN = 22

# LEFT Motor Pins
ENB_PIN = 23
IN3_PIN = 24
IN4_PIN = 25

# Global PWM objects
right_pwm = None
left_pwm = None

# --- Setup and Cleanup Functions ---
def setup_gpio():
    """Sets up GPIO pins for motor control."""
    global right_pwm, left_pwm
    GPIO.setup([ENA_PIN, IN1_PIN, IN2_PIN, ENB_PIN, IN3_PIN, IN4_PIN], GPIO.OUT)
    GPIO.output([IN1_PIN, IN2_PIN, IN3_PIN, IN4_PIN], GPIO.LOW)
    right_pwm = GPIO.PWM(ENA_PIN, 100)
    left_pwm = GPIO.PWM(ENB_PIN, 100)
    right_pwm.start(0)
    left_pwm.start(0)
    print("GPIO setup complete.")

def cleanup_gpio():
    """Stops PWM and cleans up GPIO channels."""
    print("\nCleaning up GPIO...")
    if right_pwm:
        right_pwm.stop()
    if left_pwm:
        left_pwm.stop()
    GPIO.cleanup()
    print("GPIO cleanup complete.")

# --- Individual Motor Control Functions (copied from robot_controller.py) ---
# These are the functions we are testing.

def right_motor_forward(duty_cycle):
    GPIO.output(IN1_PIN, GPIO.HIGH)
    GPIO.output(IN2_PIN, GPIO.LOW)
    right_pwm.ChangeDutyCycle(duty_cycle)

def right_motor_backward(duty_cycle):
    GPIO.output(IN1_PIN, GPIO.LOW)
    GPIO.output(IN2_PIN, GPIO.HIGH)
    right_pwm.ChangeDutyCycle(duty_cycle)

def left_motor_forward(duty_cycle):
    # This function was intended to make the left motor go physically forward
    # by using the "backward" L298N logic. We are testing this assumption.
    GPIO.output(IN3_PIN, GPIO.LOW)
    GPIO.output(IN4_PIN, GPIO.HIGH)
    left_pwm.ChangeDutyCycle(duty_cycle)

def left_motor_backward(duty_cycle):
    # This function was intended to make the left motor go physically backward
    # by using the "forward" L298N logic. We are testing this assumption.
    GPIO.output(IN3_PIN, GPIO.HIGH)
    GPIO.output(IN4_PIN, GPIO.LOW)
    left_pwm.ChangeDutyCycle(duty_cycle)

def stop_all_motors():
    right_pwm.ChangeDutyCycle(0)
    left_pwm.ChangeDutyCycle(0)

# --- Main Diagnostic Sequence ---
if __name__ == '__main__':
    try:
        setup_gpio()
        test_duty_cycle = 60  # A medium speed for testing

        print("\n--- Starting Motor Diagnostic Sequence ---")
        print("Please observe the physical rotation of each wheel.\n")

        # 1. Test right_motor_forward
        print("1. Testing right_motor_forward()...")
        right_motor_forward(test_duty_cycle)
        time.sleep(2)
        stop_all_motors()
        print("   ...Stop.\n")
        time.sleep(2)

        # 2. Test right_motor_backward
        print("2. Testing right_motor_backward()...")
        right_motor_backward(test_duty_cycle)
        time.sleep(2)
        stop_all_motors()
        print("   ...Stop.\n")
        time.sleep(2)

        # 3. Test left_motor_forward
        print("3. Testing left_motor_forward()...")
        left_motor_forward(test_duty_cycle)
        time.sleep(2)
        stop_all_motors()
        print("   ...Stop.\n")
        time.sleep(2)

        # 4. Test left_motor_backward
        print("4. Testing left_motor_backward()...")
        left_motor_backward(test_duty_cycle)
        time.sleep(2)
        stop_all_motors()
        print("   ...Stop.\n")

        print("--- Diagnostic Sequence Complete ---")

    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
    finally:
        cleanup_gpio()
