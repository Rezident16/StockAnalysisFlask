# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt and install Python dependencies first
COPY requirements.txt requirements.txt

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    wget \
    gcc \
    libffi-dev \
    libssl-dev \
    python3-dev && \
    rm -rf /var/lib/apt/lists/*

# Define the installation directory
ENV INSTALL_DIR=/usr/local

# Download and install TA-Lib
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
    tar -xzf ta-lib-0.4.0-src.tar.gz && \
    cd ta-lib && \
    wget -O config.guess 'http://savannah.gnu.org/cgi-bin/viewcvs/*checkout*/config/config/config.guess' && \
    wget -O config.sub 'http://savannah.gnu.org/cgi-bin/viewcvs/*checkout*/config/config/config.sub' && \
    ./configure --prefix=/usr --build=aarch64-unknown-linux-gnu && \
    make && \
    make install && \
    cd .. && \
    rm -rf ta-lib ta-lib-0.4.0-src.tar.gz

# Set environment variables to use the installed TA-Lib
ENV CFLAGS="-I$INSTALL_DIR/include"
ENV LDFLAGS="-L$INSTALL_DIR/lib"
ENV LD_LIBRARY_PATH="$INSTALL_DIR/lib"

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    pip check

# Copy the entire application code
COPY . /app

# Expose the port
EXPOSE 5000

# Define environment variable
ENV PORT=5000

# Run app.py when the container launches with specified workers
CMD exec gunicorn -b 0.0.0.0:$PORT app:ap
