# calls: variants in /projects/b1131/saya/panel-of-normal/03_variant_calls/10-1/*.vcf
# correct: variants in /projects/b1131/saya/panel-of-normal/03_variant_calls/ground_truths/*.vcf

# there are two sets of items, some overlapping and others not
# intersect(ground_truth, calls) = true positives 
# set(ground_truth) - set(calls) = false negatives
# set(calls) - set(ground_truth) = false positives 

# prob can calculate F1 as an overall metric, alongside each counts and rates (TP, FP, FN) 

