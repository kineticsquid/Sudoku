#!/bin/bash
echo "URL is http://0.0.0.0:5000/"

# Now run locally. Use "rm" to remove the container once it finishes
docker run --rm -p 5000:5000 us.icr.io/sudoku/sudoku-main:latest


