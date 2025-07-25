import cv2
import asyncio

from core.streaming import watch_stream

# Function to display frames
async def display_frames(server_url=None):
    # Default to local server, but allow override for ngrok URL
    if server_url is None:
        uri = "ws://localhost:8000/stream"
    else:
        # Ensure the URL has the /stream endpoint
        if not server_url.endswith('/stream'):
            uri = f"{server_url}/stream"
        else:
            uri = server_url
    
    print(f"Connecting to: {uri}")
    
    try:
        await watch_stream(uri)

    except Exception as e:
        print(f"Error: Failed to connect to server: {e}")
        print("Make sure the server is running and the URL is correct")
    
    cv2.destroyAllWindows()


def get_server_url():
    """Get server URL from user input"""
    print("\nVideo Stream Client")
    print("=" * 30)
    print("1. Connect to local server (localhost:8000)")
    print("2. Connect to ngrok URL")
    
    choice = input("\nEnter your choice (1 or 2): ").strip()
    
    if choice == "1":
        return None  # Use default local URL
    elif choice == "2":
        ngrok_url = input("Enter your ngrok WebSocket URL (e.g., wss://abc123.ngrok.app): ").strip()
        
        # Validate and clean the URL
        if not ngrok_url.startswith(('ws://', 'wss://')):
            print("Error: URL must start with ws:// or wss://")
            return get_server_url()
        
        return ngrok_url
    else:
        print("Error: Invalid choice. Please enter 1 or 2.")
        return get_server_url()

# Run the client
if __name__ == "__main__":
    try:
        server_url = get_server_url()
        asyncio.run(display_frames(server_url))
    except KeyboardInterrupt:
        print("\nClient stopped by user")
    except Exception as e:
        print(f"Error: Client error: {e}")
    finally:
        cv2.destroyAllWindows()