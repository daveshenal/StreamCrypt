import asyncio
import numpy as np
import websockets
import cv2
import os
import firebase_admin
from dotenv import load_dotenv
from firebase_admin import credentials, db
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes

from core.encryption import decrypt_data_with_key
from core.compression import decompress_data

# Load environment variables from .env
load_dotenv()

# -------------------- Firebase --------------------

# Load Firebase credentials
cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': os.getenv("FIREBASE_DATABASE_URL")
})

# -------------------- Get ngrok Public URL --------------------

def fetch_ngrok_key():
    # Fetch the ngrok URL from Firebase
    ref = db.reference("server/ngrok_url")  # Path where the URL is stored in Firebase
    ngrok_url = ref.get()
    print("Receved ngrok URL from Firebase")
    return ngrok_url

NGROK_URL = fetch_ngrok_key()

print(NGROK_URL)

# -------------------- RSA --------------------

# Fetch the RSA public key from the server
async def fetch_public_key():
    ws_url = NGROK_URL.replace("https://", "wss://").rstrip("/") + "/get-public-key"
    async with websockets.connect(ws_url) as websocket:
        public_key_pem = await websocket.recv()
        return serialization.load_pem_public_key(public_key_pem)

# Encrypt data using RSA
def encrypt_with_rsa(public_key, data):
    return public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )


# -------------------- Watch Stream --------------------

async def receive_video_stream():
    print("Connecting to WebSocket server...")
    public_key = await fetch_public_key()
    
    # Generate a random ChaCha20 key
    symmetric_key = os.urandom(32)

    # Encrypt the symmetric key using RSA
    encrypted_key = encrypt_with_rsa(public_key, symmetric_key)
    
    ws_url = NGROK_URL.replace("https://", "wss://").rstrip("/") + "/stream"
    async with websockets.connect(ws_url) as websocket:
        # Send the encrypted ChaCha20 key
        await websocket.send(encrypted_key)
        
        print("Successfully connected to WebSocket server")
        

        while True:
            encrypted_frame = await websocket.recv()
            decrypted_frame = decrypt_data_with_key(encrypted_frame, symmetric_key)
            frame_data = decompress_data(decrypted_frame)

            # Decode and display
            nparr = np.frombuffer(frame_data, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            cv2.imshow("Video Stream", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()

if __name__ == "__main__":
    asyncio.run(receive_video_stream())