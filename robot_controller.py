import RPi.GPIO as GPIO
import time
import atexit
from flask import Flask, render_template

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
    # Goal: Right FORWARD, Left FORWARD
    # Confirmed via diagnostics:
    # - right_motor_forward() -> Right physical FORWARD
    # - left_motor_backward() -> Left physical FORWARD
    right_motor_forward(duty_cycle)
    left_motor_backward(duty_cycle)
    print(f"Robot Forward at {duty_cycle}% duty cycle")

def robot_backward(duty_cycle):
    """Moves the robot backward."""
    # Goal: Right BACKWARD, Left BACKWARD
    # Confirmed via diagnostics:
    # - right_motor_backward() -> Right physical BACKWARD
    # - left_motor_forward() -> Left physical BACKWARD
    right_motor_backward(duty_cycle)
    left_motor_forward(duty_cycle)
    print(f"Robot Backward at {duty_cycle}% duty cycle")

def robot_turn_left(duty_cycle):
    """Pivots the robot to the left."""
    # Goal: Right FORWARD, Left BACKWARD
    # Confirmed via diagnostics:
    # - right_motor_forward() -> Right physical FORWARD
    # - left_motor_forward() -> Left physical BACKWARD
    right_motor_forward(duty_cycle)
    left_motor_forward(duty_cycle)
    print(f"Robot Turning Left at {duty_cycle}% duty cycle")

def robot_turn_right(duty_cycle):
    """Pivots the robot to the right."""
    # Goal: Right BACKWARD, Left FORWARD
    # Confirmed via diagnostics:
    # - right_motor_backward() -> Right physical BACKWARD
    # - left_motor_backward() -> Left physical FORWARD
    right_motor_backward(duty_cycle)
    left_motor_backward(duty_cycle)
    print(f"Robot Turning Right at {duty_cycle}% duty cycle")

def robot_stop():
    """Stops all robot movement."""
    right_motor_stop()
    left_motor_stop()
    print("Robot Stop")

# --- Pattern Functions ---
def robot_spin(duty_cycle, duration):
    """Spins the robot to the right for a given duration."""
    print(f"Pattern: Spin right for {duration}s at {duty_cycle}% speed")
    robot_turn_right(duty_cycle)
    time.sleep(duration)
    robot_stop()
    print("Pattern: Spin complete")

def robot_square(duty_cycle, side_duration):
    """Drives the robot in a square pattern."""
    # A 90-degree turn duration is hardware-dependent. This is a guess.
    turn_duration = 0.5
    print(f"Pattern: Drive square with side duration {side_duration}s at {duty_cycle}% speed")
    for i in range(4):
        print(f"  Square side {i+1}")
        # Drive forward for one side
        robot_forward(duty_cycle)
        time.sleep(side_duration)
        # Stop
        robot_stop()
        time.sleep(0.2)
        # Turn right
        robot_turn_right(duty_cycle)
        time.sleep(turn_duration)
        # Stop
        robot_stop()
        time.sleep(0.2)
    print("Pattern: Square complete")


def cleanup_gpio():
    """Stops PWM and cleans up GPIO channels."""
    print("\nCleaning up GPIO...")
    if right_pwm:
        right_pwm.stop()
    if left_pwm:
        left_pwm.stop()
    GPIO.cleanup()
    print("GPIO cleanup complete.")

# --- Flask App Setup ---
app = Flask(__name__)

# Register the cleanup function to be called on exit
atexit.register(cleanup_gpio)

# Setup GPIO pins before starting the app
setup_gpio()

# --- Flask Routes ---

@app.route('/')
def index():
    """Serves the main control page."""
    return render_template('index.html')

@app.route('/move/<direction>/<int:speed>')
@app.route('/move/<direction>')
def move(direction, speed=None):
    """
    Handles movement commands from the web interface.
    Accepts an optional speed parameter (0-100).
    """
    if speed is None:
        speed = DEFAULT_DUTY_CYCLE

    # Validate speed to be within 0-100 range
    if not 0 <= speed <= 100:
        return {'status': 'error', 'message': 'Invalid speed. Must be between 0 and 100.'}, 400

    if direction == 'forward':
        robot_forward(speed)
    elif direction == 'backward':
        robot_backward(speed)
    elif direction == 'left':
        robot_turn_left(speed)
    elif direction == 'right':
        robot_turn_right(speed)
    elif direction == 'stop':
        robot_stop()
    else:
        return {'status': 'error', 'message': 'Invalid direction'}, 400

    return {'status': 'ok', 'action': direction, 'speed': speed}

@app.route('/pattern/<pattern_name>')
def pattern(pattern_name):
    """Handles pattern commands from the web interface."""
    duty_cycle = DEFAULT_DUTY_CYCLE

    if pattern_name == 'spin':
        # Default spin for 2 seconds
        robot_spin(duty_cycle, 2)
    elif pattern_name == 'square':
        # Default square with 1-second sides
        robot_square(duty_cycle, 1)
    else:
        return {'status': 'error', 'message': 'Invalid pattern name'}, 400

    return {'status': 'ok', 'action': pattern_name}


if __name__ == '__main__':
    # Setting host to '0.0.0.0' makes the server publicly available
    # on your network, so you can access it from your phone.
    print("Starting Flask web server...")
    print("Access the control interface at http://<YOUR_PI_IP_ADDRESS>:5000")
    app.run(host='0.0.0.0', port=5000)
