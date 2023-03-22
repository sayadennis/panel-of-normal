import os
import sys
import numpy as np
import pandas as pd

###########################################
#### Get input arguments (sample info) ####
###########################################

source = 'tumor_normal'
sample_id = sys.argv[1]
annovar_filename = f'{sample_id}_bbcarpon.hg38_multianno.vcf'

if sample_id[-1]=='t':
    sample_id = sample_id[:-1] # remove the "t" at the end

for pon_num in [5, 10, 20, 30, 40]:
    for rep_num in [1,2,3]:
        ##########################################
        #### Set input and output directories ####
        ##########################################

        din = f'/projects/b1131/saya/panel-of-normal/05_annovar/{pon_num}-{rep_num}'
        dout = f'/projects/b1131/saya/panel-of-normal/06_ml_features/{pon_num}-{rep_num}/01_indivi_annovar_features'
        
        if not os.path.isdir(f'/projects/b1131/saya/panel-of-normal/06_ml_features/{pon_num}-{rep_num}'):
            os.mkdir(f'/projects/b1131/saya/panel-of-normal/06_ml_features/{pon_num}-{rep_num}')

        if not os.path.isdir(dout):
            os.mkdir(dout)

        #######################################
        #### Set variable names to collect ####
        #######################################

        variables=[
            'var_id',
            'source',
            'sample_id',
            'Func.refGene',
            'Gene.refGene',
            'ExonicFunc.refGene',
            'Func.knownGene',
            'Gene.knownGene',
            'GeneDetail.knownGene',
            'ExonicFunc.knownGene',
            'Func.ensGene',
            'Gene.ensGene',
            'GeneDetail.ensGene',
            'ExonicFunc.ensGene',
            'AF',
            'avsnp150',
            'ExAC_ALL',
            'SIFT_score',
            'SIFT_pred',
            'Polyphen2_HDIV_score',
            'Polyphen2_HDIV_pred',
            'Polyphen2_HVAR_score',
            'Polyphen2_HVAR_pred',
            'LRT_score',
            'LRT_pred',
            'MutationTaster_score',
            'MutationTaster_pred',
            'MutationAssessor_score',
            'MutationAssessor_pred',
            'FATHMM_score',
            'FATHMM_pred',
            'MetaSVM_score',
            'MetaSVM_pred',
            'MetaLR_score',
            'MetaLR_pred',
            'VEST3_score',
            'CADD_raw',
            'CADD_phred',
            'GERP++_RS',
            'phyloP20way_mammalian',
            'phyloP100way_vertebrate',
            'SiPhy_29way_logOdds'
        ]

        ##########################
        #### Collect features ####
        ##########################

        ## Define feature matrix where I can record/append data 
        features = pd.DataFrame(columns=variables)

        ## Iterate through lines of VCF
        vcf = f'{din}/{annovar_filename}'

        with open(vcf, 'r') as f:
            lines = f.readlines()

        # loop through lines
        for line in lines:
            if not line.startswith('#'):
                var_feature = pd.DataFrame(index=[0],columns=variables)
                # define elements of variants and their annotations 
                var_elements = line.split()
                chrom = var_elements[0]
                pos = var_elements[1]
                ref = var_elements[3]
                alt = var_elements[4]
                info = var_elements[7]
                # create variant ID 
                var_feature.loc[0,'var_id'] = f'{chrom}_{pos}_{ref}_{alt}'
                var_feature.loc[0,'source'] = source
                var_feature.loc[0,'sample_id'] = sample_id
                # get necessary information
                info = info.split(';')
                try:
                    third_af_loc = np.where([x.startswith('AF=') for x in info])[0][2]
                    info = info[:third_af_loc]
                except:
                    print(f'{chrom}_{pos}_{ref}_{alt},{source},{sample_id}')
                for anno_item in info:
                    for variable in variables:
                        if anno_item.startswith(variable):
                            feature_value = anno_item.split('=')[1]
                            try:
                                var_feature.loc[0,variable] = float(feature_value)
                            except:
                                if feature_value != '.': # if it's not the regular "." (i.e. missing) - then enter so that we can evaluate
                                    var_feature.loc[0,variable] = feature_value
                # record result in feature matrix 
                features = pd.concat((features,var_feature), ignore_index=True)

        features.to_csv(f'{dout}/{source}_{sample_id}_bbcarpon_annovar_features.csv', index=False)
