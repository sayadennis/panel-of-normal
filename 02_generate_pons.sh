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

din='/projects/b1131/saya/bbcar/data/01_alignment/germline/aligned'
tmpdir='/projects/b1042/lyglab/saya/bbcar/pon_tmp'
dout='/projects/b1131/saya/panel-of-normal/02_pon'

## Define input arguments for job array 
ls /projects/b1131/saya/panel-of-normal/01_samplesets/development_subset_*-1.txt > input_args_${SLURM_ARRAY_TASK_ID}.txt
IFS=$'\n' read -d '' -r -a input_args < input_args_${SLURM_ARRAY_TASK_ID}.txt

# subset_id=

# IFS='\n' read -ra filenames <<< ${input_args[$SLURM_ARRAY_TASK_ID]}
# IFS='.' read -ra subsetid <<< ${filenames[-1]}
# subsetid=${subsetid[0]}

# if [ ! -d ${dout}/${subsetid} ]; then
#   mkdir -p ${dout}/${subsetid};
# fi

# if [ ! -d ${tmpdir}/${subsetid} ]; then
#   mkdir -p ${tmpdir}/${subsetid};
# fi

# interval='/projects/b1122/gannon/bbcar/RAW_data/int_lst/SureSelect_v6/hg38.preprocessed.interval_list'
# ref='/projects/p30791/hg38_ref/hg38.fa'

# module purge all
# export PATH="/projects/b1131/saya/bbcar/tools/gatk-4.2.5.0:$PATH"
# # module load gatk/4.1.0

# # Instructions taken from https://gatk.broadinstitute.org/hc/en-us/articles/360035531132

# # # Step 1: Run Mutect2 in tumor-only mode for each normal sample:
# for sampleid in $(cat /projects/b1131/saya/bbcar/sample_names_germline.txt); do 
#     gatk Mutect2 -R $ref -I $din/${sampleid}_bqsr.bam --max-mnp-distance 0 -O $dout/${sampleid}_bqsr.vcf.gz;
# done
# #

# # Step 2: Create a GenomicsDB from the normal Mutect2 calls:
# rm -r ${tmpdir}/${subsetid}/*
# gatk GenomicsDBImport -R $ref -L $interval --tmp-dir ${tmpdir}/${subsetid}/pon_tmp/ --genomicsdb-workspace-path ${tmpdir}/${subsetid}/pon_db $(for x in $(cat ${input_args[$SLURM_ARRAY_TASK_ID]}); do echo -n "-V ${din}/${x}_bqsr.vcf.gz "; done)

# # Step 3: Combine the normal calls using CreateSomaticPanelOfNormals:
# cd /projects/b1042/lyglab/saya/bbcar/
# gatk CreateSomaticPanelOfNormals \
#     -V gendb://pon_db \
#     -R $ref \
#     --output $dout/bbcar_pon.vcf.gz
# #

# # --germline-resource /projects/b1131/saya/bbcar/genome_resources/GATK/af-only-gnomad.hg38.vcf.gz 
