import asyncio
import cv2
from fastapi.websockets import WebSocketState
import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from core.encryption import encrypt_data
from core.compression import compress_data
from core.vid_process import process_video_frame

# Initialize FastAPI app
app = FastAPI()

# Setup logging
logger = logging.getLogger("uvicorn")

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
    uvicorn.run(app, host="0.0.0.0", port=8000)