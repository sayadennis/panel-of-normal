import numpy as np
import pandas as pd
import glob
import matplotlib.pyplot as plt

dn = '/projects/b1131/saya/panel-of-normal'
dout = '/projects/b1131/saya/panel-of-normal/plots'

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

performance = pd.DataFrame(columns=['PON', 'REP', 'F1', 'TP', 'FP', 'FN'])
for pon_num in [5,10,20,30,40]:
    for rep_num in [1,2,3]:
        tp = np.sum([len(called[f'{pon_num}-{rep_num}'][sample_id].intersection(ground_truth[sample_id])) for sample_id in germline_sample_ids])
        fp = np.sum([len(called[f'{pon_num}-{rep_num}'][sample_id] - ground_truth[sample_id]) for sample_id in germline_sample_ids])
        fn = np.sum([len(ground_truth[sample_id] - called[f'{pon_num}-{rep_num}'][sample_id]) for sample_id in germline_sample_ids])
        f1 = tp / (tp + 1/2 * (fp + fn))
        performance = pd.concat((
            performance, 
            pd.DataFrame(
                np.array([pon_num, rep_num, f1, tp, fp, fn]).reshape(1,-1),
                index=[0], columns=['PON', 'REP', 'F1', 'TP', 'FP', 'FN']
            )
        ), axis=0)

fig, ax = plt.subplots(nrows=1, ncols=4, figsize=(12,6))

## F1 score 
ax[0].bar(
    x=np.arange(len(performance['PON'].unique())),
    height=[np.mean(performance['F1'].iloc[performance['PON'].values==x]) for x in [5,10,20,30,40]],
    yerr=[np.std(performance['F1'].iloc[performance['PON'].values==x]) for x in [5,10,20,30,40]],
)
ax[0].set_xticks(np.arange(len(performance['PON'].unique())))
ax[0].set_xticklabels([f'{int(x)} samples' for x in performance['PON'].unique()], rotation=45, ha='right')
ax[0].set_ylabel('F1 score')
ax[0].set_title('F1 Score')

## True positive counts
ax[1].bar(
    x=np.arange(len(performance['PON'].unique())),
    height=[np.mean(performance['TP'].iloc[performance['PON'].values==x]) for x in [5,10,20,30,40]],
    yerr=[np.std(performance['TP'].iloc[performance['PON'].values==x]) for x in [5,10,20,30,40]],
)
ax[1].set_xticks(np.arange(len(performance['PON'].unique())))
ax[1].set_xticklabels([f'{int(x)} samples' for x in performance['PON'].unique()], rotation=45, ha='right')
ax[1].set_ylabel('Number of calls')
ax[1].set_ylim([np.min(performance['TP'])*0.99, np.max(performance['TP']*1.01)])
ax[1].set_title('Correct Calls (True Positives)')

## False positive counts
ax[2].bar(
    x=np.arange(len(performance['PON'].unique())),
    height=[np.mean(performance['FP'].iloc[performance['PON'].values==x]) for x in [5,10,20,30,40]],
    yerr=[np.std(performance['FP'].iloc[performance['PON'].values==x]) for x in [5,10,20,30,40]],
)
ax[2].set_xticks(np.arange(len(performance['PON'].unique())))
ax[2].set_xticklabels([f'{int(x)} samples' for x in performance['PON'].unique()], rotation=45, ha='right')
ax[2].set_ylabel('Number of calls')
ax[2].set_title('Incorrectly Called (False Positives)')

## False negative counts
ax[3].bar(
    x=np.arange(len(performance['PON'].unique())),
    height=[np.mean(performance['FN'].iloc[performance['PON'].values==x]) for x in [5,10,20,30,40]],
    yerr=[np.std(performance['FN'].iloc[performance['PON'].values==x]) for x in [5,10,20,30,40]],
)
ax[3].set_xticks(np.arange(len(performance['PON'].unique())))
ax[3].set_xticklabels([f'{int(x)} samples' for x in performance['PON'].unique()], rotation=45, ha='right')
ax[3].set_ylabel('Number of calls')
ax[3].set_ylim([np.min(performance['FN'])*0.98, np.max(performance['FN']*1.02)])
ax[3].set_title('Incorrectly Not Called (False Negatives)')

fig.suptitle('Somatic Prediction Performance by Number of Samples in PoN', fontsize=16)
plt.tight_layout()
fig.savefig(f'{dout}/prelim_performance.png')
plt.close()

# performance.to_csv(f'{dn}/')
