#!/bin/bash
echo 'hello, $USER. testing now...'

cd ~/DevelopmentEnvironment/OpenWhiskActions/Sudoku

echo 'should be an error:'
python twilio_receive.py

echo 'should be an error:'
python twilio_receive.py 'data'

echo 'receive should succeed, but solve should return a matrix error'
python twilio_receive.py '9192446142' '[[1,2],[3.4]]'

echo 'should be an error:'
python twilio_send.py

echo 'should be an error:'
python twilio_send.py 'data'

echo 'should succeed:'
python twilio_send.py '9192446142' 'testing...'

echo 'should be an error:'
python SudokuSolver.py

echo 'should be an error:'
python SudokuSolver.py '[[4,0,2,0,0,0,0,0,3],[0,0,9,4,1,0,2,5,0],[8,0,0,0,9,0,3,0,5],[0,0,4,8,0,5,6,0,0],[5,0,1,0,7,0,0,0,9],[0,6,8,0,5,2,4,0,0],[1,0,0,0,0,0,7,0,6]]'

echo 'should be an error:'
python SudokuSolver.py '[[0,7,0,6,0,9,8,0],[4,0,2,0,0,0,0,0,3],[0,0,9,4,1,0,2,5,0],[8,0,0,0,9,0,3,0,5],[0,0,4,8,0,5,6,0,0],[5,0,1,0,7,0,0,0,9],[0,6,8,0,5,2,4,0,0],[1,0,0,0,0,0,7,0,6]]'

echo 'should be an error:'
python SudokuSolver.py '[[0,7,0,6,0,9,A,8,0],[4,0,2,0,0,0,0,0,3],[0,0,9,4,1,0,2,5,0],[8,0,0,0,9,0,3,0,5],[0,0,4,8,0,5,6,0,0],[5,0,1,0,7,0,0,0,9],[0,6,8,0,5,2,4,0,0],[1,0,0,0,0,0,7,0,6],[0,4,0,3,0,1,0,9,0]]'

echo 'should be an error:'
python SudokuSolver.py '[[0,7,0,6,0,9,0,8,0],[4,0,2,0,0,0,0,0,3],[0,0,9,4,1,0,2,5,0],[8,0,0,0,9,0,3,0,5],[0,0,4,8,0,5,6,0,0],[5,0,1,0,7,0,0,0,9],[0,6,8,0,5,2,4,0,0],[1,0,0,0,0,0,7,0,6],[0,4,0,3,0,1,0,9,10]]'

echo 'should result in a solution:'
python SudokuSolver.py '[[0,7,0,6,0,9,0,8,0],[4,0,2,0,0,0,0,0,3],[0,0,9,4,1,0,2,5,0],[8,0,0,0,9,0,3,0,5],[0,0,4,8,0,5,6,0,0],[5,0,1,0,7,0,0,0,9],[0,6,8,0,5,2,4,0,0],[1,0,0,0,0,0,7,0,6],[0,4,0,3,0,1,0,9,0]]'

echo 'should result in a solution'
python twilio_receive.py '9192446142' '[[0,7,0,6,0,9,0,8,0],[4,0,2,0,0,0,0,0,3],[0,0,9,4,1,0,2,5,0],[8,0,0,0,9,0,3,0,5],[0,0,4,8,0,5,6,0,0],[5,0,1,0,7,0,0,0,9],[0,6,8,0,5,2,4,0,0],[1,0,0,0,0,0,7,0,6],[0,4,0,3,0,1,0,9,0]]'





