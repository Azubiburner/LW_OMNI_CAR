import websockets
import asyncio
#import lib.movement as m
import lib.controller as c
import os

#Einstellen
name = "omni01"
#ip = "192.168.1.175"
ip = "127.0.0.1"
port= 9011 

async def client_handler(websocket):
    print("car1 verbunden")
    try:
        async for command in websocket:
            print("Empfangen von Server: " + command)

            # Beispiel: Antwort zurücksenden
            comsmand = command[6:][:-1]
            await c.command_execute(comsmand)
            antwort = f"car1 hat '{command}' empfangen"
            await websocket.send(antwort)

    except websockets.exceptions.ConnectionClosed:
        print("Verbindung zu car1 geschlossen")

async def main():
    print("car1 wartet auf Verbindung...")
    async with websockets.serve(client_handler, ip, port):
        await asyncio.Future()  # Run forever



    

if __name__ == "__main__":
    os.system("libcamera-vid -t 0 --width 640 --height 360 --framerate 30 --codec h264 -o - | ffmpeg -re -i - -c:v copy -f rtsp rtsp://server:8554/stream/omni03")
    asyncio.run(main())
