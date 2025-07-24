import base64
import yaml
import os
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
import lz4.frame

# Load config
with open("configs/config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Decode key from base64
ENCRYPTION_KEY = base64.b64decode(config["encryption"]["key_b64"])
NONCE_SIZE = config["encryption"]["nonce_size"]

# Encrypt function
def encrypt_data(data: bytes) -> bytes:
    nonce = os.urandom(NONCE_SIZE)
    cipher = ChaCha20Poly1305(ENCRYPTION_KEY)
    encrypted_data = cipher.encrypt(nonce, data, None)
    return nonce + encrypted_data

# Function to decrypt data using ChaCha20-Poly1305
def decrypt_data(encrypted_data: bytes) -> bytes:
    nonce = encrypted_data[:NONCE_SIZE]  # Extract nonce
    ciphertext = encrypted_data[NONCE_SIZE:]  # Extract ciphertext
    cipher = ChaCha20Poly1305(ENCRYPTION_KEY)
    return cipher.decrypt(nonce, ciphertext, None)  # None for associated data

