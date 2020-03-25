#!/bin/bash

export APP_ENV=test

source venv/bin/activate

clear
python -m unittest discover tests
