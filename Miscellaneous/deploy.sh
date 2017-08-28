#!/bin/bash
echo "listing files in the current directory, $PWD:"
ls  # list files
echo ""
echo "listing current environment:"
printenv
echo ""
echo "hello, $USER. Deploying now..."
# Get the OpenWhisk CLI
mkdir ~/wsk
curl https://openwhisk.ng.bluemix.net/cli/go/download/linux/amd64/wsk > ~/wsk/wsk
chmod +x ~/wsk/wsk
export PATH=$PATH:~/wsk

# Configure the OpenWhisk CLI
wsk property set --apihost openwhisk.ng.bluemix.net --auth "${WSK_AUTH}" --namespace "${CF_ORG}_${CF_SPACE}"
echo ""

# Create/Update this action
wsk action update return_environment ./Miscellaneous/return_environment.py
echo ""

# List current actions
wsk action list
echo ""

# Now testing the deployment
./Miscellaneous/test.sh



