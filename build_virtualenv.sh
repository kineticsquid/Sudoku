#!/bin/bash
@echo on
mkdir python-runtime
cd python-runtime
virtualenv virtualenv
source virtualenv/bin/activate
pip install -r requirements.txt





