#!/bin/bash

find . -name "*.py[co]" -type f -delete -or -name "__pycache__" -type d -delete
