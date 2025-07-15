import RPi.GPIO as GPIO
import time

# GPIO Pin Configuration
# Using BCM numbering scheme for GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False) # Disable warnings for GPIO already in use if re-running script

# Define L298N Motor Driver Pins

# RIGHT Motor (formerly Motor A on Arduino)
# ENA_PIN controls speed (PWM), IN1_PIN & IN2_PIN control direction
ENA_PIN = 18  # Physical Pin 12 (PWM capable)
IN1_PIN = 27  # Physical Pin 13
IN2_PIN = 22  # Physical Pin 15

# LEFT Motor (formerly Motor B on Arduino - this motor had inverted logic)
# ENB_PIN controls speed (PWM), IN3_PIN & IN4_PIN control direction
ENB_PIN = 23  # Physical Pin 16 (PWM capable)
IN3_PIN = 24  # Physical Pin 18 (Connected to L298N IN3)
IN4_PIN = 25  # Physical Pin 22 (Connected to L298N IN4)

# Placeholder for PWM objects - will be initialized in setup_gpio()
# Made global to be accessible by motor control functions
right_pwm = None
left_pwm = None

# Placeholder for default speed (duty cycle 0-100)
DEFAULT_DUTY_CYCLE = 75

def setup_gpio():
    """Sets up GPIO pins for motor control."""
    global right_pwm, left_pwm

    # Set all motor control pins as outputs
    GPIO.setup(ENA_PIN, GPIO.OUT)
    GPIO.setup(IN1_PIN, GPIO.OUT)
    GPIO.setup(IN2_PIN, GPIO.OUT)
    GPIO.setup(ENB_PIN, GPIO.OUT)
    GPIO.setup(IN3_PIN, GPIO.OUT)
    GPIO.setup(IN4_PIN, GPIO.OUT)

    # Initialize motors to a stopped state (direction pins low)
    GPIO.output(IN1_PIN, GPIO.LOW)
    GPIO.output(IN2_PIN, GPIO.LOW)
    GPIO.output(IN3_PIN, GPIO.LOW)
    GPIO.output(IN4_PIN, GPIO.LOW)

    # Initialize PWM objects for speed control
    # Using 100 Hz frequency for PWM
    right_pwm = GPIO.PWM(ENA_PIN, 100)
    left_pwm = GPIO.PWM(ENB_PIN, 100)

    # Start PWM with 0% duty cycle (motors stopped)
    right_pwm.start(0)
    left_pwm.start(0)
    print("GPIO pins setup complete. Motors initialized to stopped.")

# --- Individual Motor Control Functions ---

# RIGHT Motor Controls (Standard Behavior)
def right_motor_forward(duty_cycle):
    """Drives the RIGHT motor forward at a given duty cycle (0-100)."""
    GPIO.output(IN1_PIN, GPIO.HIGH)
    GPIO.output(IN2_PIN, GPIO.LOW)
    right_pwm.ChangeDutyCycle(duty_cycle)

def right_motor_backward(duty_cycle):
    """Drives the RIGHT motor backward at a given duty cycle (0-100)."""
    GPIO.output(IN1_PIN, GPIO.LOW)
    GPIO.output(IN2_PIN, GPIO.HIGH)
    right_pwm.ChangeDutyCycle(duty_cycle)

def right_motor_stop():
    """Stops the RIGHT motor."""
    GPIO.output(IN1_PIN, GPIO.LOW)
    GPIO.output(IN2_PIN, GPIO.LOW)
    right_pwm.ChangeDutyCycle(0)

# LEFT Motor Controls (Corrected for Inverted Physical Behavior)
# The L298N IN3/IN4 pin logic is set opposite to achieve desired physical motion.
def left_motor_forward(duty_cycle):
    """Drives the LEFT motor physically FORWARD at a given duty cycle (0-100)."""
    # To make Left motor go physically FORWARD, use L298N "backward" config for its pins
    # This corresponds to original Arduino motorB_backward() which made it go physically FORWARD
    GPIO.output(IN3_PIN, GPIO.LOW)   # L298N IN3 for Left Motor
    GPIO.output(IN4_PIN, GPIO.HIGH)  # L298N IN4 for Left Motor
    left_pwm.ChangeDutyCycle(duty_cycle)

def left_motor_backward(duty_cycle):
    """Drives the LEFT motor physically BACKWARD at a given duty cycle (0-100)."""
    # To make Left motor go physically BACKWARD, use L298N "forward" config for its pins
    # This corresponds to original Arduino motorB_forward() which made it go physically BACKWARD
    GPIO.output(IN3_PIN, GPIO.HIGH)  # L298N IN3 for Left Motor
    GPIO.output(IN4_PIN, GPIO.LOW)   # L298N IN4 for Left Motor
    left_pwm.ChangeDutyCycle(duty_cycle)

def left_motor_stop():
    """Stops the LEFT motor."""
    GPIO.output(IN3_PIN, GPIO.LOW)
    GPIO.output(IN4_PIN, GPIO.LOW)
    left_pwm.ChangeDutyCycle(0)

# --- Robot Movement Functions ---
def robot_forward(duty_cycle):
    """Moves the robot forward."""
    right_motor_forward(duty_cycle)
    left_motor_forward(duty_cycle)
    print(f"Robot Forward at {duty_cycle}% duty cycle")

def robot_backward(duty_cycle):
    """Moves the robot backward."""
    right_motor_backward(duty_cycle)
    left_motor_backward(duty_cycle)
    print(f"Robot Backward at {duty_cycle}% duty cycle")

def robot_turn_left(duty_cycle):
    """Pivots the robot to the left."""
    # Right motor forward, Left motor backward
    right_motor_forward(duty_cycle)
    left_motor_backward(duty_cycle)
    print(f"Robot Turning Left at {duty_cycle}% duty cycle")

def robot_turn_right(duty_cycle):
    """Pivots the robot to the right."""
    # Right motor backward, Left motor forward
    right_motor_backward(duty_cycle)
    left_motor_forward(duty_cycle)
    print(f"Robot Turning Right at {duty_cycle}% duty cycle")

def robot_stop():
    """Stops all robot movement."""
    right_motor_stop()
    left_motor_stop()
    print("Robot Stop")

def cleanup_gpio():
    """Stops PWM and cleans up GPIO channels."""
    print("\nCleaning up GPIO...")
    if right_pwm:
        right_pwm.stop()
    if left_pwm:
        left_pwm.stop()
    GPIO.cleanup()
    print("GPIO cleanup complete.")

if __name__ == '__main__':
    try:
        setup_gpio() # Call the setup function
        print("Robot Controller Script Initialized and GPIO setup.")
        print("Pin Definitions:")
        print(f"  Right Motor: ENA={ENA_PIN}, IN1={IN1_PIN}, IN2={IN2_PIN}")
        print(f"  Left Motor: ENB={ENB_PIN}, IN3={IN3_PIN}, IN4={IN4_PIN}")

        print("\n--- Interactive Command Line Test Interface ---")
        print("Commands: f (forward), b (backward), l (turn_left), r (turn_right), s (stop)")
        print("Optionally, add a duty cycle (0-100) after the command, e.g., 'f 75'")
        print("Type 'q' or 'exit' to quit.")

        # Comment out or remove the automated test sequence if using interactive mode primarily
        # print("\n--- Skipping Automated Test Sequence for Interactive Mode ---")
        # --- Test Sequence for Individual Motor Functions (Optional: Comment out to skip) ---
        # print("\n--- Testing Individual Motors ---")
        # ... (automated tests from previous version can be kept here if desired for quick checks)
        # print("--- Individual Motor Tests Complete ---")
        # --- Test Sequence for Robot Movement Functions ---
        # print("\n--- Testing Robot Movements ---")
        # ... (automated tests from previous version can be kept here if desired for quick checks)
        # print("--- Robot Movement Tests Complete ---")

        while True:
            command_input = input("Enter command: ").strip().lower()

            if command_input in ['q', 'exit']:
                print("Exiting interactive mode.")
                break

            parts = command_input.split()
            action = parts[0]

            duty_cycle = DEFAULT_DUTY_CYCLE # Use default if not specified
            if len(parts) > 1:
                try:
                    speed_param = int(parts[1])
                    if 0 <= speed_param <= 100:
                        duty_cycle = speed_param
                    else:
                        print("Invalid duty cycle. Must be 0-100. Using default.")
                except ValueError:
                    print("Invalid speed parameter. Using default duty cycle.")

            if action == 'f':
                robot_forward(duty_cycle)
            elif action == 'b':
                robot_backward(duty_cycle)
            elif action == 'l':
                robot_turn_left(duty_cycle)
            elif action == 'r':
                robot_turn_right(duty_cycle)
            elif action == 's':
                robot_stop()
            else:
                print(f"Unknown command: {action}")

            time.sleep(0.1) # Small delay to prevent rapid re-prompting if used in a tight loop by mistake

    except KeyboardInterrupt:
        print("\nProgram exited by user (Ctrl+C)")
    finally:
        cleanup_gpio() # Call the cleanup function
