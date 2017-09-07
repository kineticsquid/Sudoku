#!/bin/bash
echo "hello, $USER. testing now..."

# Now update the action at Bluemix, also creates the action if it doesn't exist
bx api https://api.ng.bluemix.net
bx plugin install Cloud-Functions -r Bluemix
# bx login --apikey ${WSK_AUTH}
# bx target -o ${CF_ORG} -s ${CF_SPACE}
# bx wsk action update return_environment ./Miscellaneous.zip --kind python:3

bx wsk action invoke return_environment --blocking --result --param name Fred
echo ""

bx wsk action invoke return_environment --blocking --result
echo ""





