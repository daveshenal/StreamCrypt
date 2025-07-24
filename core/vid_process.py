import cv2

# Video compression levels based on battery status
VIDEO_COMPRESSION_LEVELS = {
    'l': 10,  # High compression (low quality)
    'm': 30,  # Medium compression
    'f': 80,  # Low compression (high quality)
}

# Function to process video frames based on battery level
def process_video_frame(frame, battery_level: chr='l'):
    compression_level = VIDEO_COMPRESSION_LEVELS.get(battery_level, 50)  # Default to medium
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), compression_level]
    _, buffer = cv2.imencode(".jpg", frame, encode_param)
    return buffer.tobytes()