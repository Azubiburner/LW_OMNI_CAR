import asyncio
import websockets
import json
from adafruit_motorkit import MotorKit
import time

# Initialize the motor kit
kit = MotorKit()

# Constants for controlling the motors
MIN_SPEED = 1.0
MAX_SPEED = 1.0
ACCEL_STEP = 0.085
DECAY = 0.05
LOOP_DELAY = 0.05  # 50ms delay between updates

# Initial speeds
left_speed = 0.0
right_speed = 0.0

# Function to set motor speeds
def set_motor_throttle(left, right):
    kit.motor1.throttle = left
    kit.motor2.throttle = right
    kit.motor3.throttle = left
    kit.motor4.throttle = right

# Function for smooth acceleration and deceleration
def approach(current, target, step):
    if current < target:
        return min(current + step, target)
    elif current > target:
        return max(current - step, target)
    return current

# WebSocket handler
async def motor_control(websocket, path):
    global left_speed, right_speed
    
    # Send a message when a client connects
    await websocket.send("Connected to RC Car WebSocket Server")

    try:
        while True:
            # Wait for a message from the client
            message = await websocket.recv()
            data = json.loads(message)

            # Extract movement commands from the received message
            forward = data.get('forward', False)
            backward = data.get('backward', False)
            left = data.get('left', False)
            right = data.get('right', False)
            rotate_left = data.get('rotate_left', False)
            rotate_right = data.get('rotate_right', False)
            stop = data.get('stop', False)

            target_left = 0.0
            target_right = 0.0

            # Handle forward and backward movement
            if forward:
                target_left += MAX_SPEED
                target_right += MAX_SPEED
            if backward:
                target_left -= MAX_SPEED
                target_right -= MAX_SPEED

            # Handle left and right movement (turning)
            if left:
                target_left -= MAX_SPEED
                target_right += MAX_SPEED
            if right:
                target_left += MAX_SPEED
                target_right -= MAX_SPEED

            # Handle 360-degree rotation
            if rotate_left:
                target_left = MAX_SPEED
                target_right = -MAX_SPEED
            if rotate_right:
                target_left = -MAX_SPEED
                target_right = MAX_SPEED

            # Apply the minimum speed when moving
            if target_left != 0:
                target_left = (MIN_SPEED + (MAX_SPEED - MIN_SPEED)) * (1 if target_left > 0 else -1)
            if target_right != 0:
                target_right = (MIN_SPEED + (MAX_SPEED - MIN_SPEED)) * (1 if target_right > 0 else -1)

            # Handle decay directly to 0 when below MIN_SPEED
            if target_left == 0 and left_speed < MIN_SPEED:
                left_speed = 0
            if target_right == 0 and right_speed < MIN_SPEED:
                right_speed = 0

            # Smooth acceleration and deceleration
            left_speed = approach(left_speed, target_left, ACCEL_STEP if target_left != 0 else DECAY)
            right_speed = approach(right_speed, target_right, ACCEL_STEP if target_right != 0 else DECAY)

            # Jump directly to MIN_SPEED if starting from 0
            if left_speed == 0 and target_left != 0:
                left_speed = MIN_SPEED
            if right_speed == 0 and target_right != 0:
                right_speed = MIN_SPEED

            # Apply motor speeds
            set_motor_throttle(left_speed, right_speed)

            # Send updated motor speeds back to the client
            motor_speeds = {
                'm1': left_speed,
                'm2': right_speed,
                'm3': left_speed,
                'm4': right_speed
            }
            await websocket.send(json.dumps(motor_speeds))

            # Stop if the stop key is pressed
            if stop:
                break

            time.sleep(LOOP_DELAY)

    except websockets.exceptions.ConnectionClosed as e:
        print("Connection closed")

    finally:
        # Stop the motors when the connection is closed
        set_motor_throttle(0, 0)

# Start the WebSocket server
async def start_server():
    server = await websockets.serve(motor_control, "localhost", 8765)
    print("WebSocket server started on ws://localhost:8765")
    await server.wait_closed()

# Run the server
if __name__ == "__main__":
    asyncio.run(start_server())
