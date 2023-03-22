#!/bin/bash
#SBATCH -A b1042
#SBATCH -p genomics
#SBATCH --array=0-51
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -t 2:00:00
#SBATCH --mem=1G
#SBATCH --mail-user=sayarenedennis@northwestern.edu
#SBATCH --mail-type=END,FAIL
#SBATCH --job-name=avfts_pon_%a
#SBATCH --output=/projects/b1131/saya/panel-of-normal/out/generate_annovar_features_%a.out

module purge all
module load python-miniconda3/4.12.0

source activate pon

cd ${HOME}/panel-of-normal/07_generate_ml_features/

## Define input arguments for job array 
IFS=$'\n' read -d '' -r -a input_args < /projects/b1131/saya/bbcar/data/02a_mutation/sample_names_tumor_normal.txt

mkdir -p /projects/b1131/saya/panel-of-normal/06_ml_features

python 01_generate_annovar_features.py ${input_args[$SLURM_ARRAY_TASK_ID]}
