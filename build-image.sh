#!/bin/bash
echo "Tagging and pushing docker image. Be sure to start docker.app first"
echo "To examine contents: 'docker run -it sudoku-main sh'"

ibmcloud cr login
docker login us.icr.io -u token -p ${DOCKER_TOKEN}
ibmcloud cr image-rm us.icr.io/sudoku/sudoku-main
docker rmi us.icr.io/redsonja_hyboria/watson-base-common-rhubi7
docker rmi us.icr.io/sudoku/sudoku-main
docker rmi sudoku-main

# Use "--rm" to remove intermediate images
docker build --rm -t sudoku-main -f Dockerfile .

ibmcloud cr login
docker tag sudoku-main us.icr.io/sudoku/sudoku-main:latest
docker push us.icr.io/sudoku/sudoku-main:latest

# list the current images
echo "Docker Images..."
docker images
echo ""
echo "Container Registry Images..."
ibmcloud cr images