#!/bin/bash
echo "Building and deploying now..."

# IF CF_ORG is not defined, this is not running as part of a DevOps Pipeline in Bluemix, so set these values
if [[ -z "${CF_ORG}" ]]; then
  export CF_ORG='kellrman@us.ibm.com'
  export CF_SPACE='dev'
  export WSK_AUTH='7vZob_7TCakks64OV9C4aJxBD9FPscVf1rdoSHdJazs5'
fi

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
bx wsk package update utils
bx wsk action update utils/environment ./Miscellaneous.zip --kind python:3 --web true
rm Miscellaneous.zip

# Now list the package and action to confirm results
bx wsk package get utils

# Define API - do this once only because there is no update, ony create and delete
# bx wsk property set --apihost openwhisk.ng.bluemix.net
# bx wsk api create /environment get /utils/environment --response-type json