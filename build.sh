#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status
set -x  # Print commands and their arguments as they are executed

# Install dependencies using wget and tar
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
