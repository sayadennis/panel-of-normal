#!/bin/bash
#SBATCH -A b1042
#SBATCH -p genomics
#SBATCH -t 48:00:00
#SBATCH --array=0-14
#SBATCH -N 1
#SBATCH -n 8
#SBATCH --mail-user=sayarenedennis@northwestern.edu
#SBATCH --mail-type=END,FAIL
#SBATCH --job-name="pon_ml%a"
#SBATCH --output=/projects/b1131/saya/panel-of-normal/out/08_train_and_evaluate%a.out

module purge all
module load python-miniconda3/4.12.0
source activate classical-ml

cd /projects/b1131/saya/panel-of-normal

## Define input arguments for job array 
IFS=$'\n' read -d '' -r -a input_args < /projects/b1131/saya/panel-of-normal/input_args_setnames.txt

inputdir=/projects/b1131/saya/panel-of-normal/06_ml_features/${input_args[$SLURM_ARRAY_TASK_ID]}
labeldir=/projects/b1131/saya/panel-of-normal/06_ml_features/${input_args[$SLURM_ARRAY_TASK_ID]}
ixdir=/projects/b1131/saya/panel-of-normal/06_ml_features/${input_args[$SLURM_ARRAY_TASK_ID]}/somatic_pred_ix
outdir=/projects/b1131/saya/panel-of-normal/06_ml_features/${input_args[$SLURM_ARRAY_TASK_ID]}/model_interpretations
modeldir=/projects/b1131/saya/panel-of-normal/06_ml_features/${input_args[$SLURM_ARRAY_TASK_ID]}/models

mkdir -p $outdir
mkdir -p $modeldir

python ${HOME}/classical-ml/ClassicalML/run_classical_ml.py \
    --input $inputdir/input_matched.csv \
    --label $labeldir/target_matched.csv \
    --outdir $outdir \
    --indexdir $ixdir \
    --scoring roc_auc
#

python ${HOME}/panel-of-normal/08_train_and_evaluate.py ${input_args[$SLURM_ARRAY_TASK_ID]}
