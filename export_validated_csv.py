#!/usr/bin/env python3
import pandas as pd

# 1) Read your merged Excel
df = pd.read_excel('merged_all_seasons_data.xlsx')

# 2) Keep only the needed columns
df = df[['Scientific name', 'Confidence', 'Validation Status']]

# 3) Fix mis-parsed confidences: any value >1 (e.g. 765) → divide by 1000 → 0.765
df['Confidence'] = pd.to_numeric(df['Confidence'], errors='coerce')
mask = df['Confidence'] > 1
df.loc[mask, 'Confidence'] = df.loc[mask, 'Confidence'] / 1000

# 4) Map Validation Status to binary label
df['label'] = df['Validation Status'].map({'p': 1, 'nc': 0})

# 5) Rename for the R script
df = df.rename(columns={
    'Scientific name': 'species',
    'Confidence':       'confidence'
})

# 6) Save CSV
df.to_csv('validated_birdnet.csv', index=False)

print("Wrote validated_birdnet.csv with corrected confidence values.")
