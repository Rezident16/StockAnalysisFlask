#!/usr/bin/env bash
set -o errexit  # Exit on error

# Install TA-Lib C library
apt-get update && apt-get install -y ta-lib

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
export LD_LIBRARY_PATH=$INSTALL_DIR/lib:$LD_LIBRARY_PATH

# Install Python dependencies
pip install -r requirements.txt
