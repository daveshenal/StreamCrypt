import cv2
import asyncio
import websockets
import numpy as np

from core.encryption import decrypt_data
from core.compression import decompress_data

# Function to display frames
async def display_frames():
    print("Connecting to WebSocket server...")
    uri = "ws://localhost:8000/stream"  # WebSocket server URI
    async with websockets.connect(uri) as websocket:
        print("Successfully connected to WebSocket server")

        while True:
            # Receive the encrypted frame from the server
            encrypted_frame = await websocket.recv()
            decrypted_frame = decrypt_data(encrypted_frame)
            decompressed_frame = decompress_data(decrypted_frame)
            frame = cv2.imdecode(np.frombuffer(decompressed_frame, dtype=np.uint8), cv2.IMREAD_COLOR)
            cv2.imshow("Video Stream", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cv2.destroyAllWindows()

# Run the client
if __name__ == "__main__":
    asyncio.run(display_frames())