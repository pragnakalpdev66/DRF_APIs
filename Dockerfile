# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libopenjp2-7-dev \
    libtiff5-dev \
    tk-dev \
    tcl-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY drf_requirements.txt websocket_requirement.txt /app/
RUN pip install --no-cache-dir -r drf_requirements.txt && \
    pip install --no-cache-dir -r websocket_requirement.txt

# Copy project
COPY . /app/

# Set work directory to the django project root
WORKDIR /app/core

# Expose port 8000
EXPOSE 8000

# Use daphne as the ASGI server
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "core.asgi:application"]
