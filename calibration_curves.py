#!/usr/bin/env python3
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression

# --- CONFIG ---
VALIDATED_CSV = 'validated_birdnet.csv'     # semicolon-delimited CSV: species;confidence;label
THR_XLS       = 'species_specific.xls'      # Excel file with headers: species, threshold, precision, retained_pct
OUT_DIR       = 'calibration_curves'
BIN_WIDTH     = 0.05
GRID_POINTS   = 200
MIN_CONF      = 0.5                        # lower bound of confidences you actually validated
# ---------------

# 1. Load your validated detections
df = pd.read_csv(VALIDATED_CSV, sep=';')

# 2. Load species thresholds from Excel
thr_df = pd.read_excel(THR_XLS, sheet_name=0)  # ['species','threshold',...]

# 3. Prepare output directory
os.makedirs(OUT_DIR, exist_ok=True)

# 4. Only plot species for which you have thresholds
species_list = thr_df['species'].unique()

for sp in species_list:
    # 5a. Subset to this species and drop missing values
    sub = df[df['species'] == sp].dropna(subset=['confidence', 'label'])
    
    # 5b. Only keep the range you actually validated
    sub = sub[sub['confidence'] >= MIN_CONF]
    
    # Skip if no data or only one class remains
    if sub.empty or sub['label'].nunique() < 2:
        print(f"Skipping {sp}: no validated data ≥ {MIN_CONF} or only one class")
        continue

    # 6. Fit logistic regression (no regularization)
    lr = LogisticRegression(penalty=None, solver='lbfgs', max_iter=1000)
    lr.fit(sub[['confidence']], sub['label'])

    # 7. Create a grid from MIN_CONF to 1.0 for the logistic curve
    conf_grid = np.linspace(MIN_CONF, 1.0, GRID_POINTS).reshape(-1, 1)
    probs = lr.predict_proba(conf_grid)[:, 1]

    # 8. Empirical binning (only in [MIN_CONF, 1.0])
    bins = np.arange(MIN_CONF, 1 + BIN_WIDTH, BIN_WIDTH)
    sub['bin'] = pd.cut(sub['confidence'], bins=bins, include_lowest=True)
    emp = sub.groupby('bin')['label'].agg(['mean', 'count']).dropna()
    mids = [interval.mid for interval in emp.index]

    # 9. Fetch this species’ threshold
    t0 = float(thr_df.loc[thr_df['species'] == sp, 'threshold'].iloc[0])

    # 10. Plot
    plt.figure(figsize=(6, 4))
    plt.plot(conf_grid, probs, label='Logistic fit')
    plt.scatter(mids, emp['mean'], s=emp['count'], label='Empirical (binned)')
    plt.axvline(t0, linestyle='--', label=f'Threshold = {t0:.2f}')
    plt.title(f'Calibration curve: {sp}')
    plt.xlabel('BirdNET confidence')
    plt.ylabel('True positive rate')
    plt.legend()
    plt.xlim(MIN_CONF, 1.0)
    plt.tight_layout()

    fn = os.path.join(OUT_DIR, f'calibration_{sp.replace(" ", "_")}.png')
    plt.savefig(fn, dpi=300)
    plt.close()
    print(f"Saved: {fn}")

print("All done — calibration curves are in", OUT_DIR)
