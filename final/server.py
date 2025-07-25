'''
References:

1. RSA - Private and Public kay
    https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/

2. Cryptography - Encryption:
    https://cryptography.io/en/latest/hazmat/primitives/aead/

3. lZ4 - Compression:
    https://python-lz4.readthedocs.io/en/stable/quickstart.html

'''

import asyncio
import cv2
import os
import logging
import uvicorn
import firebase_admin
from pyngrok import ngrok
from dotenv import load_dotenv
from firebase_admin import credentials, db
from fastapi.websockets import WebSocketState
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

from core.encryption import encrypt_data_with_key
from core.compression import compress_data
from core.vid_process import process_video_frame

# Load environment variables from .env
load_dotenv()

app = FastAPI()
logger = logging.getLogger("uvicorn")

# -------------------- Firebase --------------------

# Load Firebase credentials
cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': os.getenv("FIREBASE_DATABASE_URL")
})

# -------------------- ngrok --------------------

# Upload ngrok URL to Firebase
def upload_ngrok_url():
    # Start ngrok
    public_url = ngrok.connect(8000).public_url
    print(f"[ngrok] Tunnel opened: {public_url}")
    
    ref = db.reference("server/ngrok_url")
    ref.set(public_url)
    print("[ngrok] Uploaded ngrok URL to Firebase")

# -------------------- RSA --------------------

# Generate RSA Key Pair (Done once and stored securely)
RSA_PRIVATE_KEY = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)
RSA_PUBLIC_KEY = RSA_PRIVATE_KEY.public_key()

# Serialize Public Key
PUBLIC_KEY_PEM = RSA_PUBLIC_KEY.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)


# -------------------- End Points --------------------

# WebSocket endpoint to send the public key
@app.websocket("/get-public-key")
async def get_public_key(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_bytes(PUBLIC_KEY_PEM)
    await websocket.close()
    
# WebSocket endpoint to receive the encrypted ChaCha20 key and start video streaming
@app.websocket("/stream")
async def websocket_video_stream(websocket: WebSocket):
    await websocket.accept()
    logger.info("Client connected via WebSocket")

    # Receive the Encrypted Symmetric Key
    encrypted_key = await websocket.receive_bytes()

    try:
        # Decrypt the Symmetric Key using RSA Private Key
        encryption_key = RSA_PRIVATE_KEY.decrypt(
            encrypted_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        logger.info("Symmetric key successfully decrypted.")

        camera = cv2.VideoCapture(0)
        if not camera.isOpened():
            await websocket.close(code=1008, reason="Camera not available")
            return

        # Stream Encrypted Video Data
        try:
            while True:
                success, frame = camera.read()
                if not success:
                    break

                # Compress and encrypt the frame
                processed_frame = process_video_frame(frame)
                compressed_frame = compress_data(processed_frame)
                encrypted_frame = encrypt_data_with_key(compressed_frame, encryption_key)

                # if WebSocket connection is still open
                if websocket.application_state == WebSocketState.CONNECTED:
                    await websocket.send_bytes(encrypted_frame)
                    await asyncio.sleep(0.03)

        except WebSocketDisconnect:
            logger.info("Web Client disconnected.")
        except Exception as e:
            logger.error(f"Error during WebSocket communication: {e}")

    finally:
        camera.release()
        if websocket.application_state == WebSocketState.CONNECTED:
            await websocket.close()

# -------------------- Run the app --------------------
if __name__ == "__main__":
    upload_ngrok_url()
    uvicorn.run(app, host="0.0.0.0", port=8000)