/*
  TwoWheelRobot.ino

  This sketch controls a two-wheeled robot using an Arduino UNO and an L298N motor driver.
  The robot can be controlled via the Serial Monitor with simple commands.

  L298N Pin Connections:
  - ENA: Motor A Speed Control (PWM) - Connect to Arduino PWM pin (e.g., D5)
  - IN1: Motor A Direction Control 1 - Connect to Arduino digital pin (e.g., D7)
  - IN2: Motor A Direction Control 2 - Connect to Arduino digital pin (e.g., D8)
  - ENB: Motor B Speed Control (PWM) - Connect to Arduino PWM pin (e.g., D6)
  - IN3: Motor B Direction Control 1 - Connect to Arduino digital pin (e.g., D9)
  - IN4: Motor B Direction Control 2 - Connect to Arduino digital pin (e.g., D10)
  - VCC: L298N Logic Power (+5V from Arduino)
  - GND: Ground
  - MOTA: Connect Motor A
  - MOTB: Connect Motor B
  - VS: Motor Power Supply (e.g., 12V for the motors)

  Serial Commands:
  'f'         - Move forward at default speed
  'f[speed]'  - Move forward at specified speed (e.g., f150, speed 0-255)
  'b'         - Move backward at default speed
  'b[speed]'  - Move backward at specified speed
  'l'         - Pivot left at default speed
  'l[speed]'  - Pivot left at specified speed
  'r'         - Pivot right at default speed
  'r[speed]'  - Pivot right at specified speed
  's'         - Stop motors
*/

// Define L298N Motor Driver Pins

// Motor A (assumed to be the Left Motor)
const int ENA = 5; // Enable A - PWM pin for speed control (must be a PWM pin)
const int IN1 = 7; // Input 1 for Motor A (controls direction)
const int IN2 = 8; // Input 2 for Motor A (controls direction)

// Motor B (assumed to be the Right Motor)
const int ENB = 6; // Enable B - PWM pin for speed control (must be a PWM pin)
const int IN3 = 9; // Input 3 for Motor B (controls direction)
const int IN4 = 10; // Input 4 for Motor B (controls direction)

// Default speed for robot movement (0-255). Used if no speed is specified in the command.
int defaultSpeed = 150;

// Setup function: runs once when the Arduino starts
void setup() {
  // Initialize Serial Communication at 9600 baud rate
  Serial.begin(9600);
  Serial.println("Robot Control System Initialized.");
  Serial.println("Send commands via Serial Monitor (e.g., 'f', 'f200', 's').");
  Serial.println("Commands: f (forward), b (backward), l (left), r (right), s (stop)");
  Serial.println("----------------------------------------------------");

  // Set all motor control pins as outputs
  pinMode(ENA, OUTPUT); // Motor A Speed
  pinMode(IN1, OUTPUT); // Motor A Direction
  pinMode(IN2, OUTPUT); // Motor A Direction
  pinMode(ENB, OUTPUT); // Motor B Speed
  pinMode(IN3, OUTPUT); // Motor B Direction
  pinMode(IN4, OUTPUT); // Motor B Direction

  // Initialize motors to a stopped state to prevent unexpected movement on startup
  motorA_stop();
  motorB_stop();
  Serial.println("Motors initialized to STOPPED state.");
}

// --- Motor A Control Functions ---

/**
 * @brief Drives Motor A forward at a specified speed.
 * @param speed The speed for the motor (0-255).
 */
void motorA_forward(int speed) {
  digitalWrite(IN1, HIGH); // Set direction to forward
  digitalWrite(IN2, LOW);
  analogWrite(ENA, speed);  // Set speed (PWM)
}

/**
 * @brief Drives Motor A backward at a specified speed.
 * @param speed The speed for the motor (0-255).
 */
void motorA_backward(int speed) {
  digitalWrite(IN1, LOW);  // Set direction to backward
  digitalWrite(IN2, HIGH);
  analogWrite(ENA, speed); // Set speed (PWM)
}

/**
 * @brief Stops Motor A.
 */
void motorA_stop() {
  digitalWrite(IN1, LOW);  // Set direction to stop (both inputs low)
  digitalWrite(IN2, LOW);
  analogWrite(ENA, 0);     // Set speed to 0
}

// --- Motor B Control Functions ---

/**
 * @brief Drives Motor B forward at a specified speed.
 * @param speed The speed for the motor (0-255).
 */
void motorB_forward(int speed) {
  digitalWrite(IN3, HIGH); // Set direction to forward
  digitalWrite(IN4, LOW);
  analogWrite(ENB, speed);  // Set speed (PWM)
}

/**
 * @brief Drives Motor B backward at a specified speed.
 * @param speed The speed for the motor (0-255).
 */
void motorB_backward(int speed) {
  digitalWrite(IN3, LOW);  // Set direction to backward
  digitalWrite(IN4, HIGH);
  analogWrite(ENB, speed); // Set speed (PWM)
}

/**
 * @brief Stops Motor B.
 */
void motorB_stop() {
  digitalWrite(IN3, LOW);  // Set direction to stop (both inputs low)
  digitalWrite(IN4, LOW);
  analogWrite(ENB, 0);     // Set speed to 0
}

// --- Robot Movement Functions ---
// These functions coordinate Motor A and Motor B to achieve overall robot movement.

/**
 * @brief Moves the robot forward.
 * @param speed The speed for the movement (0-255).
 */
// Reminder: Motor A = RIGHT Motor (Standard), Motor B = LEFT Motor (Inverted Logic)

/**
 * @brief Moves the robot forward.
 * Desired: RIGHT motor FORWARD, LEFT motor FORWARD.
 * @param speed The speed for the movement (0-255).
 */
void robot_forward(int speed) {
  // RIGHT motor (A) forward: motorA_forward()
  // LEFT motor (B) forward (physically): motorB_backward() [due to inverted logic]
  motorA_forward(speed);
  motorB_backward(speed);
}

/**
 * @brief Moves the robot backward.
 * Desired: RIGHT motor BACKWARD, LEFT motor BACKWARD.
 * @param speed The speed for the movement (0-255).
 */
void robot_backward(int speed) {
  // RIGHT motor (A) backward: motorA_backward()
  // LEFT motor (B) backward (physically): motorB_forward() [due to inverted logic]
  motorA_backward(speed);
  motorB_forward(speed);
}

/**
 * @brief Pivots the robot to the left.
 * Desired: RIGHT motor FORWARD, LEFT motor BACKWARD.
 * @param speed The speed for the pivot (0-255).
 */
void robot_left(int speed) {
  // RIGHT motor (A) forward: motorA_forward()
  // LEFT motor (B) backward (physically): motorB_forward() [due to inverted logic]
  motorA_forward(speed);
  motorB_forward(speed);
}

/**
 * @brief Pivots the robot to the right.
 * Desired: RIGHT motor BACKWARD, LEFT motor FORWARD.
 * @param speed The speed for the pivot (0-255).
 */
void robot_right(int speed) {
  // RIGHT motor (A) backward: motorA_backward()
  // LEFT motor (B) forward (physically): motorB_backward() [due to inverted logic]
  motorA_backward(speed);
  motorB_backward(speed);
}

/**
 * @brief Stops all robot movement.
 */
void robot_stop() {
  motorA_stop();
  motorB_stop();
}

// Main loop function: runs repeatedly after setup()
void loop() {
  // Check if there is data available from the Serial port
  if (Serial.available() > 0) {
    // Read the incoming command string until a newline character ('\n')
    String command = Serial.readStringUntil('\n');
    command.trim(); // Remove any leading/trailing whitespace (like CR, LF)

    char action = ' ';        // Stores the action character (f, b, l, r, s)
    int speed = defaultSpeed; // Use default speed unless a valid speed is specified

    // Parse the command
    if (command.length() > 0) {
      action = command.charAt(0); // Get the first character as the action

      // Check if a speed parameter is provided after the action character
      if (command.length() > 1) {
        String speedStr = command.substring(1); // Get the rest of the string for speed
        speedStr.trim(); // Remove whitespace from speed string

        if (speedStr.length() > 0) {
          int parsedSpeed = speedStr.toInt(); // Convert speed string to integer

          // Validate the parsed speed: must be between 0 and 255.
          // toInt() returns 0 if conversion fails or if the string is "0".
          // We allow speed 0 for movement commands (effectively a stop for that movement).
          if (parsedSpeed >= 0 && parsedSpeed <= 255) {
            speed = parsedSpeed;
          } else {
            // If parsedSpeed is out of 0-255 range (e.g., negative or >255)
            Serial.print("Invalid speed value: ");
            Serial.println(speedStr);
            Serial.println("Speed must be between 0 and 255. Using default speed for this command.");
            // 'speed' remains defaultSpeed or previously set valid speed.
            // For 's' (stop), speed is irrelevant, so this message might be slightly off but harmless.
          }
        }
      }
    }

    // Execute the command based on the action character
    switch (action) {
      case 'f': // Forward
        Serial.print("Command: Forward, Speed: ");
        Serial.println(speed);
        robot_forward(speed);
        break;
      case 'b': // Backward
        Serial.print("Command: Backward, Speed: ");
        Serial.println(speed);
        robot_backward(speed);
        break;
      case 'l': // Left (Pivot)
        Serial.print("Command: Left, Speed: ");
        Serial.println(speed);
        robot_left(speed);
        break;
      case 'r': // Right (Pivot)
        Serial.print("Command: Right, Speed: ");
        Serial.println(speed);
        robot_right(speed);
        break;
      case 's': // Stop
        Serial.println("Command: Stop");
        robot_stop();
        break;
      default:
        // Handle unknown commands if the received string was not empty
        if (command.length() > 0) {
          Serial.print("Unknown command: '");
          Serial.print(command);
          Serial.println("'");
          Serial.println("Available commands: f, b, l, r, s (optional speed, e.g., f150)");
        }
        // If only whitespace or newline was sent, command.length() would be 0 after trim(),
        // and we don't need to print an "Unknown command" message.
        break;
    }
  }
}
