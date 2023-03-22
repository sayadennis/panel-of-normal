#!/bin/bash
#SBATCH -A b1042
#SBATCH -p genomics
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -t 8:00:00
#SBATCH --mem=5G
#SBATCH --mail-user=sayarenedennis@northwestern.edu
#SBATCH --mail-type=END,FAIL
#SBATCH --job-name=restml
#SBATCH --output=/projects/b1131/saya/panel-of-normal/out/run_rest_ml_features.out

module purge all
module load python-miniconda3/4.12.0

source activate pon

cd ${HOME}/panel-of-normal/07_generate_ml_features/

python 02_concatenate_annovar_features.py

python 03_calculate_bbcar_freq.py

python 04_impute_missing.py

python 05_prep_input_target.py
