import os
import base64

key = os.urandom(32)  # Exactly 32 bytes
key_b64 = base64.b64encode(key).decode()

print("Put this in config.yaml:")
print(f"key_b64: \"{key_b64}\"")