BirdNET Calibration Pipeline

A reproducible workflow for calibrating BirdNET confidence scores against manually validated labels. This repository contains scripts in Python and R to:

Clean & export validated BirdNET detections
Compute species‐specific confidence cutoffs targeting 90 % precision
Generate calibration curves per species and overlay plots
Calculate true‐positive rates (recall) at chosen thresholds
📂 Repository Structure

birdnet-calibration/
├── .gitignore
├── LICENSE
├── README.md
├── validated_birdnet.csv        # Hand‐validated data export
├── species_specific.xls         # R‐derived thresholds & metrics
├── export_validated_csv.py      # Step 1: CSV export (Python)
├── species_thresholds.R         # Step 2: Threshold search (R)
├── calibration_curves.py        # Step 3a: Per‐species curves (Python)
├── overlay_cutoff_0_7.py        # Step 3b: All‐species overlay plot
├── tpr_at_thresholds.py         # Step 4: Recall table (Python)
└── calibration_curves/          # (ignored) generated PNGs
⚙️ Prerequisites

Python 3.8+
Install via:

pip install pandas numpy scikit-learn matplotlib openpyxl
R 4.0+
Install the tidyverse packages:

install.packages(c("dplyr","readr","tidyr","broom"))
🚀 Quick Start

Clone the repo
git clone https://github.com/Cyrusko/Birdnet-calibration.git
cd Birdnet-calibration
Set up Python environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
Export validated CSV
python3 export_validated_csv.py
Compute thresholds in R
Rscript species_thresholds.R
Generate per‐species calibration curves
python3 calibration_curves.py
Overlay all species at 0.70 cutoff
python3 overlay_cutoff_0_7.py
Calculate TPR at species‐specific cutoffs
python3 tpr_at_thresholds.py
🔧 Configuration

Adjust the constants at the top of each script for input paths, confidence bounds (e.g. MIN_CONF = 0.5), and cutoff values (e.g. UNIVERSAL_CUT = 0.70).

📜 License

This project is licensed under the MIT License. See LICENSE for details.

🙋‍♂️ Contact

Kourosh Haghbin
kourosh.haghbin@tu-dortmund.de
GitHub: https://github.com/Cyrusko