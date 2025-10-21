# Use a specific, stable base image and specify the platform
FROM --platform=linux/amd64 python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies, including fonts for multilingual support (e.g., Japanese CJK)
# This is crucial for handling multilingual PDFs correctly.
RUN apt-get update && \
    apt-get install -y --no-install-recommends fonts-noto-cjk fonts-freefont-ttf && \
    rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application script into the container
COPY process_pdfs.py .

# Create input/output directories as specified by the hackathon run command
RUN mkdir -p /app/input /app/output

# Set the command to run the script when the container starts
CMD ["python", "process_pdfs.py"]