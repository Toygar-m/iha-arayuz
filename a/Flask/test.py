import cv2
import time
import websockets
import asyncio
import numpy as np
import base64
import json
import os

framecount = 0
cap = cv2.VideoCapture(0)

async def send_video(websocket, path=None):
    global framecount
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            _, buffer = cv2.imencode('.jpeg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 50])

            image_size_mb = len(buffer) / (1024 * 1024)

            await websocket.send(json.dumps({
                "image": base64.b64encode(buffer).decode('utf-8'),
                "time": str(time.time()),
                "size": round(image_size_mb, 4)
            }))

            # os.makedirs("sdsa", exist_ok=True)
            # with open(f"sdsa/{framecount}.jpeg", 'wb') as f:
            #     f.write(buffer)

            # framecount += 1
            await asyncio.sleep(0.033)

    except websockets.exceptions.ConnectionClosed as e:
        print(f"Connection closed: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        print("Server connection closed.")

async def start_server():
    try:
        server = await websockets.serve(send_video, "192.168.31.252", 6789)
        await server.wait_closed()
    except Exception as e:
        print(f"Server error: {e}")

if __name__ == "__main__":
    asyncio.run(start_server())
