import sys
import tty
import termios
import select
import time
from adafruit_motorkit import MotorKit

kit = MotorKit()

# Key map
KEYS = {
    '\x1b[A': 'UP',
    '\x1b[B': 'DOWN',
    '\x1b[C': 'RIGHT',
    '\x1b[D': 'LEFT',
    'q': 'QUIT'
}

# Motor mapping for clarity
motors = {
    'm1': lambda v: setattr(kit.motor1, 'throttle', v),  # right back
    'm2': lambda v: setattr(kit.motor2, 'throttle', v),  # left back
    'm3': lambda v: setattr(kit.motor3, 'throttle', v),  # right front
    'm4': lambda v: setattr(kit.motor4, 'throttle', v)   # left front
}

# Speeds
motor_speeds = {'m1': 0.0, 'm2': 0.0, 'm3': 0.0, 'm4': 0.0}
last_logged_speeds = motor_speeds.copy()

MIN_SPEED = 0.6
MAX_SPEED = 1.0
ACCEL = 0.05
DECAY = 0.03

pressed_keys = set()

def get_key():
    if select.select([sys.stdin], [], [], 0)[0]:
        c = sys.stdin.read(1)
        if c == '\x1b':
            c += sys.stdin.read(2)
        return c
    return None

def set_motor_speed(name, value):
    motor_speeds[name] = round(value, 2)
    motors[name](motor_speeds[name])

def update_motors():
    forward = 'UP' in pressed_keys
    backward = 'DOWN' in pressed_keys
    left = 'LEFT' in pressed_keys
    right = 'RIGHT' in pressed_keys

    targets = {'m1': 0, 'm2': 0, 'm3': 0, 'm4': 0}

    # Step 1: Base forward/backward movement
    if forward or backward:
        base_speed = MAX_SPEED if forward else -MAX_SPEED
        targets = {m: base_speed for m in targets}

    # Step 2: Adjust speeds for turning
    if left:
        # Slow down left motors, keep right full
        for m in ['m2', 'm4']:
            if targets[m] != 0:
                targets[m] = base_speed * 0.6
            else:
                targets[m] = MIN_SPEED if forward else -MIN_SPEED
    elif right:
        # Slow down right motors, keep left full
        for m in ['m1', 'm3']:
            if targets[m] != 0:
                targets[m] = base_speed * 0.6
            else:
                targets[m] = MIN_SPEED if forward else -MIN_SPEED

    # Step 3: Smoothly approach target speeds
    for m in targets:
        current = motor_speeds[m]
        target = targets[m]

        if target == 0:
            # Decay
            if abs(current) <= MIN_SPEED:
                new = 0.0
            else:
                new = current - DECAY if current > 0 else current + DECAY
        else:
            # Accelerate
            if current == 0.0:
                current = MIN_SPEED if target > 0 else -MIN_SPEED
            step = ACCEL if target > current else -ACCEL
            new = current + step
            # Clamp between MIN and MAX
            if target > 0:
                new = min(new, target)
            else:
                new = max(new, target)

        set_motor_speed(m, round(new, 2))

    # Determine target speeds
    forward = 'UP' in pressed_keys
    backward = 'DOWN' in pressed_keys
    left = 'LEFT' in pressed_keys
    right = 'RIGHT' in pressed_keys

    targets = {'m1': 0, 'm2': 0, 'm3': 0, 'm4': 0}

    if forward or backward:
        base = MAX_SPEED if forward else -MAX_SPEED
        targets = {k: base for k in targets}

    if left:
        targets['m2'] -= 0.4  # back left
        targets['m4'] -= 0.4  # front left
        targets['m1'] += 0.0 if targets['m1'] != 0 else MIN_SPEED
        targets['m3'] += 0.0 if targets['m3'] != 0 else MIN_SPEED

    if right:
        targets['m1'] -= 0.4  # back right
        targets['m3'] -= 0.4  # front right
        targets['m2'] += 0.0 if targets['m2'] != 0 else MIN_SPEED
        targets['m4'] += 0.0 if targets['m4'] != 0 else MIN_SPEED

    for m, target in targets.items():
        current = motor_speeds[m]

        if target == 0:
            # decay
            if abs(current) <= MIN_SPEED:
                new = 0.0
            else:
                new = current - DECAY if current > 0 else current + DECAY
        else:
            # accelerate
            if current == 0.0:
                current = MIN_SPEED if target > 0 else -MIN_SPEED
            step = ACCEL if target > current else -ACCEL
            new = current + step
            # clamp
            new = max(min(new, MAX_SPEED), -MAX_SPEED)

        set_motor_speed(m, new)

def log_changes():
    global last_logged_speeds
    if motor_speeds != last_logged_speeds:
        print("Motor speeds:")
        for m in motor_speeds:
            print(f"  {m}: {motor_speeds[m]}")
        last_logged_speeds = motor_speeds.copy()

def main():
    old_settings = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin.fileno())
    print("Use arrow keys to move. 'q' to quit.")

    try:
        while True:
            key = get_key()
            if key:
                action = KEYS.get(key)
                if action == 'QUIT':
                    break
                elif action:
                    pressed_keys.add(action)

            # Simulate key release behavior (very basic — can improve)
            if not key:
                pressed_keys.clear()

            update_motors()
            log_changes()
            time.sleep(0.05)

    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
        print("Stopping motors...")
        for m in motors:
            set_motor_speed(m, 0.0)

if __name__ == "__main__":
    main()
