#!/bin/bash

export DATE=`date '+%F_%H:%M:%S'`

# Now run locally. Use "rm" to remove the container once it finishes
docker run --rm -p 5010:5010 \
  --env PORT=${PORT} \
  --env DATE=$DATE \
  kineticsquid/sudoku:latest



