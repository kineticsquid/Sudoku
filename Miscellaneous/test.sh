#!/bin/bash
echo "hello, $USER. testing now..."
echo "run bx wsk activation poll to poll for log results"

# Now update the action at Bluemix, also creates the action if it doesn't exist
bx api https://api.ng.bluemix.net
bx wsk action invoke utils/environment --blocking --result --param name "[1,2]"
bx wsk action invoke utils/environment --blocking --result





