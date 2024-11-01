#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status
set -x  # Print commands and their arguments as they are executed

# Update package list and install dependencies
apt-get update
apt-get install -y build-essential wget

# Download and install TA-Lib
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
tar -xzf ta-lib-0.4.0-src.tar.gz
cd ta-lib
./configure --prefix=/usr
make
make install

# Clean up
cd ..
rm -rf ta-lib ta-lib-0.4.0-src.tar.gz

# Install Python dependencies
pip install -r requirements.txt
