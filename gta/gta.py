import time
from inputs import get_key
from adafruit_motorkit import MotorKit

kit = MotorKit()

# Constants
MAX_SPEED = 1.0
MIN_SPEED = 0.6
ACCEL = 0.05
DECAY = 0.05
UPDATE_INTERVAL = 0.05

# Motor speeds
motor_speeds = {
    "m1": 0.0,  # Right back
    "m2": 0.0,  # Left back
    "m3": 0.0,  # Right front
    "m4": 0.0   # Left front
}

# Pressed key states
key_states = {
    "KEY_UP": False,
    "KEY_DOWN": False,
    "KEY_LEFT": False,
    "KEY_RIGHT": False
}

def apply_motor_speeds():
    kit.motor1.throttle = motor_speeds["m1"]
    kit.motor2.throttle = motor_speeds["m2"]
    kit.motor3.throttle = motor_speeds["m3"]
    kit.motor4.throttle = motor_speeds["m4"]

def accelerate(current, target):
    if abs(target) < MIN_SPEED:
        target = 0
    if current < target:
        return min(current + ACCEL, target)
    elif current > target:
        return max(current - ACCEL, target)
    return current

def decay(current):
    if abs(current) > MIN_SPEED:
        return current - DECAY if current > 0 else current + DECAY
    else:
        return 0

def update_motor_logic():
    target = {"m1": 0, "m2": 0, "m3": 0, "m4": 0}

    forward = key_states["KEY_UP"]
    backward = key_states["KEY_DOWN"]
    left = key_states["KEY_LEFT"]
    right = key_states["KEY_RIGHT"]

    # Base movement
    if forward:
        base = MIN_SPEED
        target.update({"m1": base, "m2": base, "m3": base, "m4": base})
    elif backward:
        base = -MIN_SPEED
        target.update({"m1": base, "m2": base, "m3": base, "m4": base})

    # Turning logic
    if left:
        # Slow down left side, ensure right side gets MIN_SPEED if not moving
        target["m2"] -= 0.2
        target["m4"] -= 0.2
        if target["m1"] == 0:
            target["m1"] = MIN_SPEED
        if target["m3"] == 0:
            target["m3"] = MIN_SPEED
        else:
            target["m1"] += 0.2
            target["m3"] += 0.2

    if right:
        target["m1"] -= 0.2
        target["m3"] -= 0.2
        if target["m2"] == 0:
            target["m2"] = MIN_SPEED
        if target["m4"] == 0:
            target["m4"] = MIN_SPEED
        else:
            target["m2"] += 0.2
            target["m4"] += 0.2

    # Acceleration & Decay
    for m in motor_speeds:
        motor_speeds[m] = (
            accelerate(motor_speeds[m], target[m])
            if target[m] != 0
            else decay(motor_speeds[m])
        )

    apply_motor_speeds()
    print(f"Speeds: {motor_speeds}")

def poll_keys():
    try:
        events = get_key()
        for event in events:
            if event.code in key_states:
                key_states[event.code] = event.state == 1
    except Exception:
        pass  # sometimes get_key throws if nothing is available

def main():
    print("Control with Arrow Keys. Press Ctrl+C to stop.")
    try:
        while True:
            poll_keys()
            update_motor_logic()
            time.sleep(UPDATE_INTERVAL)
    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        for m in motor_speeds:
            motor_speeds[m] = 0
        apply_motor_speeds()

if __name__ == "__main__":
    main()
