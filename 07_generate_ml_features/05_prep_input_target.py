import os
import sys
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

for pon_num in [5, 10, 20, 30, 40]:
    for rep_num in [1,2,3]:

        ##########################################
        #### Set input and output directories ####
        ##########################################

        din = f'/projects/b1131/saya/panel-of-normal/06_ml_features/{pon_num}-{rep_num}/04_imputed'
        dout = f'/projects/b1131/saya/panel-of-normal/06_ml_features/{pon_num}-{rep_num}'
        dix = f'/projects/b1131/saya/panel-of-normal/06_ml_features/{pon_num}-{rep_num}/somatic_pred_ix'

        if not os.path.isdir(dout):
            os.mkdir(dout)

        if not os.path.isdir(dix):
            os.mkdir(dix)

        ###################
        #### Load data ####
        ###################

        data = pd.read_csv(f'{din}/features_imputed.csv')

        #####################################
        #### Convert to input and target ####
        #####################################

        data['somatic'] = (data.source=='tumor_normal').astype(int)

        variables=[
            'var_id',
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
            'SiPhy_29way_logOdds',
            'somatic'
        ]

        Xy_nonmatched = data.iloc[data.source.values=='tumor_only',:][variables].drop_duplicates(ignore_index=True).set_index('var_id', drop=True)
        X_nonmatched = Xy_nonmatched.iloc[:,:-1]

        Xy_matched = data.iloc[data.source.values!='tumor_only',:][variables].drop_duplicates(ignore_index=True).set_index('var_id', drop=True)
        X_matched = Xy_matched.iloc[:,:-1]
        y_matched = Xy_matched.iloc[:,-1]

        #######################################
        #### Create train and test indices ####
        #######################################

        train_ix, test_ix = train_test_split(X_matched.index, test_size=.2, random_state=43, shuffle=True)

        ##############
        #### Save ####
        ##############

        X_matched.to_csv(f'{dout}/input_matched.csv', index=True, header=True)
        y_matched.to_csv(f'{dout}/target_matched.csv', index=True, header=True)

        ## Below is not necessary because everything is matched for this PON workflow 
        # X_nonmatched.to_csv(f'{dout}/input_nonmatched.csv', index=True, header=True)

        pd.DataFrame(index=train_ix).to_csv(f'{dix}/train_index.txt', header=False)
        pd.DataFrame(index=test_ix).to_csv(f'{dix}/test_index.txt', header=False)
