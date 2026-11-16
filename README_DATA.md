# Data Documentation & Three-Tier Metadata Schema

This document specifies the exact input data formats, library inclusion/exclusion rules, and three-tier biological replicate hierarchy enforced across the study.

---

## 1. Expected Raw Directory Layout (`data/raw/`)

Running `bash scripts/download_geo_data.sh` populates `data/raw/` with four cohort subdirectories containing 10x Genomics Chromium 3' count matrices (`matrix.mtx.gz`, `features.tsv.gz` or `genes.tsv.gz`, and `barcodes.tsv.gz`):

```text
data/raw/
├── GSE136103/
│   └── GSM4041150_healthy1_cd45+_{matrix.mtx.gz, genes.tsv.gz, barcodes.tsv.gz} ...
├── GSE243977/
│   ├── GSE243977_series_matrix.txt.gz
│   └── GSM7804044_C41_NPC_SC_3pr_{matrix.mtx.gz, features.tsv.gz, barcodes.tsv.gz} ...
├── GSE282701/
│   └── GSM*_P10_T / GSM*_P10_P ... (12 patient-paired Tumour [T] and Adjacent [P] libraries)
└── GSE166635/
    └── GSM5076749_HCC1 / GSM5076750_HCC2 ... (2 primary HCC tumour core libraries)
```

> **Custom Raw Data Location:** If your raw GEO files are stored on an external drive or institutional server, you do not need to move them. Simply set the environment variable `HSC_ATLAS_RAW_DIR=/path/to/your/geo_data` before launching JupyterLab, and `src/hsc_atlas_config.py` will automatically route all notebooks to that directory.

---

## 2. Cohort-Specific Library Curation Rules (Stage 1)

To prevent cross-species, cross-tissue, and cross-chemistry batch confounding, strict library filtering is applied prior to quality control (see **Supplementary Methods 1.1** and **Supplementary Table S1A**):

1. **GSE136103 (Ramachandran *et al.*):**
   * **Retained:** 20 human liver 10x 3' libraries (10 $\text{CD45}^+$ and 10 $\text{CD45}^-$ FACS fractions; `62,210` raw cells) from 10 donors (5 healthy, 2 alcohol-related cirrhosis, 2 MASLD/NAFLD cirrhosis, 1 PBC).
   * **Excluded:** Peripheral blood (`blood*`) and murine (`mouse*`) libraries. The single PBC donor (`cirrhotic5`) had only a $\text{CD45}^+$ leucocyte fraction yielding `0` HSCs and was excluded from downstream HSC analyses.
2. **GSE243977 (Andrews *et al.*):**
   * **Retained:** 19 human liver 10x 3' single-cell libraries (`_SC_3pr`; 3 NPC-enriched and 16 whole-liver dissociations; `14,008,320` raw unfiltered droplet barcodes).
   * **Excluded:** Hepatic perfusate (`flush`), 5' chemistry (`_SC_5pr`), single-nucleus (`_SN`), and primary sclerosing cholangitis (`PSC`) fractions (only healthy donor samples were retained for the integrated healthy anchor).
3. **GSE282701 (Patient-Paired HCC):**
   * **Retained:** All 12 patient-paired resection libraries (`141,842` raw cells) from 6 HCC patients—3 $\text{HBV}^+$ (`P10`, `P12`, `P13`) and 3 $\text{HBV}^-$ (`P11`, `P14`, `P15`)—each contributing matched primary tumour core (`T`, `Tumor_Core`) and adjacent non-tumour liver (`P`, `Adjacent_Liver`).
4. **GSE166635 (Meng *et al.*):**
   * **Retained:** 2 primary HCC tumour core libraries (`GSM5076749_HCC1`, `GSM5076750_HCC2`; `25,189` raw cells) from 2 treatment-naive donors (`HCC1`, `HCC2`).

---

## 3. Three-Tier Biological Replicate Hierarchy (Stage 2)

To eliminate single-cell pseudoreplication and prevent technical FACS splits from being treated as independent biological replicates, all cells are indexed under a three-tier metadata schema:

| Hierarchy Tier | Column Name in `adata.obs` | Final Atlas Count | Definition & Role in Statistical Modelling |
| :--- | :--- | :---: | :--- |
| **Tier 1: Sequencing Library** | `sample_id` | $n = 42$ | Individual 10x Chromium sequencing library (GSM accession). Unit of execution for **Scrublet doublet removal**. |
| **Tier 2: Biological Sample** | `sample_bio_id` | $N = 34$ | Unique physical tissue specimen (`global_patient_id__tissue_context`). Technical FACS libraries from the same donor and tissue (`CD45+` and `CD45-` in GSE136103) are collapsed into a single `sample_bio_id`. Unit of observation for **LISI benchmarking**, **compositional testing**, and **pseudobulk UMI aggregation**. |
| **Tier 3: Unique Donor** | `global_patient_id` | $n = 28$ | Unique human individual (`dataset_id_patient_id`). Used as a blocking factor (`~ global_patient_id + tissue_context`) in **patient-paired PyDESeq2 models** and Wilcoxon signed-rank tests. |