#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status
set -x  # Print commands and their arguments as they are executed

# Update Homebrew and install dependencies
echo "Updating Homebrew..."
brew update
echo "Installing wget..."
brew install wget

# Download and install TA-Lib
echo "Downloading TA-Lib..."
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
echo "Extracting TA-Lib..."
tar -xzf ta-lib-0.4.0-src.tar.gz
cd ta-lib
echo "Configuring TA-Lib..."
./configure --prefix=/usr/local
echo "Building TA-Lib..."
make
echo "Installing TA-Lib..."
sudo make install

# Verify installation
echo "Verifying TA-Lib installation..."
ls -l /usr/local/include/ta-lib
ls -l /usr/local/lib

# Clean up
echo "Cleaning up..."
cd ..
rm -rf ta-lib ta-lib-0.4.0-src.tar.gz

echo "TA-Lib installation completed."

# Install Python dependencies
pip install -r requirements.txt
