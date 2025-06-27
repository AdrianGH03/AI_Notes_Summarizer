# This Dockerfile sets up the environment for the AI notes summarizer application.
# It uses a Python base image, installs the necessary dependencies, and sets the working directory.

FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code into the container
COPY src/ .

# Command to run the application
CMD ["python", "main.py"]