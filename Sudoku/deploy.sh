#!/bin/bash
echo "Building and deploying now..."

# IF CF_ORG is not defined, this is not running as part of a DevOps Pipeline in Bluemix, so set these values
if [[ -z "${CF_ORG}" ]]; then
  export CF_ORG='kellrman@us.ibm.com'
  export CF_SPACE='dev'
  export WSK_AUTH='7vZob_7TCakks64OV9C4aJxBD9FPscVf1rdoSHdJazs5'
else
  bx plugin install Cloud-Functions -r Bluemix
fi

# Create virtual python runtime with dependencies
sudo pip install virtualenv
virtualenv virtualenv
source virtualenv/bin/activate
pip install -r ../requirements.txt

# Zip this up with action code for receive and other pre-req code from this project
cp twilio_receive.py __main__.py
zip -r receive.zip __main__.py
zip -r receive.zip ../AppExceptions.py
zip -r receive.zip virtualenv
rm __main__.py

# Zip this up with action code for send and other pre-req code from this project
cp twilio_send.py __main__.py
zip -r send.zip __main__.py
zip -r send.zip ../AppExceptions.py
zip -r send.zip virtualenv
rm __main__.py

# Create zip file for the solver action
cp SudokuSolver.py __main__.py
zip -r solve.zip __main__.py
zip -r solve.zip ../AppExceptions.py
rm __main__.py

# Authenticate to Bluemix and set the target org and space
bx api https://api.ng.bluemix.net
bx login --apikey ${WSK_AUTH}
bx target -o ${CF_ORG} -s ${CF_SPACE}

# Update the package (create it if it doesn't exist)
bx wsk package update sudoku

# Update the actions
bx wsk action update sudoku/twilio_receive ./receive.zip --kind python:3 --web true
rm receive.zip
bx wsk action update sudoku/twilio_send ./send.zip --kind python:3 --web true
rm send.zip
bx wsk action update sudoku/solve ./solve.zip --kind python:3 --web true
rm solve.zip

bx wsk action update sudoku/sudoku_solve --sequence sudoku/twilio_receive,sudoku/solve,sudoku/twilio_send

# Define API - do this once only because there is no update, ony create and delete
#bx wsk property set --apihost openwhisk.ng.bluemix.net
#bx wsk api create /sudoku get /sudoku/twilio --response-type json
#bx wsk api create /sudoku put /sudoku/twilio --response-type json

# Now list the package and action to confirm results
bx wsk package get sudoku

