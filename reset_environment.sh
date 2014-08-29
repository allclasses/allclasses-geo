#!/bin/bash

# Reset virtualenv and compiled python
rm -rf virtualenv

rm -f *.pyc
find . -name '*.pyc' -delete

virtualenv virtualenv

# Make sure we have wheel-compatible versions of pip etc.
virtualenv/bin/pip install --upgrade setuptools==1.4 pip==1.5 wheel

# Generate wheels
virtualenv/bin/pip wheel  -w /usr/local/wheels -f file:///usr/local/wheels/ -r requirements.txt

# Install from wheels
virtualenv/bin/pip install -f file:///usr/local/wheels -r requirements.txt
