# 🔐 StreamCrypt: Secure Real-Time Video Streaming Pipeline

StreamCrypt is a modular, learning-focused project that demonstrates how to build a **secure, real-time video streaming pipeline** in Python. It features:

- 📹 Real-time video capture and streaming
- 🔒 End-to-end encryption (ChaCha20, RSA)
- 📦 Fast compression (LZ4)
- 🌐 Optional [ngrok](https://ngrok.com/) tunneling for secure remote access
- 🧩 Modular design for easy experimentation and learning

---

## Table of Contents

- [Project Structure](#project-structure)
- [Features](#features)
- [How It Works](#how-it-works)
- [Setup & Installation](#setup--installation)
- [Usage](#usage)
  - [Base Version (Local)](#base-version-local)
  - [Final Version (With Firebase/ngrok)](#final-version-with-firebase-ngrok)
  - [Ngrok Standalone](#ngrok-standalone)
- [Configuration](#configuration)
- [Core Modules](#core-modules)
- [Notebooks & Demos](#notebooks--demos)
- [Learning Goals](#learning-goals)
- [References](#references)

---

## Project Structure

```
StreamCrypt/
├── base_version/   # Minimal, local-only streaming (no remote/Firebase)
├── configs/        # Configuration files (YAML)
├── core/           # Core modules: encryption, compression, video processing
├── final/          # Full-featured version (ngrok, Firebase, RSA, etc.)
├── ngrok/          # Standalone ngrok-based streaming
├── notebooks/      # Jupyter notebooks for demos and experiments
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Features

- **Real-Time Video Streaming:** Capture and stream webcam video with low latency.
- **Encryption:** Uses ChaCha20-Poly1305 for fast symmetric encryption, with optional RSA for key exchange.
- **Compression:** LZ4 for efficient, fast frame compression.
- **Remote Access:** Securely stream video over the internet using ngrok tunnels.
- **Firebase Integration:** Share ngrok URLs and manage signaling for remote clients.
- **Modular Design:** Swap out or extend components for learning and experimentation.

---

## How It Works

1. **Server** captures video frames, compresses and encrypts them, and streams them over a WebSocket.
2. **Client** connects to the server, receives encrypted frames, decrypts and decompresses them, and displays the video.
3. **ngrok** (optional) exposes the local server to the internet for remote access.
4. **Firebase** (optional, in `final/`) is used to share the ngrok URL between server and client.

---

## Setup & Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/StreamCrypt.git
   cd StreamCrypt
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Generate encryption keys and config:**

   ```bash
   python core/generate_key.py
   ```

4. **(Optional) Set up ngrok and Firebase:**
   - Install [ngrok](https://ngrok.com/download)
   - Set up a Firebase project and download `credentials.json` to the project root.
   - Create a `.env` file with your Firebase database URL.

---

## Usage

### Base Version (Local)

- **Start the server:**
  ```bash
  python base_version/server.py
  ```
- **Start the client:**
  ```bash
  python base_version/client.py
  ```

### Ngrok Standalone

- **Start the server:**
  ```bash
  python ngrok/server.py
  ```
- **Start the client:**
  ```bash
  python ngrok/client.py
  ```

### Final Version (With Firebase/ngrok)

- **Start the server (exposes via ngrok, uploads URL to Firebase):**
  ```bash
  python final/server.py
  ```
- **Start the client (fetches ngrok URL from Firebase):**
  ```bash
  python final/client.py
  ```

---

## Configuration

Edit `configs/config.yaml` to set encryption parameters. Example:

```yaml
encryption:
  key_b64: <base64-encoded-key>
  nonce_size: 12
```

Generate a new key with:

```bash
python core/generate_key.py
```

---

## Core Modules

- `core/encryption.py` – ChaCha20-Poly1305 encryption/decryption, config loading
- `core/compression.py` – LZ4 compression/decompression
- `core/vid_process.py` – Video frame processing and JPEG encoding
- `core/streaming.py` – Async video stream receiver (client-side)
- `core/generate_key.py` – Utility to generate and save encryption keys

---

## Notebooks & Demos

- `notebooks/encryption_demo.ipynb` – Interactive demo of encryption and compression modules.

---

## Learning Goals

- Understand secure, real-time data streaming
- Learn about symmetric and asymmetric encryption in practice
- Explore fast data compression for media
- Experiment with remote access and signaling (ngrok, Firebase)
- Modularize and extend a Python project for experimentation

---

## References

- [Python Cryptography](https://cryptography.io/en/latest/)
- [LZ4 Compression](https://python-lz4.readthedocs.io/en/stable/quickstart.html)
- [ngrok](https://ngrok.com/)
- [Firebase Admin SDK](https://firebase.google.com/docs/admin/setup)
- [OpenCV](https://opencv.org/)

---

**Note:** This project is for educational purposes and is not production-hardened. Use responsibly!
