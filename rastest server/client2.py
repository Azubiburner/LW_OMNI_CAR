import websockets
import asyncio

async def client_handler(websocket):
    print("car2 verbunden")
    try:
        async for command in websocket:
            print("Empfangen von Server: " + command)

            # Beispiel: Antwort zurücksenden
            antwort = f"car2 hat '{command}' empfangen"
            await websocket.send(antwort)

    except websockets.exceptions.ConnectionClosed:
        print("Verbindung zu car2 geschlossen")

async def main():
    print("car2 wartet auf Verbindung...")
    async with websockets.serve(client_handler, "", 8002):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
