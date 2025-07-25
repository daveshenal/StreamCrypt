import cv2
import websockets
import numpy as np

from core.encryption import decrypt_data
from core.compression import decompress_data

async def watch_stream(uri):
    async with websockets.connect(uri) as websocket:
        print("Successfully connected to WebSocket server")
        print("Starting video stream... (Press 'q' to quit)")

        while True:
            try:
                # Receive the encrypted frame from the server
                encrypted_frame = await websocket.recv()
                decrypted_frame = decrypt_data(encrypted_frame)
                decompressed_frame = decompress_data(decrypted_frame)
                frame = cv2.imdecode(np.frombuffer(decompressed_frame, dtype=np.uint8), cv2.IMREAD_COLOR)
                    
                cv2.imshow("Video Stream", frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                        
            except websockets.exceptions.ConnectionClosed:
                print("Error: Connection to server lost")
                break
            except Exception as e:
                print(f"Error: Error receiving frame: {e}")
                break