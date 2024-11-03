# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    gcc \
    libffi-dev \
    libssl-dev \
    python3-dev \
    && apt-get clean

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

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python dependencies in smaller groups
RUN pip install --no-cache-dir flask==2.3.3 python-dateutil==2.9.0.post0 alpaca-py python-dotenv==1.0.1
RUN pip install --no-cache-dir numpy==1.23.2 pandas==2.2.3
RUN pip install --no-cache-dir TA-Lib==0.4.32

# Run pip check to identify any issues
RUN pip check

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV PORT=5000

# Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]



# RUN pip install --no-cache-dir aiohappyeyeballs==2.4.3 aiohttp==3.8.1 aiosignal==1.3.1
# RUN pip install --no-cache-dir async-timeout==4.0.3 attrs==24.2.0
# RUN pip install --no-cache-dir blinker==1.8.2 certifi==2024.8.30 charset-normalizer==2.1.1
# RUN pip install --no-cache-dir frozenlist==1.5.0 idna==3.10 importlib-metadata==8.5.0
# RUN pip install --no-cache-dir itsdangerous==2.2.0 jinja2==3.1.4 MarkupSafe==3.0.2
# RUN pip install --no-cache-dir msgpack==1.0.3 multidict==6.1.0 numpy==1.25.2
# RUN pip install --no-cache-dir packaging==24.1 pandas==2.2.3 propcache==0.2.0
# RUN pip install --no-cache-dir pytz==2024.2
# RUN pip install --no-cache-dir PyYAML==6.0 requests==2.32.3 six==1.16.0
# RUN pip install --no-cache-dir typing-extensions==4.12.2 tzdata==2024.2
# RUN pip install --no-cache-dir urllib3==1.26.20 websocket-client==1.8.0 websockets==10.4
# RUN pip install --no-cache-dir werkzeug==2.3.7 yarl==1.17.1 zipp==3.20.2 click==8.1.7 deprecation==2.1.0 

