#!/bin/bash

# It is recommended to use the same version of liboqs and liboqs-python

# Install liboqs 

# Releases repositories
export LIBOQS_TAG=0.10.0
export LIBOQS_PYTHON_TAG=0.10.0

# Dependencies
sudo apt update -y
sudo apt install -y build-essential git cmake libssl-dev wget unzip python3 python3-venv pip

# Clone the repository liboqs
git clone --depth=1 --branch ${LIBOQS_TAG} https://github.com/open-quantum-safe/liboqs


# Sets the source and build directories 
# -DBUILD_SHARED_LIBS=ON
# Can be set to ON or OFF. When ON, liboqs is built as a shared library.
# Default: OFF.
# This means liboqs is built as a static library by default.
cmake -S liboqs -B liboqs/build -DBUILD_SHARED_LIBS=ON


# Build (--parellel optional)
cmake --build liboqs/build --parallel 8

# Install
sudo cmake --build liboqs/build --target install


# Install liboqs-python
# You may need to set the LD_LIBRARY_PATH, environment variable to point to the path to liboqs library directory

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib


# Create virtual environment 
python3 -m venv venv
source venv/bin/activate
python3 -m ensurepip --upgrade
pip install -r requirements.txt

# Clone the repository
# Configure and install the wrapper

git clone --depth=1 --branch ${LIBOQS_PYTHON_TAG} https://github.com/open-quantum-safe/liboqs-python
cd liboqs-python
pip install .

# Run the examples
# python3 liboqs-python/examples/kem.py
# python3 liboqs-python/examples/sig.py
# python3 liboqs-python/examples/rand.py

