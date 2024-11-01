#!/bin/bash

# Update Homebrew and install dependencies
brew update
brew install wget

# Download and install TA-Lib
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
tar -xzf ta-lib-0.4.0-src.tar.gz
cd ta-lib
./configure --prefix=/usr/local
make
sudo make install

# Clean up
cd ..
rm -rf ta-lib ta-lib-0.4.0-src.tar.gz
