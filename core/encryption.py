import base64
import yaml
import os
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305

# Load config
with open("configs/config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Decode key from base64
ENCRYPTION_KEY = base64.b64decode(config["encryption"]["key_b64"])
NONCE_SIZE = config["encryption"]["nonce_size"]

# Function to encrypt data using ChaCha20-Poly1305
def encrypt_data(data: bytes, encryption_key: bytes) -> bytes:
    nonce = os.urandom(NONCE_SIZE)
    cipher = ChaCha20Poly1305(encryption_key)
    encrypted_data = cipher.encrypt(nonce, data, None)  # None - associated data
    return nonce + encrypted_data

# Function to decrypt data using ChaCha20-Poly1305
def decrypt_data(encrypted_data: bytes) -> bytes:
    nonce = encrypted_data[:NONCE_SIZE]  # Extract nonce
    ciphertext = encrypted_data[NONCE_SIZE:]  # Extract ciphertext
    cipher = ChaCha20Poly1305(ENCRYPTION_KEY)
    return cipher.decrypt(nonce, ciphertext, None)  # None for associated data


# =========== FOR HYBRID ENCRYPTION ===========

# Function to encrypt data using ChaCha20-Poly1305
def encrypt_data_with_key(data: bytes, encryption_key: bytes) -> bytes:
    nonce = os.urandom(NONCE_SIZE)
    cipher = ChaCha20Poly1305(encryption_key)
    encrypted_data = cipher.encrypt(nonce, data, None)  # None - associated data
    return nonce + encrypted_data

# Function to decrypt data using ChaCha20-Poly1305
def decrypt_data_with_key(encrypted_data, decryption_key):
    nonce = encrypted_data[:12]
    encrypted_content = encrypted_data[12:]
    cipher = ChaCha20Poly1305(decryption_key)
    return cipher.decrypt(nonce, encrypted_content, None)


