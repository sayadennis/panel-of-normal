#!/bin/bash
#SBATCH -A b1042
#SBATCH -p genomics
#SBATCH -n 1
#SBATCH -t 1:00:00
#SBATCH --mail-user=sayarenedennis@northwestern.edu
#SBATCH --mail-type=END,FAIL
#SBATCH --job-name="sampleset"
#SBATCH --output=/projects/b1131/saya/panel-of-normal/out/generate_samplesets.out

. ~/anaconda3/etc/profile.d/conda.sh
conda activate pon

cd /projects/b1131/saya/bbcar/data/00_raw

dout='/projects/b1131/saya/panel-of-normal/01_samplesets'

# Sample set file of all "paired" samples -- i.e. both somatic and germline data available
comm -12  <(ls ./germline/) <(ls ./tissue/) > ${dout}/all.txt

# Run the rest in Python script 
python ${HOME}/panel-of-normal/01_generate_samplesets.py ${dout}
