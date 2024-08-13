# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the image to the container
COPY Class\ Diagram.png /app/Class\ Diagram.png

# Expose port 8080
EXPOSE 8080

# Run a simple HTTP server to serve the image
CMD ["python", "-m", "http.server", "8080"]
