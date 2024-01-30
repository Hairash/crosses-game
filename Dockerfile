# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Install the necessary libraries
RUN apt-get update && apt-get install -y \
  libglib2.0-0 \
  libsm6 \
  libxext6 \
  libxrender-dev \
  libgl1-mesa-glx \
  && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the .tar.gz file into the container
COPY dist/croco-game-1.0.0.tar.gz .

# Install your application
RUN pip install croco-game-1.0.0.tar.gz

# Run your application
CMD ["croco-game"]
