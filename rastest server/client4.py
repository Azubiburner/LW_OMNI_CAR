import websockets
import asyncio

async def client_handler(websocket):
    print("car1 verbunden")
    try:
        async for command in websocket:
            print("Empfangen von Server: " + command)

            # Beispiel: Antwort zurücksenden
            comsmand = command[6:][:-1]
            await command_execute(comsmand)
            antwort = f"car1 hat '{command}' empfangen"
            await websocket.send(antwort)

    except websockets.exceptions.ConnectionClosed:
        print("Verbindung zu car1 geschlossen")

async def main():
    print("car1 wartet auf Verbindung...")
    async with websockets.serve(client_handler, "", 8004):
        await asyncio.Future()  # Run forever

async def command_execute(comm):
    
    print(f"Verarbeite Befehl: {comm}")
    print("hi"=='hi')
    # Hier können Sie den empfangenen Befehl verarbeiten
    commands = ["forward", "backward", "left", "right", "diagonal-left", "diagonal-right", "stop", "turn-left", "turn-right"]
    if comm in commands:
        print(f"Der Befehl '{comm}' ist gültig.")
    else:
        print(f"Der Befehl '{comm}' ist ungültig.")
    

if __name__ == "__main__":
    asyncio.run(main())
