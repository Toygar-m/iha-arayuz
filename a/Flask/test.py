import cv2
import websockets
import asyncio
import numpy as np
import base64
import json

# Kamera açma
cap = cv2.VideoCapture(0)

# WebSocket sunucu fonksiyonu
async def send_video(websocket, path=None):
    try:
        while True:
            # Kameradan bir kare al
            ret, frame = cap.read()
            if not ret:
                break

            # Görüntüyü Base64 formatına çevir
            _, buffer = cv2.imencode('.jpg', frame)
            jpg_as_text = base64.b64encode(buffer).decode('utf-8')

            # JSON formatında gönder
            message = json.dumps({"image": jpg_as_text})

            # WebSocket üzerinden gönder
            await websocket.send(message)

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
