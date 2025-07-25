import cv2
import asyncio

from core.streaming import watch_stream

# Function to display frames
async def display_frames():
    print("Connecting to WebSocket server...")
    uri = "ws://localhost:8000/stream"  # WebSocket server URI
    
    try:
        await watch_stream(uri)

    except Exception as e:
        print(f"Error: Failed to connect to server: {e}")
        print("Make sure the server is running and the URL is correct")

    cv2.destroyAllWindows()

# Run the client
if __name__ == "__main__":
    asyncio.run(display_frames())