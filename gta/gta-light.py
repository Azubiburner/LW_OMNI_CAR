import curses
from adafruit_motorkit import MotorKit
import time

kit = MotorKit()

MIN_SPEED = 1.0
MAX_SPEED = 1.0
ACCEL_STEP = 0.085
DECAY = 0.05
LOOP_DELAY = 0.05  # 50ms

left_speed = 0.0
right_speed = 0.0

def set_motor_throttle(left, right):
    kit.motor1.throttle = left
    kit.motor2.throttle = right
    kit.motor3.throttle = left
    kit.motor4.throttle = right

def approach(current, target, step):
    if current < target:
        return min(current + step, target)
    elif current > target:
        return max(current - step, target)
    return current

def main(stdscr):
    global left_speed, right_speed

    curses.cbreak()
    stdscr.keypad(True)
    stdscr.nodelay(True)
    curses.noecho()

    stdscr.addstr("Use arrow keys to move, 'q' to quit\n")

    try:
        while True:
            keys_pressed = set()

            while True:
                key = stdscr.getch()
                if key == -1:
                    break
                keys_pressed.add(key)

            # Flags for movement
            forward = curses.KEY_UP in keys_pressed
            backward = curses.KEY_DOWN in keys_pressed
            left = curses.KEY_LEFT in keys_pressed
            right = curses.KEY_RIGHT in keys_pressed

            target_left = 0.0
            target_right = 0.0

            if forward:
                target_left += MAX_SPEED
                target_right += MAX_SPEED
            if backward:
                target_left -= MAX_SPEED
                target_right -= MAX_SPEED
            if left:
                target_left -= MAX_SPEED
                target_right += MAX_SPEED
            if right:
                target_left += MAX_SPEED
                target_right -= MAX_SPEED

            # Apply minimum speed when moving
            if target_left != 0:
                target_left = (MIN_SPEED + (MAX_SPEED - MIN_SPEED)) * (1 if target_left > 0 else -1)
                print(f"Apply minimum left speed of: {target_left}")
            if target_right != 0:
                target_right = (MIN_SPEED + (MAX_SPEED - MIN_SPEED)) * (1 if target_right > 0 else -1)
                print(f"Apply minimum right speed of: {target_right}")

            # Handle decay directly to 0 when below MIN_SPEED
            if target_left == 0 and left_speed < MIN_SPEED:
                print(f"Decay left speed to 0: {left_speed}")  # Logging when decay happens
                left_speed = 0
            if target_right == 0 and right_speed < MIN_SPEED:
                print(f"Decay right speed to 0: {right_speed}")
                right_speed = 0

            # Smooth acceleration/deceleration
            left_speed = approach(left_speed, target_left, ACCEL_STEP if target_left != 0 else DECAY)
            right_speed = approach(right_speed, target_right, ACCEL_STEP if target_right != 0 else DECAY)

            # Jump directly to MIN_SPEED if we are starting from 0
            if left_speed == 0 and target_left != 0:
                print("Jumping left speed to MIN_SPEED")  # Logging when we jump to MIN_SPEED
                left_speed = MIN_SPEED
            if right_speed == 0 and target_right != 0:
                print("Jumping right speed to MIN_SPEED")  # Logging when we jump to MIN_SPEED
                right_speed = MIN_SPEED

            # Apply to motors
            set_motor_throttle(left_speed, right_speed)

            # Exit on 'q'
            if ord('q') in keys_pressed:
                break

            time.sleep(LOOP_DELAY)

    finally:
        set_motor_throttle(0, 0)
        curses.nocbreak()
        stdscr.keypad(False)
        curses.echo()
        curses.endwin()

if __name__ == "__main__":
    curses.wrapper(main)
