#!/bin/bash
#SBATCH -A b1042
#SBATCH -p genomics
#SBATCH -n 1
#SBATCH --array=0-53
#SBATCH -t 1:00:00
#SBATCH --mem=1G
#SBATCH --mail-user=sayarenedennis@northwestern.edu
#SBATCH --mail-type=END,FAIL
#SBATCH --job-name="pon_mutect_%a"
#SBATCH --output=/projects/b1131/saya/panel-of-normal/out/pon_step1_mutect%a.out

cd /projects/b1131/saya/panel-of-normal/

module purge all
export PATH="/projects/b1131/saya/bbcar/tools/gatk-4.2.5.0:$PATH"

# Set directory names and reference files 
datadir='/projects/b1131/saya/bbcar/data/01_alignment/germline/aligned'
samplesetdir='/projects/b1131/saya/panel-of-normal/01_samplesets'
tmpdir='/projects/b1042/lyglab/saya/bbcar/pon_tmp'
dout='/projects/b1131/saya/panel-of-normal/02_pon'

interval='/projects/b1122/gannon/bbcar/RAW_data/int_lst/SureSelect_v6/hg38.preprocessed.interval_list'
ref='/projects/p30791/hg38_ref/hg38.fa'

# Define sample ID for this element of job array 
IFS=$'\n' read -d '' -r -a sampleids <<< "$(cat ${samplesetdir}/all.txt)"
sampleid=${sampleids[${SLURM_ARRAY_TASK_ID}]}

# Create directory to save mutect variant calls 
if [ ! -d ${tmpdir}/mutect ]; then
  mkdir -p ${tmpdir}/mutect;
fi

# Instructions taken from https://gatk.broadinstitute.org/hc/en-us/articles/360035531132

# Step 1: Run Mutect2 in tumor-only mode for each normal sample:
gatk Mutect2 -R $ref -I ${datadir}/${sampleid}_bqsr.bam --max-mnp-distance 0 -O ${tmpdir}/mutect/${sampleid}_bqsr.vcf.gz;
