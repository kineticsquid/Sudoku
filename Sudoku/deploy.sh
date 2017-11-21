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
# sudo pip install virtualenv
# virtualenv virtualenv
# source virtualenv/bin/activate
# pip install -r ../requirements.txt
# pip install --upgrade pillow
# pip freeze

# read -p "Press [Enter] to contine"

# Zip this up with action code for receive and other pre-req code from this project
cp sudokuSolve.py __main__.py
zip -r sudokuSolve.zip __main__.py
zip -r sudokuSolve.zip virtualenv
rm __main__.py

# Zip this up with action code for send and other pre-req code from this project
cp twilioSend.py __main__.py
zip -r twilioSend.zip __main__.py
zip -r twilioSend.zip virtualenv
rm __main__.py

# Create zip file for the solver action
cp solvePuzzle.py __main__.py
zip -r solvePuzzle.zip __main__.py
zip -r solvePuzzle.zip virtualenv
rm __main__.py

#Create zip file for the action to generate an image file
cp generateImageFile.py __main__.py
zip -r generateImageFile.zip __main__.py
zip -r generateImageFile.zip virtualenv
rm __main__.py

# rm virtualenv

# Authenticate to Bluemix and set the target org and space
bx api https://api.ng.bluemix.net
bx login --apikey ${WSK_AUTH}
bx target -o ${CF_ORG} -s ${CF_SPACE}

# Update the package (create it if it doesn't exist)
bx wsk package update sudoku --shared yes

# Update the actions
bx wsk action update sudoku/solve ./sudokuSolve.zip --kind python:3 --web true
rm sudokuSolve.zip
bx wsk action update sudoku/twilioSend ./twilioSend.zip --kind python:3 --web true
rm twilioSend.zip
bx wsk action update sudoku/solvePuzzle ./solvePuzzle.zip --kind python:3 --web true
rm solvePuzzle.zip
bx wsk action update sudoku/generateImageFile ./generateImageFile.zip --kind python:3 --web true
rm generateImageFile.zip

# Define API - do this once only because there is no update, ony create and delete
#bx wsk property set --apihost openwhisk.ng.bluemix.net
#bx wsk api create /sudoku get /sudoku/twilio --response-type json
#bx wsk api create /sudoku put /sudoku/twilio --response-type json

# Now list the package and action to confirm results
bx wsk package get sudoku

