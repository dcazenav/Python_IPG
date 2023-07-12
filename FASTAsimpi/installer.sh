#!/bin/bash

mamba create -n tb-profiler -c conda-forge -c bioconda docxtpl tb-profiler=4.4.2
conda install -c bioconda miru-hero
conda activate tb-profiler

git clone https://github.com/phglab/MIRUReader.git
git clone https://github.com/matnguyen/SpoTyping.git

pip install -r requirements.txt