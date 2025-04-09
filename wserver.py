import asyncio
import websockets

# Set of connected clients
connected_clients = set()

# Function to handle each client connection
async def handle_client(websocket):
    # Add the new client to the set of connected clients
    connected_clients.add(websocket)
    print("Client connected")
    try:
        # Listen for messages from the client
        async for message in websocket:
            print("Nachricht: " + message)
            # Broadcast the message to all other connected clients
            for client in connected_clients:
                if client != websocket:
                    print("Nachricht weitergeleitet: " + message)
                    await client.send(message)
    except websockets.exceptions.ConnectionClosed:
        print("Connection geschlossen")
    finally:
        # Remove the client from the set of connected clients
        connected_clients.remove(websocket)

# Main function to start the WebSocket server
async def main():
    server = await websockets.serve(handle_client, '192.168.1.105', 8000)
    await server.wait_closed()

# Run the server
if __name__ == "__main__":
    asyncio.run(main())

