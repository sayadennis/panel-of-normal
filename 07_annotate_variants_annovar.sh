#!/bin/bash
#SBATCH -A b1042
#SBATCH -p genomics
#SBATCH --array=0-51
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -t 4:00:00
#SBATCH --mem=20G
#SBATCH --mail-user=sayarenedennis@northwestern.edu
#SBATCH --mail-type=END,FAIL
#SBATCH --job-name=av_pon_%a
#SBATCH --output=/projects/b1131/saya/panel-of-normal/out/annovar_%a.out

cd /projects/b1131/saya/panel-of-normal/

## Load necessary modules 
module purge all
module load perl/5.16

## Define input arguments for job array 
IFS=$'\n' read -d '' -r -a input_args < /projects/b1131/saya/bbcar/data/02a_mutation/sample_names_tumor_normal.txt

mkdir -p /projects/b1131/saya/panel-of-normal/05_annovar

for pon_num in 5 10 20 30 40; do
    for rep_num in {1..3}; do
        ## Set input and output directories 
        din=/projects/b1131/saya/panel-of-normal/04_filtered_variants/${pon_num}-${rep_num}
        dout=/projects/b1131/saya/panel-of-normal/05_annovar/${pon_num}-${rep_num}
        dav='/projects/b1131/saya/bbcar/tools/annovar'

        mkdir -p $dout

        fin=${input_args[$SLURM_ARRAY_TASK_ID]}_DPfiltered_bbcarpon.vcf
        fout=${input_args[$SLURM_ARRAY_TASK_ID]}_bbcarpon

        perl ${dav}/table_annovar.pl \
            ${din}/${fin} \
            ${dav}/humandb/ \
            -buildver hg38 \
            -out $dout/$fout \
            -remove \
            -protocol refGene,knownGene,ensGene,avsnp150,dbnsfp35a,dbnsfp31a_interpro,exac03,gnomad211_exome,gnomad211_genome \
            -operation g,g,g,f,f,f,f,f,f \
            -nastring . -vcfinput
        #
    done
done

