FROM debian:stretch-slim

# Use an official Python runtime as the base image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the necessary dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port for the websocket listener
EXPOSE 8000

# Run the websocket listener script
CMD ["python", "main.py"]

