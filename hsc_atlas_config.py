"""
Centralized configuration, portable path resolver, publication palettes,
and locked gene signature panels for the Human Hepatic Stellate Cell Atlas.

All parameters in this module strictly match the Methods and Supplementary Methods
of Nguyen & Le ("A lineage-purified atlas of human hepatic stellate cells reveals
a conserved four-state architecture and niche-specific reprogramming in
hepatocellular carcinoma").
"""

import os
from pathlib import Path
from typing import Dict, List

# ==============================================================================
# 1. REPRODUCIBLE SEED & PORTABLE DIRECTORY RESOLUTION
# ==============================================================================
RANDOM_STATE: int = 0

# Automatically resolve repository root regardless of current working directory
REPO_ROOT: Path = Path(__file__).resolve().parent.parent

DATA_DIR: Path = Path(os.environ.get("HSC_ATLAS_DATA_DIR", REPO_ROOT / "data"))
RAW_DATA_DIR: Path = Path(os.environ.get("HSC_ATLAS_RAW_DIR", DATA_DIR / "raw"))
PROCESSED_HSC_DIR: Path = Path(os.environ.get("HSC_ATLAS_PROCESSED_DIR", DATA_DIR / "processed_hsc"))
METADATA_DIR: Path = DATA_DIR / "metadata"

RESULTS_DIR: Path = Path(os.environ.get("HSC_ATLAS_RESULTS_DIR", REPO_ROOT / "results"))
FIGURES_DIR: Path = RESULTS_DIR / "figures"
TABLES_DIR: Path = RESULTS_DIR / "tables"

for _d in [PROCESSED_HSC_DIR, METADATA_DIR, FIGURES_DIR, TABLES_DIR]:
    _d.mkdir(parents=True, exist_ok=True)

DATASETS: List[str] = ["GSE136103", "GSE243977", "GSE166635", "GSE282701"]

# ==============================================================================
# 2. QUALITY CONTROL & SCRUBLET PARAMETERS (SUPPLEMENTARY METHODS 1.2)
# ==============================================================================
QC_PARAMS = {
    "min_genes": 200,            # Preserves low-RNA quiescent HSCs (qHSCs)
    "upper_quantile": 0.995,     # Cohort-level upper cap on total UMIs and detected genes
    "max_mt_pct": 20.0,          # Maximum mitochondrial UMI fraction (%)
    "min_cells_per_gene": 3,     # Minimum cells expressing a gene per cohort
    "target_sum": 10000,         # Library-size normalization target sum
}

SCRUBLET_PARAMS = {
    "min_counts": 2,
    "min_cells": 3,
    "min_gene_variability_pctl": 85,
    "n_prin_comps_max": 30,
    "sim_doublet_ratio": 2.0,
    "expected_rate_slope": 0.008 / 1000.0,
    "expected_rate_min": 0.01,
    "expected_rate_max": 0.10,
    "random_state": RANDOM_STATE,
}

# ==============================================================================
# 3. TWO-STAGE RECIPROCAL HSC PURIFICATION PANELS (SUPPLEMENTARY METHODS 1.3)
# ==============================================================================
# Tier 1: Whole-Liver Pan-Mesenchymal Extraction (6 Lineage Panels)
TIER1_LINEAGE_PANELS: Dict[str, List[str]] = {
    "HSC_Mesenchymal": [
        "PDGFRB", "DCN", "RGS5", "ECM1", "RELN", "DES",
        "LRAT", "CYGB", "COL1A1", "COL1A2", "COL3A1", "LUM",
    ],
    "Hepatocyte": ["ALB", "CPS1", "APOA1", "APOA2", "CYP3A4", "HNF4A"],
    "Cholangiocyte": ["EPCAM", "KRT19", "KRT7", "SOX9", "ANXA4"],
    "Endothelial": ["PECAM1", "KDR", "VWF", "STAB2", "CLDN5", "FCN2"],
    "Myeloid": ["CD68", "MARCO", "CD163", "LYZ", "C1QA", "VSIG4"],
    "Lymphoid": ["PTPRC", "CD3D", "CD3E", "NKG7", "GNLY", "CD79A", "MS4A1"],
}

TIER1_THRESHOLDS = {
    "min_z_mesenchymal": 1.0,
    "min_margin_over_non_mes": 0.5,
}

# Tier 2: Within-Mesenchymal Reciprocal Z-Score Gating (5 Competing Panels)
TIER2_PURIFICATION_PANELS: Dict[str, List[str]] = {
    "HSC_Core": [
        "LRAT", "RBP1", "CYGB", "RELN", "COLEC11", "COLEC10",
        "ACTA2", "TAGLN", "CNN1", "DCN", "LUM", "COL1A1",
        "COL1A2", "COL3A1", "RGS5", "DES", "GFAP", "PDGFRB",
        "SPARC", "IGFBP3", "TIMP1",
    ],
    "VSMC_Pericyte": ["MYH11", "NOTCH3", "CSPG4", "MCAM", "SMTN", "MYLK"],
    "Portal_Fibroblast": ["CLEC3B", "CD34", "COL15A1", "THY1", "OSR1", "MFAP4"],
    "Mesothelial": ["UPK3B", "MSLN", "UPK1B"],
    "Lineage_Contam": ["PTPRC", "LYZ", "CD68", "PECAM1", "VWF", "KDR", "ALB", "EPCAM", "TTR"],
}

TIER2_EXCLUSION_THRESHOLDS = {
    "z_vsmc_max": 1.0,           # Exclude if z_VSMC > 1.0 and z_VSMC > z_HSC
    "z_pf_max": 1.0,             # Exclude if z_PF > 1.0 and z_PF > z_HSC
    "z_meso_max": 1.5,           # Exclude if z_Meso > 1.5 and z_Meso > z_HSC
    "z_contam_max": 1.8,         # Exclude if z_Contam > 1.8
    "zero_umi_genes": ["PTPRC", "EPCAM"],
    "stringent_vsmc_pf_cap": 0.5 # Sensitivity audit threshold (n = 4,055 HSCs)
}

# ==============================================================================
# 4. HVG MASKING REGEX & FOUR FUNCTIONAL HSC PROGRAMMES (SUPP. METHODS 1.4)
# ==============================================================================
HVG_ARTEFACT_REGEX: str = (
    r"^(MT-|MTRNR|RPL|RPS|MRP|HSP|DNAJ|FOS|JUN|EGR1|MKI67|TOP2A|"
    r"ALB$|TTR$|APOA|APOB|APOC|HP$|HPR$|FGA$|FGB$|FGG$|CYP|SERPINA1$|CRP$|ORM1$)"
)

HSC_FOUR_STATE_PROGRAMMES: Dict[str, List[str]] = {
    "qHSC": [
        "LRAT", "RBP1", "RELN", "CYGB", "COLEC11", "COLEC10", "VIPR1",
        "HHIP", "NGFR", "GFAP", "PPARG", "ADGRL3", "SPARCL1", "ECM1",
    ],
    "A1": [
        "ACTA2", "TAGLN", "MYL9", "TPM2", "CNN1", "CALD1",
        "MYLK", "VCL", "CRYAB", "SOD3", "PLN",
    ],
    "A2": [
        "COL1A1", "COL1A2", "COL3A1", "LUM", "TIMP1", "SERPINE1",
        "SPARC", "FN1", "VCAN", "POSTN", "LOXL2", "MMP2",
    ],
    "INF": [
        "CCL2", "CXCL8", "CXCL1", "CXCL2", "CXCL12", "IL6", "ICAM1",
        "VCAM1", "NFKBIA", "TNFAIP3", "CCL20", "SOD2", "SOCS3", "IRF1",
    ],
}

# ==============================================================================
# 5. COMPOSITE SIGNATURES FOR WITHIN-STATE AUDITS (SUPP. METHODS 1.5)
# ==============================================================================
WITHIN_STATE_AUDIT_SIGNATURES: Dict[str, List[str]] = {
    "Desmoplastic_ECM": [
        "COL1A1", "COL1A2", "COL3A1", "POSTN", "SPARC",
        "THY1", "SERPINE1", "TIMP1", "LGALS1",
    ],
    "Quiescence_Core": ["LRAT", "RELN", "RBP1", "COLEC11", "VIPR1"],
    "Anabolic_MYC_UPR": [
        "MYC", "NPM1", "ENO1", "LDHA", "CYCS",
        "COX5A", "ATP5F1A", "HSPA5", "HSP90B1", "XBP1",
    ],
}

# ==============================================================================
# 6. BMJ PUBLICATION COLOUR PALETTES
# ==============================================================================
PALETTE_STATE: Dict[str, str] = {
    "qHSC": "#2b83ba",  # Quiescent / Retinoid-storing (Blue)
    "A1":   "#fdae61",  # Contractile Myofibroblast (Orange)
    "A2":   "#d7191c",  # Profibrogenic / Desmoplastic ECM (Red)
    "INF":  "#abdda4",  # Immunomodulatory / Inflammatory (Green)
}

PALETTE_DS: Dict[str, str] = {
    "GSE136103": "#1f78b4",
    "GSE243977": "#33a02c",
    "GSE166635": "#ff7f00",
    "GSE282701": "#e31a1c",
}

PALETTE_COND: Dict[str, str] = {
    "Healthy":          "#2b83ba",
    "NAFLD":            "#fdae61",
    "Alcohol":          "#fe9929",
    "HBV_neg_Adjacent": "#74c476",
    "HBV_pos_Adjacent": "#006d2c",
    "HCC_Tumor":        "#984ea3",
    "HBV_neg_Tumor":    "#fb6a4a",
    "HBV_pos_Tumor":    "#a50f15",
}