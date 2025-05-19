#!/usr/bin/env python3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression

# — CONFIG —
VALIDATED_CSV = 'validated_birdnet.csv'
THR_XLS       = 'species_specific.xls'
MIN_CONF      = 0.5     # lower bound of confidences you validated
UNIVERSAL_CUT = 0.70    # universal cutoff you want to test
TPR_REF       = 0.90    # horizontal reference line
GRID_POINTS   = 200
# ————————

# Load your validated data
df = pd.read_csv(VALIDATED_CSV, sep=';').dropna(subset=['confidence','label'])

# Prepare the figure
plt.figure(figsize=(10,6))

# Plot each species’ calibration curve
for sp in df['species'].unique():
    sub = df[(df['species']==sp) & (df['confidence']>=MIN_CONF)]
    if sub['label'].nunique() < 2:
        continue

    # Fit logistic regression
    lr = LogisticRegression(penalty=None, solver='lbfgs', max_iter=1000)
    lr.fit(sub[['confidence']], sub['label'])
    grid = np.linspace(MIN_CONF,1.0,GRID_POINTS).reshape(-1,1)
    probs = lr.predict_proba(grid)[:,1]

    plt.plot(grid, probs, alpha=0.6, label=sp)

# Draw the vertical universal cutoff line at 0.70
plt.axvline(UNIVERSAL_CUT, color='black', linestyle='--', lw=2,
            label=f'Universal cutoff = {UNIVERSAL_CUT:.2f}')

# Draw the horizontal TPR reference line at 0.90
plt.axhline(TPR_REF, color='darkblue', linestyle='-.', lw=2,
            label=f'TPR = {TPR_REF:.2f}')

# Final styling
plt.xlabel('BirdNET confidence')
plt.ylabel('True positive rate')
plt.title(f'Calibration curves (conf ≥ {MIN_CONF:.2f}) with universal cutoff at {UNIVERSAL_CUT:.2f}')
plt.xlim(MIN_CONF, 1.0)
plt.ylim(0, 1.02)
plt.grid(alpha=0.3)
plt.legend(bbox_to_anchor=(1.01,1), loc='upper left', fontsize='small')
plt.tight_layout()

plt.show()
# If you prefer to save to file instead of show(), uncomment:
# plt.savefig('all_species_calibration_cutoff_0.70.png', dpi=300)
