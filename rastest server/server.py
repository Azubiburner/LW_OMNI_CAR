import asyncio
import websockets

connected_clients = set()
link = "ws://localhost:"
port = ["8001","8002","8003","8004"]
cars = ["car1","car2","car3","car4"]
async def handle_client(websocket):
    connected_clients.add(websocket)
    print("Client connected")

    try:
        async for message in websocket:
            print("Nachricht vom Browser: " + message)
            print("Verbinde zu "+message[1:5])
            if(message[1:5] in cars):
                print("Verbinde zu "+message[1:5])
                print("command: "+message[5:][:-1]+"for "+message[1:5])
                await websocket.send("Waiting for Car")
                socket= link+port[cars.index(message[1:5])]
                print("Verbinde zu "+socket)
            # Nachricht an html senden und Antwort empfangen
                response = await connect_to_car(socket, message)
                if response:
                    await websocket.send("Antwort von "+message[1:5]+": " + response)
            else:
                await websocket.send("Waiting for Car")

            # Antwort an Browser zurücksenden
            

    except websockets.exceptions.ConnectionClosed:
        print("Connection geschlossen")
    finally:
        connected_clients.remove(websocket)

async def connect_to_car(uri, message):
    try:
        async with websockets.connect(uri) as car_ws:
            print("Verbindung zu "+ message[1:5]+": " +" hergestellt")
            await car_ws.send(message)
            response = await car_ws.recv()
            print("Antwort von "+message[1:5]+": " + response)
            return response
    except Exception as e:
        print(f"Fehler bei Verbindung zu car1: {e}")
        return None

async def main():
    print("Server läuft auf Port 8000")
    async with websockets.serve(handle_client, "", 8000):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
