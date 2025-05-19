#!/usr/bin/env python3
import os
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression

# — CONFIG —
VALIDATED_CSV = 'validated_birdnet.csv'   # your semicolon-delimited labels file
THRESH_XLS    = 'species_specific.xls'    # R output with columns: species, threshold, precision, retained_pct
MIN_CONF      = 0.5                       # only confidences you actually validated
# ————

if not os.path.exists(VALIDATED_CSV) or not os.path.exists(THRESH_XLS):
    raise FileNotFoundError("Make sure both 'validated_birdnet.csv' and 'species_specific.xls' are in this folder.")

# 1. Load data
df  = pd.read_csv(VALIDATED_CSV, sep=';').dropna(subset=['confidence','label'])
thr = pd.read_excel(THRESH_XLS, sheet_name=0)

records = []
for sp in thr['species']:
    # subset to species and only the range you validated
    sub = df[(df['species'] == sp) & (df['confidence'] >= MIN_CONF)]
    # total number of true positives in your manual labels
    total_true = (sub['label'] == 1).sum()
    if total_true == 0:
        # no positives to compute recall on
        continue

    # R-derived threshold for this species
    t0 = float(thr.loc[thr['species'] == sp, 'threshold'].iloc[0])

    # empirical TPR = fraction of true positives with conf >= t0
    emp_tpr = ((sub['confidence'] >= t0) & (sub['label'] == 1)).sum() / total_true

    # fit a logistic model just to get model‐predicted TPR at exactly t0
    if sub['label'].nunique() > 1:
        lr = LogisticRegression(penalty=None, solver='lbfgs', max_iter=1000)
        lr.fit(sub[['confidence']], sub['label'])
        model_tpr = lr.predict_proba([[t0]])[0,1]
    else:
        model_tpr = np.nan

    records.append({
        'species':       sp,
        'threshold':     t0,
        'empirical_TPR': emp_tpr,
        'model_TPR':     model_tpr,
        'n_true':        int(total_true)
    })

# 2. Build and save the table
result_df = pd.DataFrame(records).sort_values('empirical_TPR', ascending=False)
print(result_df.to_string(index=False))

result_df.to_csv('tpr_at_thresholds.csv', index=False)
print("\nSaved results to tpr_at_thresholds.csv")
