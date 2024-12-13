import websockets
import asyncio
import numpy as np

# Kamera açma

# WebSocket sunucu fonksiyonu
async def send_video(websocket, path=None):
    try:
        while True:
            # Kameradan bir kare al
            await websocket.send("sa")

            # 0.1 saniye bekle
            # await asyncio.sleep(0.033)
    except websockets.exceptions.ConnectionClosed as e:
        print(f"Connection closed: {e}")
    finally:
        print("Sunucu bağlantıyı kapattı.")

# WebSocket server'ı başlat
async def start_server():
    try:
        server = await websockets.serve(send_video, "192.168.31.252", 6789)
        await server.wait_closed()
    except Exception as e:
        print(f"Sunucu hatası: {e}")

# Event loop başlat
if __name__ == "__main__":
    asyncio.run(start_server())
