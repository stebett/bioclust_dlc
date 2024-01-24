#!/bin/bash

source /usr/local/conda/etc/profile.d/conda.sh

conda activate deeplabcut

python3 produce-videos.py

conda deactivate
