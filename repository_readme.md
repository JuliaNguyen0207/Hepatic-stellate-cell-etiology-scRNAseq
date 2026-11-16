# A Lineage-Purified Atlas of Human Hepatic Stellate Cells Reveals a Conserved Four-State Architecture and Niche-Specific Reprogramming in Hepatocellular Carcinoma

[![Python 3.10](https://img.shields.io/badge/Python-3.10-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Scanpy](https://img.shields.io/badge/Scanpy-v1.9%2B-orange.svg)](https://scanpy.readthedocs.io/)
[![PyDESeq2](https://img.shields.io/badge/PyDESeq2-Pseudobulk-2b83ba.svg)](https://pydeseq2.readthedocs.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 1. Study Overview & Biological Motivation

Hepatic stellate cells (HSCs) are the primary fibrogenic effector population in chronic liver disease (CLD) and furnish cancer-associated fibroblasts (CAFs) in hepatocellular carcinoma (HCC). However, cross-cohort single-cell syntheses of human HSCs have been hampered by three methodological bottlenecks:
1. **Lineage Contamination:** Activated HSCs share contractile and extracellular matrix (ECM) transcripts (*ACTA2*, *PDGFRB*, *COL1A1*) with vascular smooth muscle cells (VSMCs), pericytes, portal fibroblasts (PFs), and mesothelial cells.
2. **Batch Confounding:** Cross-dataset integration without shared healthy reference anchors risks distorting biological state neighbourhoods.
3. **Single-Cell Pseudoreplication:** Treating individual cells rather than biological specimens/donors as independent statistical units inflates false discovery rates in differential expression and compositional testing.

This repository implements a **two-stage, de-confounded bioinformatic framework** across **four human liver 10x Genomics Chromium 3' scRNA-seq cohorts** (`14,237,561` raw droplet barcodes across `53` libraries $\rightarrow$ `494,560` quality-controlled singlets $\rightarrow$ `9,185` pan-liver mesenchymal cells $\rightarrow$ **`5,728` high-purity HSCs** across **`N = 34` biological samples** from **`28` unique donors** and **`42` libraries**).

---

## 2. Two-Stage Analytical Architecture

```text
STAGE 1: INDEPENDENT PER-COHORT PROCESSING & TWO-STAGE LINEAGE PURIFICATION
  ├── Input: 4 Public 10x 3' scRNA-seq Cohorts (GSE136103, GSE243977, GSE282701, GSE166635)
  ├── 3-Tier Replicate Hierarchy: Unique Donor (n=28) -> Biological Sample (N=34) -> Library (n=42)
  ├── Per-Library QC & Scrublet: Detected genes >= 200, <= 99.5% quantile cap, MT <= 20.0% (494,560 singlets)
  ├── Tier 1 (Pan-Liver Mesenchymal Extraction): Leiden (res=0.8) + 6-lineage Z-scoring (9,185 mesenchymal cells)
  └── Tier 2 (Reciprocal Z-Score Gating): Purge VSMC/Pericyte (n=1,396), Portal Fibroblast (n=903), Mesothelial,
      and apply hard zero-UMI lock (PTPRC = 0, EPCAM = 0) + sample size filter (>=10 HSCs; paired HCC >=6)
      ===> OUTPUT: 5,728 High-Purity HSCs across N = 34 Biological Samples (28 Unique Donors)

STAGE 2: HEALTHY-ANCHORED INTEGRATION & DE-CONFOUNDED DOWNSTREAM ANALYSIS
  ├── Artefact Masking & HVG Selection: Mask MT/RPL/RPS/HSP/dissociation/ambient hepatocyte genes -> 2,500 Seurat v3 HVGs
  ├── Healthy-Anchored Harmony Integration (theta = 2.0): Anchored by 17 healthy liver samples (1,978 HSCs)
  ├── 30-D Quantitative Benchmarking: Global iLISI (1.000 -> 2.136, P = 1.16e-10), Unbiased cLISI (P = 0.427, NS)
  ├── Conserved 4-State Resolution: qHSC (+1.11), A1 (+1.05), A2 (+0.76), INF (+0.81); 92.91% Pre/Post agreement (kappa = 0.904)
  ├── Sample-Level Compositional Testing (N = 34): Kruskal-Wallis, Mann-Whitney U, Leave-P15-Out (N=32), Paired Wilcoxon (n=6)
  ├── De-Confounded Donor Pseudobulk DEA (PyDESeq2): 6 within-cohort contrasts + A2-proportion covariate control (711 DEGs)
  ├── Pathway & Purity Audits: Preranked MSigDB Hallmark GSEA (1,000 perms) + Pan-state HBV+ ISG & non-A2 ECM audits
  └── Undirected PAGA Topology: 50x bootstrap stability (80% subsample) + 30x density-controlled subsampling (N=250/compartment)
```

---

## 3. Curated GEO Cohorts & Replicate Hierarchy

All datasets analysed in this study are publicly available from the NCBI Gene Expression Omnibus (GEO):

| GEO Accession | Reference | Tissue Compartment (`tissue_context`) | Clinical Condition (`condition_group`) | Initial Libraries ($n$) | Post-QC Singlets ($n$) | Tier-1 Mesenchymal ($n$) | Retained Donors ($n$) | Retained Bio Samples ($N$) | Retained Libraries ($n$) | Final Purified HSCs ($n$) |
| :--- | :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **GSE136103** | Ramachandran *et al.* | `NonTumor_Liver` | `Healthy` (3), `Alcohol` (2), `NAFLD` (1) | 20 | 59,332 | 2,297 | 6 | 6 | 14 | **1,380** |
| **GSE243977** | Andrews *et al.* | `NonTumor_Liver` | `Healthy` | 19 | 291,229 | 1,587 | 14 | 14 | 14 | **1,008** |
| **GSE282701** | Patient-Paired HCC | `Adjacent_Liver` & `Tumor_Core` | `HBV_neg_Adjacent` (3), `HBV_pos_Adjacent` (3), `HBV_neg_Tumor` (3), `HBV_pos_Tumor` (3) | 12 | 125,967 | 4,982 | 6 (paired) | 12 | 12 | **3,142** |
| **GSE166635** | Meng *et al.* | `Tumor_Core` | `HCC_Tumor` | 2 | 18,032 | 319 | 2 | 2 | 2 | **198** |
| **Total Atlas** | **10x Chromium 3'** | **3 Compartments** | **8 Condition Groups** | **53** | **494,560** | **9,185** | **28 unique** | **34** | **42** | **5,728** |

> **Note on Sample Filtering:** Stage-1 cohort gating initially identified `1,396` HSCs in GSE136103 and `1,280` HSCs in GSE243977 (`1,025` healthy + `255` excluded PSC cells) (see **Supplementary Table S1A** & **Supplementary Fig. S3**). Excluding 6 unpaired biological samples with `< 10` HSCs (`healthy4`, `healthy5`, `cirrhotic4` in GSE136103; `C59`, `C66`, `C69` in GSE243977; totalling `33` cells) yielded **`5,728` HSCs across `N = 34` biological samples**.

---

## 4. Repository Structure

```text
Hepatic-stellate-cell-etiology-scRNAseq/
├── README.md                                  # Study overview, workflow mapping, and execution instructions
├── .gitignore                                 # Excludes large raw matrices, .h5ad binaries, and local caches
├── CITATION.cff                               # Bibliographic citation metadata
├── LICENSE                                    # MIT Open-Source License
├── Makefile                                   # Automation commands for environment setup and data download
├── environment.yml                            # Reproducible Conda environment specification (Python 3.10)
├── requirements.txt                           # Pinned Python package dependencies
├── scripts/
│   └── download_geo_data.sh                   # Automated NCBI GEO downloader and archive extractor
├── src/
│   ├── __init__.py
│   └── hsc_atlas_config.py                    # Centralised relative paths, BMJ palettes, regex, and gene panels
├── data/
│   ├── README_DATA.md                         # Documentation of GEO input files and 3-tier metadata schema
│   ├── raw/                                   # [Git-ignored] Raw 10x matrices downloaded from NCBI GEO
│   ├── processed_hsc/                         # [Git-ignored] Stage-1 purified per-cohort .h5ad objects
│   └── metadata/                              # Curated per-cohort sample sheets (.csv)
├── notebooks/
│   ├── stage1_cohort_purification/            # Independent per-cohort QC, Scrublet & 2-tier reciprocal gating
│   │   ├── 01_GSE136103_HSC_purification.ipynb
│   │   ├── 02_GSE243977_HSC_purification.ipynb
│   │   ├── 03_GSE282701_HSC_purification.ipynb
│   │   └── 04_GSE166635_HSC_purification.ipynb
│   └── stage2_integrated_atlas/               # Healthy-anchored Harmony, 4-state scoring, PyDESeq2, GSEA & PAGA
│       └── 05_Integrated_HSC_Atlas_Analysis.ipynb
└── results/
    ├── tables/                                # Generated CSV tables corresponding to Manuscript & Supplementary Tables
    └── figures/                               # Publication-ready vector PDFs and 300 DPI PNG figures
```

---

## 5. Manuscript-to-Code Mapping

Every figure and table reported in the manuscript and supplementary materials is directly traceable to the notebooks in this repository:

| Manuscript Display Item | Description | Source Notebook | Output File Path (`results/`) |
| :--- | :--- | :--- | :--- |
| **Table 1** & **Supp. Table S1A** | Cohort characteristics, QC funnel, and biological replicate audit ($N=34$, $n=5,728$) | `01`–`04` & `05` | `tables/Table1_Cohort_Biological_Replicate_Audit.csv` |
| **Figure 2** & **Table 2** / **Supp. Table S1C** | Pre-/Post-Harmony UMAPs and 30-D LISI / ASW integration benchmarks | `05_Integrated_HSC_Atlas_Analysis.ipynb` | `figures/Fig2_Harmony_Integration_and_LISI_Benchmark.pdf`<br>`tables/Table2_Rigorous_Integration_Benchmark.csv` |
| **Figure 3** & **Supp. Table S1B** | Conserved 4-state UMAP (`qHSC`, `A1`, `A2`, `INF`), program matrix, lineage purity heatmap & dotplot; stringent gating audit ($n=4,055$) | `05_Integrated_HSC_Atlas_Analysis.ipynb` | `figures/Fig3_Conserved_Four_States_and_Purity_Audit.pdf`<br>`tables/Supplementary_TableS1B_Gating_Sensitivity_Audit.csv` |
| **Figure 4** & **Supp. Table S2 (A–C)** | Sample-level HSC state composition ($N=34$) and non-parametric hypothesis testing | `05_Integrated_HSC_Atlas_Analysis.ipynb` | `figures/Fig4_Sample_Level_HSC_Composition.pdf`<br>`tables/Table3_Sample_Level_HSC_Composition_N34_Verified.csv`<br>`tables/Table3B_Composition_Statistical_Tests.csv` |
| **Figure 5** & **Supp. Table S3A** | De-confounded donor-level pseudobulk PyDESeq2 volcano plots across 6 within-cohort contrasts + `prop_A2` covariate control | `05_Integrated_HSC_Atlas_Analysis.ipynb` | `figures/Fig5_Deconfounded_Pseudobulk_Volcano_Plots.pdf`<br>`tables/Table4_Pseudobulk_PyDESeq2_Rigorous_Deconfounded.csv`<br>`tables/Supplementary_TableS4_PyDESeq2_ControlledFor_PropA2.csv` |
| **Figure 6A** & **Supp. Table S4B** | Preranked MSigDB Hallmark GSEA Normalized Enrichment Score (NES) heatmap across 6 contrasts | `05_Integrated_HSC_Atlas_Analysis.ipynb` | `figures/Fig6A_Pseudobulk_GSEA_Hallmark_Heatmap.pdf`<br>`tables/Table5_Pseudobulk_GSEA_Hallmark_Pathways.csv` |
| **Figure 6B–C**, **Supp. Fig. S1** & **Supp. Table S4A** | Undirected PAGA connectivity graph, 50-run bootstrap stability, and 30-run density-controlled subsampling ($N=250$/compartment) | `05_Integrated_HSC_Atlas_Analysis.ipynb` | `figures/Fig6BC_Undirected_PAGA_and_Bootstrap_Stability.pdf`<br>`figures/Supplementary_FigS1_Density_Controlled_Tissue_PAGA.pdf`<br>`tables/Supplementary_TableS1_Density_Controlled_Tissue_PAGA.csv` |
| **Supp. Fig. S2** & **Supp. Table S3B–C** | Cell-count-invariant within-state (`qHSC + A1`) paired ECM audit & pan-state HBV+ ISG purity heatmap | `05_Integrated_HSC_Atlas_Analysis.ipynb` | `figures/Supplementary_FigS2_Intrinsic_Reprogramming_and_HBV_Purity.pdf`<br>`tables/Supplementary_TableS3_CellCount_Invariant_WithinState_Audit.csv`<br>`tables/Supplementary_TableS5_HBV_ISG_Purity_Across_States.csv` |
| **Supp. Fig. S3 (A–D)** | Stage-1 cohort-independent reciprocal gating and pre-integration four-state resolution | `01`–`04` (`stage1_cohort_purification/`) | `figures/Supplementary_FigS3_Cohort_Independent_Purification.pdf` |

---

## 6. Installation & Reproducibility Guide

### Step 1: Clone the Repository & Create the Conda Environment
```bash
git clone https://github.com/JuliaNguyen0207/Hepatic-stellate-cell-etiology-scRNAseq.git
cd Hepatic-stellate-cell-etiology-scRNAseq

# Create and activate the reproducible Conda environment (Python 3.10)
conda env create -f environment.yml
conda activate hsc-atlas-bmj
```

### Step 2: Download Raw GEO Datasets
Run the automated download script to fetch the supplementary 10x Genomics count matrices from NCBI GEO into `data/raw/`:
```bash
bash scripts/download_geo_data.sh
```
*(See `data/README_DATA.md` for detailed file structures, MD5/size checks, and manual download instructions if behind an institutional firewall).*

### Step 3: Execute the Analytical Pipeline
1. **Stage 1 (Per-Cohort Purification):** Execute notebooks `01` through `04` inside `notebooks/stage1_cohort_purification/` to reproduce quality control, per-library Scrublet doublet removal, and two-stage reciprocal HSC isolation. Purified AnnData objects (`*_HSC_clean.h5ad`) are saved to `data/processed_hsc/`.
2. **Stage 2 (Integrated Atlas & De-Confounded Modelling):** Execute `notebooks/stage2_integrated_atlas/05_Integrated_HSC_Atlas_Analysis.ipynb` to reproduce the 5,728-cell integrated atlas, LISI/ASW benchmarks, sample-level statistics, PyDESeq2 models, Hallmark GSEA, and PAGA topology.

---

## 7. License & Citation

This code is made available under the **MIT License** (see [`LICENSE`](LICENSE)). If you use this pipeline, curated gene signatures, or the integrated human HSC atlas in your research, please cite our manuscript (see [`CITATION.cff`](CITATION.cff)).
