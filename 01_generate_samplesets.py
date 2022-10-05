import sys
import numpy as np
import pandas as pd

# directory to write sample set files
dn = sys.argv[1]

# get all sample IDs 
with open(f'{dn}/all.txt', 'r') as f:
    lines = f.readlines()

sampleids = [line.strip() for line in lines]

# determine evaluation size 
eval_size = np.round(0.1 * len(sampleids)).astype(int)

# generate development set and evaluation set 
np.random.seed(7)
eval_set = list(np.random.choice(sampleids, eval_size, replace=False))
dev_set = []
for sampleid in sampleids:
    if sampleid not in eval_set:
        dev_set.append(sampleid)

with open(f'{dn}/development.txt', 'w') as f:
    for sampleid in dev_set:
        f.write(f'{sampleid}\n')

with open(f'{dn}/evaluation.txt', 'w') as f:
    for sampleid in eval_set:
        f.write(f'{sampleid}\n')

# generate dev set subsamples with different sizes 
subsets = {}
for size in [5, 10, 20, 30, 40]:
    for seed in [1,2,3,4]:
        np.random.seed(seed)
        subsets[f'{size}-{seed}'] = list(np.random.choice(dev_set, size, replace=False))

# write the sample sets 
for key in subsets.keys():
    with open(f'{dn}/development_subset_{key}.txt', 'w') as f:
        for sampleid in subsets[key]:
            f.write(f'{sampleid}\n')
