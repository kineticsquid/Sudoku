#!/bin/bash

ic target -r us-south -g default
ic ce project select --name Utils
REV=$(date +"%y-%m-%d-%H-%M-%S")
echo ${REV}

ic ce app update -n sudoku -i docker.io/kineticsquid/sudoku-main:latest --rn ${REV} --min 1
ic ce rev list --app sudoku
ic ce app events --app sudoku
ic ce app logs --app sudoku