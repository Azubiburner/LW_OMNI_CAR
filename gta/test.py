from sshkeyboard import listen_keyboard
from adafruit_motorkit import MotorKit

# Initialize the motor kit
kit = MotorKit()

# Constants for controlling the motors
MIN_SPEED = 0.6  # minimum speed to start with for noticeable movement
MAX_SPEED = 1.0
ACCELERATION_RATE = 0.1  # Speed increment per key press
DECELERATION_RATE = 0.05  # Deceleration rate for turning

# Initial speeds (starting with a minimum)
motor_speeds = {
    "m1": 0.0,  # back right
    "m2": 0.0,  # back left
    "m3": 0.0,  # front right
    "m4": 0.0   # front left
}

# Track the state of the keys
pressed_keys = set()

# Motor speed update function
def set_motor_speeds():
    kit.motor1.throttle = motor_speeds["m1"]  # Back right (m1)
    kit.motor2.throttle = motor_speeds["m2"]  # Back left (m2)
    kit.motor3.throttle = motor_speeds["m3"]  # Front right (m3)
    kit.motor4.throttle = motor_speeds["m4"]  # Front left (m4)
    
    # Print the current motor speeds after each key press
    print(f"Motor speeds after key press:")
    print(f"  m1 (Back Right): {motor_speeds['m1']}")
    print(f"  m2 (Back Left): {motor_speeds['m2']}")
    print(f"  m3 (Front Right): {motor_speeds['m3']}")
    print(f"  m4 (Front Left): {motor_speeds['m4']}")

# Accelerate or decelerate motors based on inputs
def change_speed_forwards():
    if motor_speeds["m1"] < MAX_SPEED:
        motor_speeds["m1"] = min(motor_speeds["m1"] + ACCELERATION_RATE, MAX_SPEED)
    if motor_speeds["m2"] < MAX_SPEED:
        motor_speeds["m2"] = min(motor_speeds["m2"] + ACCELERATION_RATE, MAX_SPEED)
    if motor_speeds["m3"] < MAX_SPEED:
        motor_speeds["m3"] = min(motor_speeds["m3"] + ACCELERATION_RATE, MAX_SPEED)
    if motor_speeds["m4"] < MAX_SPEED:
        motor_speeds["m4"] = min(motor_speeds["m4"] + ACCELERATION_RATE, MAX_SPEED)

def change_speed_backwards():
    if motor_speeds["m1"] > -MAX_SPEED:
        motor_speeds["m1"] = max(motor_speeds["m1"] - ACCELERATION_RATE, -MAX_SPEED)
    if motor_speeds["m2"] > -MAX_SPEED:
        motor_speeds["m2"] = max(motor_speeds["m2"] - ACCELERATION_RATE, -MAX_SPEED)
    if motor_speeds["m3"] > -MAX_SPEED:
        motor_speeds["m3"] = max(motor_speeds["m3"] - ACCELERATION_RATE, -MAX_SPEED)
    if motor_speeds["m4"] > -MAX_SPEED:
        motor_speeds["m4"] = max(motor_speeds["m4"] - ACCELERATION_RATE, -MAX_SPEED)

def adjust_turning_left():
    if motor_speeds["m1"] > MIN_SPEED:
        motor_speeds["m1"] -= DECELERATION_RATE
    if motor_speeds["m3"] > MIN_SPEED:
        motor_speeds["m3"] -= DECELERATION_RATE
    if motor_speeds["m2"] < MAX_SPEED:
        motor_speeds["m2"] += DECELERATION_RATE
    if motor_speeds["m4"] < MAX_SPEED:
        motor_speeds["m4"] += DECELERATION_RATE

def adjust_turning_right():
    if motor_speeds["m1"] < -MIN_SPEED:
        motor_speeds["m1"] += DECELERATION_RATE
    if motor_speeds["m3"] < -MIN_SPEED:
        motor_speeds["m3"] += DECELERATION_RATE
    if motor_speeds["m2"] > -MAX_SPEED:
        motor_speeds["m2"] -= DECELERATION_RATE
    if motor_speeds["m4"] > -MAX_SPEED:
        motor_speeds["m4"] -= DECELERATION_RATE

def rotate_left():
    if motor_speeds["m1"] > -MAX_SPEED:
        motor_speeds["m1"] -= ACCELERATION_RATE
    if motor_speeds["m2"] < MAX_SPEED:
        motor_speeds["m2"] += ACCELERATION_RATE
    if motor_speeds["m3"] > -MAX_SPEED:
        motor_speeds["m3"] -= ACCELERATION_RATE
    if motor_speeds["m4"] < MAX_SPEED:
        motor_speeds["m4"] += ACCELERATION_RATE

def rotate_right():
    if motor_speeds["m1"] < MAX_SPEED:
        motor_speeds["m1"] += ACCELERATION_RATE
    if motor_speeds["m2"] > -MAX_SPEED:
        motor_speeds["m2"] -= ACCELERATION_RATE
    if motor_speeds["m3"] < MAX_SPEED:
        motor_speeds["m3"] += ACCELERATION_RATE
    if motor_speeds["m4"] > -MAX_SPEED:
        motor_speeds["m4"] -= ACCELERATION_RATE

def stop():
    motor_speeds["m1"] = 0
    motor_speeds["m2"] = 0
    motor_speeds["m3"] = 0
    motor_speeds["m4"] = 0

def on_key_press(key):
    """Called when a key is pressed."""
    
    # Track pressed keys
    pressed_keys.add(key)

    # Reset motor speeds to zero to avoid conflicting key press actions
    if "w" in pressed_keys:
        if motor_speeds["m1"] == 0 and motor_speeds["m2"] == 0 and motor_speeds["m3"] == 0 and motor_speeds["m4"] == 0:
            motor_speeds["m1"] = motor_speeds["m2"] = motor_speeds["m3"] = motor_speeds["m4"] = MIN_SPEED  # Start from minimum speed
        change_speed_forwards()
        print("Moving forward.")
    elif "s" in pressed_keys:
        change_speed_backwards()
        print("Moving backward.")
    elif "a" in pressed_keys:
        adjust_turning_left()
        print("Turning left.")
    elif "d" in pressed_keys:
        adjust_turning_right()
        print("Turning right.")
    elif "q" in pressed_keys:
        rotate_left()
        print("Rotating left.")
    elif "e" in pressed_keys:
        rotate_right()
        print("Rotating right.")
    elif " " in pressed_keys:
        stop()
        print("Stopping motors.")
    else:
        stop()

    # Update motor speeds
    set_motor_speeds()

def main():
    print("Press WASD for movement, Q for rotating left, E for rotating right, and space for stopping.")
    listen_keyboard(on_key_press)

if __name__ == "__main__":
    main()
