import asyncio
import cv2
from fastapi.websockets import WebSocketState
import logging
import subprocess
import requests
import time
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from contextlib import asynccontextmanager

from core.encryption import encrypt_data
from core.compression import compress_data
from core.vid_process import process_video_frame

# Initialize FastAPI app with lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    start_ngrok_tunnel(8000)
    yield
    # Shutdown logic
    stop_ngrok_tunnel()

app = FastAPI(lifespan=lifespan)
logger = logging.getLogger("uvicorn")

# ngrok configuration
NGROK_PROCESS = None
NGROK_PUBLIC_URL = None

def start_ngrok_tunnel(port=8000):
    """Start ngrok tunnel and return the public URL"""
    global NGROK_PROCESS, NGROK_PUBLIC_URL
    
    try:
        # Start ngrok process
        logger.info("Starting ngrok tunnel...")
        NGROK_PROCESS = subprocess.Popen(
            ['ngrok', 'http', str(port)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait a bit for ngrok to start
        time.sleep(3)
        
        # Get the public URL from ngrok API
        try:
            response = requests.get('http://localhost:4040/api/tunnels')
            tunnels = response.json()['tunnels']
            
            if tunnels:
                public_url = tunnels[0]['public_url']
                # Convert http to ws for WebSocket
                NGROK_PUBLIC_URL = public_url.replace('http://', 'ws://').replace('https://', 'wss://')
                logger.info(f"ngrok tunnel established: {public_url}")
                logger.info(f"WebSocket URL: {NGROK_PUBLIC_URL}/stream")
                return NGROK_PUBLIC_URL
            else:
                logger.error("No ngrok tunnels found")
                return None
                
        except Exception as e:
            logger.error(f"Failed to get ngrok URL: {e}")
            return None
            
    except FileNotFoundError:
        logger.error("ngrok not found. Please install ngrok first.")
        return None
    except Exception as e:
        logger.error(f"Failed to start ngrok: {e}")
        return None

def stop_ngrok_tunnel():
    """Stop the ngrok tunnel"""
    global NGROK_PROCESS
    if NGROK_PROCESS:
        logger.info("Stopping ngrok tunnel...")
        NGROK_PROCESS.terminate()
        NGROK_PROCESS = None

# WebSocket endpoint to stream processed video frames
@app.websocket("/stream")
async def websocket_video_stream(websocket: WebSocket):
    await websocket.accept()
    logger.info("Client connected via WebSocket")

    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        await websocket.close(code=1008, reason="Camera not available")
        return

    try:
        while True:
            success, frame = camera.read()
            if not success:
                break

            # compress and encrypt
            processed_frame = process_video_frame(frame)
            compressed_frame = compress_data(processed_frame)
            encrypted_frame = encrypt_data(compressed_frame)

            # if the WebSocket connection is still open
            if websocket.application_state == WebSocketState.CONNECTED:
                await websocket.send_bytes(encrypted_frame)
                await asyncio.sleep(0.03)

    except WebSocketDisconnect:
        logger.info("Web Client disconnected.")
    except Exception as e:
        logger.error(f"Error during WebSocket communication: {e}")
    finally:
        camera.release()
        # close the WebSocket connection safely
        if websocket.application_state == WebSocketState.CONNECTED:
            await websocket.close()

# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    
    try:
        # Start ngrok tunnel
        ngrok_url = start_ngrok_tunnel(8000)
        if ngrok_url:
            print(f"\nServer will be accessible via ngrok at: {ngrok_url}/stream")
            print("Copy this URL to use in your client!")
        
        # Start the server
        uvicorn.run(app, host="0.0.0.0", port=8000)
        
    except KeyboardInterrupt:
        logger.info("Server interrupted by user")
    finally:
        stop_ngrok_tunnel()