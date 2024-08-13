# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install Redis (necessary for running the Redis server inside the container)
RUN apt-get update && apt-get install -y redis-server

# Expose port 5000 for Flask and port 6379 for Redis
EXPOSE 5000 6379

# Copy the entrypoint script to the working directory
COPY entrypoint.sh /app/entrypoint.sh

# Make the entrypoint script executable
RUN chmod +x /app/entrypoint.sh

# Run the entrypoint script
CMD ["/app/entrypoint.sh"]
