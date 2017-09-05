#!/bin/bash

# Build the Python runtime
../build_virtualenv.sh

# Zip up the files
cp return_environment.py __main__.py
zip -r Miscellaneous.zip virtualenv __main__.py ../AppExceptions.py
rm __main__.py

# Create/Update this action
bx wsk action update return_environment ./Miscellaneous/return_environment.py
echo ""

# List current actions
wsk action list
echo ""

# Now testing the deployment
./test.sh



