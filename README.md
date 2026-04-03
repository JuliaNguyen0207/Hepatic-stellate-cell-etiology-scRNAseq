# Code & Analysis for: "Etiology specific activation programs of hepatic stellate cells revealed by integrated single-cell RNA-seq across human liver diseases"
## Overview

This repository contains the code used for the single-cell RNA sequencing (scRNA-seq) analysis presented in our study of hepatic stellate cells (HSCs) across healthy, fibrotic, viral, cholestatic, and tumor-associated human liver microenvironments.

The workflow integrates three public human liver scRNA-seq datasets:

- **GSE136103**: healthy and cirrhotic liver reference atlas
- **GSE282701**: HBV-positive and HBV-negative hepatocellular carcinoma microenvironment
- **GSE166635**: primary liver cancer heterogeneity

The analysis was designed to:
1. preprocess each dataset in a consistent framework,
2. construct a global liver atlas,
3. identify and subset hepatic stellate cells,
4. integrate the HSC compartment across cohorts,
5. annotate HSC states,
6. perform comparative downstream analysis across etiologies.

---

## System Requirements

- Python 3.10+
- Colab Notebook or command-line Python environment
- Recommended RAM: 32 GB or higher
- GPU is **not required**, but may help with large-scale computation and visualization

Install dependencies with:

```bash
pip install -r requirements.txt
```
---

# Repository structure
```bash
.
├── code/
│   ├── 01_preprocess_all_datasets.py
│   ├── 02_integrate_hsc_atlas.py
│   ├── 03_downstream_analysis.py
│   └── 04_visualization_and_export.py
│
├── data/
│   ├── raw/
│   │   ├── GSE136103/
│   │   ├── GSE282701/
│   │   └── GSE166635/
│   ├── processed/
│   └── metadata/
│
├── results/
│   ├── figures/
│   ├── tables/
│   └── ppi_input/
│
├── requirements.txt
└── README.md
```
## Datasets

Publicly available human liver scRNA-seq datasets were retrieved from the NCBI Gene Expression Omnibus (GEO):___

GSE136103
GSE282701
GSE166635

Please download the raw matrices and place them in the corresponding folders under:
```bash
data/raw/
