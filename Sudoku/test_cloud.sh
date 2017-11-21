#!/bin/bash
echo 'hello, $USER. testing now...'
echo 'run "bx wsk activation poll" to poll for log results'

echo 'should be an error:'
curl -X POST -H 'content-type: application/json' https://openwhisk.ng.bluemix.net/api/v1/web/kellrman%40us.ibm.com_dev/sudoku/twilio_receive.json

echo 'should be an error:'
curl -X POST -H 'content-type: application/json' https://openwhisk.ng.bluemix.net/api/v1/web/kellrman%40us.ibm.com_dev/sudoku/twilio_receive.json -d '{"data": "test"}'

echo 'receive should succeed, but solve should return a matrix error'
curl -X POST -H 'content-type: application/json' https://openwhisk.ng.bluemix.net/api/v1/web/kellrman%40us.ibm.com_dev/sudoku/twilio_receive.json -d '{"From": "9192446142", "Body": "[[1,2],[3.4]]"}'

echo 'should be an error:'
curl -X POST -H 'content-type: application/json' https://openwhisk.ng.bluemix.net/api/v1/web/kellrman%40us.ibm.com_dev/sudoku/twilio_send.json

echo 'should be an error:'
curl -X POST -H 'content-type: application/json' https://openwhisk.ng.bluemix.net/api/v1/web/kellrman%40us.ibm.com_dev/sudoku/twilio_send.json -d '{"data": "test"}'

echo 'should succeed:'
curl -X POST -H 'content-type: application/json' https://openwhisk.ng.bluemix.net/api/v1/web/kellrman%40us.ibm.com_dev/sudoku/twilio_send.json -d '{"number": "9192446142", "message": "testing..."}'

echo 'should be an error:'
curl -X POST -H 'content-type: application/json' https://openwhisk.ng.bluemix.net/api/v1/web/kellrman%40us.ibm.com_dev/sudoku/solve.json

echo 'should be an error:'
curl -X POST -H 'content-type: application/json' https://openwhisk.ng.bluemix.net/api/v1/web/kellrman%40us.ibm.com_dev/sudoku/solve.json -d '{"matrix" : "[[0,7,0,6,0,9,0,8,0],[4,0,2,0,0,0,0,0,3],[0,0,9,4,1,0,2,5,0],[8,0,0,0,9,0,3,0,5],[0,0,4,8,0,5,6,0,0],[5,0,1,0,7,0,0,0,9],[0,6,8,0,5,2,4,0,0],[1,0,0,0,0,0,7,0,6]]"}'

echo 'should be an error:'
curl -X POST -H 'content-type: application/json' https://openwhisk.ng.bluemix.net/api/v1/web/kellrman%40us.ibm.com_dev/sudoku/solve.json -d '{"matrix" : "[[0,7,0,6,9,0,8,0],[4,0,2,0,0,0,0,0,3],[0,0,9,4,1,0,2,5,0],[8,0,0,0,9,0,3,0,5],[0,0,4,8,0,5,6,0,0],[5,0,1,0,7,0,0,0,9],[0,6,8,0,5,2,4,0,0],[1,0,0,0,0,0,7,0,6],[0,4,0,3,0,1,0,9,0]]"}'

echo 'should be an error:'
curl -X POST -H 'content-type: application/json' https://openwhisk.ng.bluemix.net/api/v1/web/kellrman%40us.ibm.com_dev/sudoku/solve.json -d '{"matrix" : "[[0,7,0,6,0,9,0,8,0],[4,A,2,0,0,0,0,0,3],[0,0,9,4,1,0,2,5,0],[8,0,0,0,9,0,3,0,5],[0,0,4,8,0,5,6,0,0],[5,0,1,0,7,0,0,0,9],[0,6,8,0,5,2,4,0,0],[1,0,0,0,0,0,7,0,6],[0,4,0,3,0,1,0,9,0]]"}'

echo 'should be an error:'
curl -X POST -H 'content-type: application/json' https://openwhisk.ng.bluemix.net/api/v1/web/kellrman%40us.ibm.com_dev/sudoku/solve.json -d '{"matrix" : "[[0,7,0,6,0,9,0,8,0],[4,0,2,0,0,0,0,0,3],[0,0,9,4,1,0,2,5,0],[8,0,0,0,9,0,3,0,5],[0,0,4,8,0,5,6,0,0],[5,0,1,0,7,0,0,0,9],[0,6,8,0,5,2,4,0,0],[1,0,0,0,0,0,7,0,6],[0,4,0,3,0,1,0,9,10]]"}'

echo 'should return a solution:'
curl -X POST -H 'content-type: application/json' https://openwhisk.ng.bluemix.net/api/v1/web/kellrman%40us.ibm.com_dev/sudoku/solve.json -d '{"matrix" : "[[0,7,0,6,0,9,0,8,0],[4,0,2,0,0,0,0,0,3],[0,0,9,4,1,0,2,5,0],[8,0,0,0,9,0,3,0,5],[0,0,4,8,0,5,6,0,0],[5,0,1,0,7,0,0,0,9],[0,6,8,0,5,2,4,0,0],[1,0,0,0,0,0,7,0,6],[0,4,0,3,0,1,0,9,0]]"}'


echo 'should return a solution:'
curl -X POST -H 'content-type: application/json' https://openwhisk.ng.bluemix.net/api/v1/web/kellrman%40us.ibm.com_dev/sudoku/twilio_receive.json -d '{"From": "9192446142", "Body" : "[[0,7,0,6,0,9,0,8,0],[4,0,2,0,0,0,0,0,3],[0,0,9,4,1,0,2,5,0],[8,0,0,0,9,0,3,0,5],[0,0,4,8,0,5,6,0,0],[5,0,1,0,7,0,0,0,9],[0,6,8,0,5,2,4,0,0],[1,0,0,0,0,0,7,0,6],[0,4,0,3,0,1,0,9,0]]"}'

echo 'should return a solution and a text:'
curl -X POST -H 'content-type: application/json' https://openwhisk.ng.bluemix.net/api/v1/web/kellrman%40us.ibm.com_dev/sudoku/sudoku_solve.json -d '{"From": "9192446142", "Body" : "[[0,7,0,6,0,9,0,8,0],[4,0,2,0,0,0,0,0,3],[0,0,9,4,1,0,2,5,0],[8,0,0,0,9,0,3,0,5],[0,0,4,8,0,5,6,0,0],[5,0,1,0,7,0,0,0,9],[0,6,8,0,5,2,4,0,0],[1,0,0,0,0,0,7,0,6],[0,4,0,3,0,1,0,9,0]]"}'









