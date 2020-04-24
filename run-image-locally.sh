#!/bin/bash

echo "http://0.0.0.0:5002/"

# Now run locally. Use "rm" to remove the container once it finishes
docker run --rm -p 5002:5010 us.icr.io/sudoku/sudoku-main:latest
#docker run --rm --env URL_ROOT="/sudoku" -p 5000:5000 us.icr.io/sudoku/sudoku-main:latest



