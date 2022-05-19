#!/bin/bash

docker rmi kineticsquid/sudoku:latest
docker build --rm --no-cache --pull -t kineticsquid/sudoku:latest -f Dockerfile .
docker push kineticsquid/sudoku:latest

# list the current images
echo "Docker Images..."
docker images

echo "Now running..."
./.vscode/run-image-locally.sh
