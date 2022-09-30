#!/bin/bash
#SBATCH -A b1042
#SBATCH -p genomicslong
#SBATCH -n 1
#SBATCH --array=0-2
#SBATCH -t 168:00:00
#SBATCH --mem=5G
#SBATCH --mail-user=sayarenedennis@northwestern.edu
#SBATCH --mail-type=END,FAIL
#SBATCH --job-name="pon_%a"
#SBATCH --output=bbcar/out/generate_pon_bbcar_%a.out

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

# Define input arguments for job array 
IFS=$'\n' read -d '' -r -a flist <<< "$(ls -1 ${samplesetdir}/development_subset_*-1.txt)"
subsetids_fn=${flist[${SLURM_ARRAY_TASK_ID}]}

IFS='/' read -ra subsetid <<< "${subsetids_fn}"
IFS='.' read -ra subsetid <<< "${subsetid[-1]}"
subsetid=${subsetid[0]}

# Create temporary directory for PON and for variant calls if they don't exist 
if [ ! -d ${tmpdir}/${subsetid} ]; then
  mkdir -p ${tmpdir}/${subsetid};
fi

# Instructions taken from https://gatk.broadinstitute.org/hc/en-us/articles/360035531132

# Step 2: Create a GenomicsDB from the normal Mutect2 calls:
rm -r ${tmpdir}/${subsetid}/*
gatk GenomicsDBImport -R $ref -L $interval \
    --tmp-dir ${tmpdir}/${subsetid}/ \
    --genomicsdb-workspace-path ${tmpdir}/${subsetid}/pon_db \
    $(for x in $(cat ${subsetids_fn}); do echo -n "-V ${tmpdir}/mutect/${x}_bqsr.vcf.gz "; done)

# Step 3: Combine the normal calls using CreateSomaticPanelOfNormals:
cd ${tmpdir}/${subsetid}/
gatk CreateSomaticPanelOfNormals \
    -V gendb://pon_db \
    -R $ref \
    --output ${dout}/pon_${subsetid}.vcf.gz
#

# --germline-resource /projects/b1131/saya/bbcar/genome_resources/GATK/af-only-gnomad.hg38.vcf.gz 
