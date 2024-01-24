#!/bin/bash

source /usr/local/conda/etc/profile.d/conda.sh

conda activate deeplabcut

python3 analyze-novel-videos.py

conda deactivate
