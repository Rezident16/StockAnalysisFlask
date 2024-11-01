#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status
set -x  # Print commands and their arguments as they are executed

# Define the installation directory
INSTALL_DIR=$HOME/ta-lib

# Download and install TA-Lib
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
tar -xzf ta-lib-0.4.0-src.tar.gz
cd ta-lib
./configure --prefix=$INSTALL_DIR
make
make install

# Clean up
cd ..
rm -rf ta-lib ta-lib-0.4.0-src.tar.gz

# Set environment variables to use the installed TA-Lib
export CFLAGS="-I$INSTALL_DIR/include"
export LDFLAGS="-L$INSTALL_DIR/lib"

# Install Python dependencies
pip install -r requirements.txt
