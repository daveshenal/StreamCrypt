# Recommendation:
# For development & local testing: Run directly on your host machine (pip install -r requirements.txt).

# Docker is supported but primarily intended for deployment scenarios or headless operation. 
# For local development with a webcam, running directly on your host machine is recommended

# On Windows, webcam passthrough in Docker requires WSL2 and USB/IP setup.

# Use lightweight Python base image
FROM python:3.11-slim

# Prevent .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies for OpenCV, LZ4, etc.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       libgl1 \
       libglib2.0-0 \
       liblz4-dev \
       ffmpeg \
       wget \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Create ngrok directory (optional)
RUN mkdir -p /ngrok

# Expose default streaming port
EXPOSE 8000

# Default: run the base server
CMD ["python", "base_version/server.py"]
