import numpy as np
import pandas as pd
import glob

dn = '/projects/b1131/saya/panel-of-normal'

# sompred = pd.read_csv(f'{dn}/07_predicted_somatic/nonmatched.csv')
# sompred = list(sompred.iloc[sompred.somatic.values==1,:].var_id.values)

germline_vcfs = glob.glob(f'{dn}/03_variant_calls/ground_truths/*_filtered_bbcarpon.vcf')
germline_sample_ids = [filename.split('/')[-1].split('_')[0] for filename in germline_vcfs]

called = {}
for pon_num in [5,10,20,30,40]:
    for rep_num in [1,2,3]:
        called[f'{pon_num}-{rep_num}'] = {}
        for sample_id in germline_sample_ids:
            called[f'{pon_num}-{rep_num}'][sample_id] = set()
            fin = f'{dn}/03_variant_calls/{pon_num}-{rep_num}/{sample_id}_filtered_bbcarpon.vcf'
            with open(fin, 'r') as f:
                lines = f.readlines()
            #
            for line in lines:
                if not line.startswith('#'):
                    chrom = line.split()[0]
                    pos = line.split()[1]
                    ref = line.split()[3]
                    alt = line.split()[4]
                    var_id = f'{chrom}_{pos}_{ref}_{alt}'
                    called[f'{pon_num}-{rep_num}'][sample_id].add(var_id)

ground_truth = {}
for sample_id in germline_sample_ids:
    ground_truth[sample_id] = set()
    fin = f'{dn}/03_variant_calls/ground_truths/{sample_id}_filtered_bbcarpon.vcf'
    with open(fin, 'r') as f:
        lines = f.readlines()
    #
    for line in lines:
        if not line.startswith('#'):
            chrom = line.split()[0]
            pos = line.split()[1]
            ref = line.split()[3]
            alt = line.split()[4]
            var_id = f'{chrom}_{pos}_{ref}_{alt}'
            ground_truth[sample_id].add(var_id)

performance = pd.DataFrame(columns=['PON ID', 'F1', 'TP', 'FP', 'FN'])
for pon_num in [5,10,20,30,40]:
    for rep_num in [1,2,3]:
        tp = np.sum([len(called[f'{pon_num}-{rep_num}'][sample_id].intersection(ground_truth[sample_id])) for sample_id in germline_sample_ids])
        fp = np.sum([len(called[f'{pon_num}-{rep_num}'][sample_id] - ground_truth[sample_id]) for sample_id in germline_sample_ids])
        fn = np.sum([len(ground_truth[sample_id] - called[f'{pon_num}-{rep_num}'][sample_id]) for sample_id in germline_sample_ids])
        f1 = tp / (tp + 1/2 * (fp + fn))
        performance = pd.concat((
            performance, 
            pd.DataFrame(
                np.array([f'{pon_num}-{rep_num}', f1, tp, fp, fn]).reshape(1,-1),
                index=[0], columns=['PON ID', 'F1', 'TP', 'FP', 'FN']
            )
        ), axis=0)

performance.to_csv(f'{dn}/')