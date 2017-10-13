#!/bin/bash
echo "hello, $USER. testing now..."
echo "run bx wsk activation poll to poll for log results"

# Now update the action at Bluemix, also creates the action if it doesn't exist
bx api https://api.ng.bluemix.net
bx wsk action invoke sudoku/sudoku_solve --blocking --result --param From +19192446142 --param Body "'[[0,7,0,6,0,9,0,8,0],[4,0,2,0,0,0,0,0,3],[0,0,9,4,1,0,2,5,0],[8,0,0,0,9,0,3,0,5],[0,0,4,8,0,5,6,0,0],[5,0,1,0,7,0,0,0,9],[0,6,8,0,5,2,4,0,0],[1,0,0,0,0,0,7,0,6],[0,4,0,3,0,1,0,9,0]]'"

bx wsk action invoke sudoku/sudoku_solve --blocking --result --param From +19192446142 --param Body "'[[7,7,0,6,0,9,0,8,0],[4,0,2,0,0,0,0,0,3],[0,0,9,4,1,0,2,5,0],[8,0,0,0,9,0,3,0,5],[0,0,4,8,0,5,6,0,0],[5,0,1,0,7,0,0,0,9],[0,6,8,0,5,2,4,0,0],[1,0,0,0,0,0,7,0,6],[0,4,0,3,0,1,0,9,0]]'"



