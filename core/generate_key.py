import os
import base64
import yaml

# Generate a random 32-byte key
key = os.urandom(32)
key_b64 = base64.b64encode(key).decode()

# Config dictionary
config_data = {
    'encryption': {
        'key_b64': key_b64,
        'nonce_size': 12
    }
}

# Path to config.yaml
config_path = 'configs/config.yaml'

# Create configs folder if it doesn't exist
os.makedirs('configs', exist_ok=True)

# Write config_data to YAML file
with open(config_path, 'w') as f:
    yaml.dump(config_data, f)

print(f"Config saved to {config_path} with key_b64: {key_b64}")