# BirdNET Calibration Pipeline

A reproducible workflow for calibrating BirdNET confidence scores against manually validated labels. This repository contains scripts in Python and R to:

1. Clean & export validated BirdNET detections  
2. Compute species-specific confidence cutoffs targeting 90% precision  
3. Generate calibration curves per species and overlay plots  
4. Calculate true-positive rates (recall) at chosen thresholds  

---

## 📂 Repository Structure

```plaintext
birdnet-calibration/
├── .gitignore
├── LICENSE
├── README.md
├── validated_birdnet.csv        # Hand-validated data export
├── species_specific.xls         # R-derived thresholds & metrics
├── export_validated_csv.py      # Step 1: CSV export (Python)
├── species_thresholds.R         # Step 2: Threshold search (R)
├── calibration_curves.py        # Step 3a: Per-species curves (Python)
├── overlay_cutoff_0_7.py        # Step 3b: All-species overlay plot
├── tpr_at_thresholds.py         # Step 4: Recall table (Python)
└── calibration_curves/          # (ignored) generated PNGs and figures
Prerequisites

Python 3.8+
pip install pandas numpy scikit-learn matplotlib openpyxl
R 4.0+
install.packages(c("dplyr","readr","tidyr","broom"))
🚀 Quick Start
1.Clone the repo
git clone https://github.com/Cyrusko/Birdnet-calibration.git
cd Birdnet-calibration
2.Set up Python environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
3.Export validated CSV
python3 export_validated_csv.py
4.Compute thresholds in R
Rscript species_thresholds.R
5.Generate per-species calibration curves
python3 calibration_curves.py
6.Overlay all species at 0.70 cutoff
python3 overlay_cutoff_0_7.py
7.Calculate TPR at species-specific cutoffs
python3 tpr_at_thresholds.py

🔧 Configuration

Each script has a configuration block at the top where you can adjust:

Input/output file paths
Minimum confidence validated (MIN_CONF)
Universal cutoff (UNIVERSAL_CUT)
Plot settings (grid resolution, figure size)
📜 License

This project is licensed under the MIT License.

🙋‍♂️ Contact

Kourosh Haghbin
Email: kourosh.haghbin@tu-dortmund.de
GitHub: Cyrusko

