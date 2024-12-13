import cv2
import websockets, requests
import asyncio, time
import numpy as np
import base64
import json

async def receive_video(websocket):
    while True:
        data = json.loads(await websocket.recv())
        frame = cv2.imdecode(np.frombuffer(base64.b64decode(data["image"]), np.uint8), cv2.IMREAD_COLOR)

        print(f"MS: {(time.time() - float(data["time"])) * 1000 :.2f}, MB: {data["size"]}")

        if frame is not None: cv2.imshow("Received Video", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'): break

    cv2.destroyAllWindows()

async def main():
    async with websockets.connect("ws://192.168.31.252:6789") as websocket:
        print(f"Sunucuya bağlanıldı: {"ws://192.168.31.252:6789"}")
        await receive_video(websocket)

if __name__ == "__main__":
    asyncio.run(main())
