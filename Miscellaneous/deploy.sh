#!/bin/bash

# Create virtual python runtime with dependencies
sudo pip install virtualenv
virtualenv virtualenv
source virtualenv/bin/activate
pip install -r ../requirements.txt

# Now zip this up with action code and other pre-req code from this project
cp return_environment.py __main__.py
zip -r Miscellaneous.zip __main__.py
zip -r Miscellaneous.zip ../AppExceptions.py
zip -r Miscellaneous.zip virtualenv
rm __main__.py

# Now update the action at Bluemix, also creates the action if it doesn't exist
bx api https://api.ng.bluemix.net
bx plugin install Cloud-Functions -r Bluemix
bx login --apikey ${WSK_AUTH}
bx target -o ${CF_ORG} -s ${CF_SPACE}
bx wsk action update return_environment ./Miscellaneous.zip --kind python:3



