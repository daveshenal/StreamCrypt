import lz4.frame

# Function to compress data using LZ4
def compress_data(data: bytes) -> bytes:
    return lz4.frame.compress(data)

# Function to decompress data using LZ4
def decompress_data(compressed_data: bytes) -> bytes:
    return lz4.frame.decompress(compressed_data)

