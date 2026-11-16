#!/usr/bin/env bash
# ==============================================================================
# Automated NCBI GEO Data Downloader & Extractor
# Study: Lineage-Purified Human Hepatic Stellate Cell Atlas
# Cohorts: GSE136103, GSE243977, GSE282701, GSE166635
# Usage: bash scripts/download_geo_data.sh [TARGET_RAW_DIR]
# ==============================================================================

set -euo pipefail

# Resolve repository root relative to this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
RAW_BASE_DIR="${1:-${REPO_ROOT}/data/raw}"

echo "======================================================================"
echo " Starting NCBI GEO Data Retrieval for Human HSC Atlas"
echo " Target raw data directory: ${RAW_BASE_DIR}"
echo "======================================================================"

mkdir -p "${RAW_BASE_DIR}"

# Helper function to download a file with resume support (curl or wget)
download_file() {
    local url="$1"
    local dest="$2"
    if [ -f "${dest}" ]; then
        echo "  [SKIP] File already exists: ${dest}"
        return 0
    fi
    echo "  [DOWNLOADING] ${url}"
    if command -v curl >/dev/null 2>&1; then
        curl -L --retry 5 --retry-delay 5 -C - -o "${dest}" "${url}"
    elif command -v wget >/dev/null 2>&1; then
        wget -c --tries=5 -O "${dest}" "${url}"
    else
        echo "ERROR: Neither 'curl' nor 'wget' was found on your system." >&2
        exit 1
    fi
}

# ------------------------------------------------------------------------------
# 1. GSE136103 (Ramachandran et al. - Healthy, Alcohol & NAFLD Cirrhosis)
#    Expected input: Per-sample 10x 3' files (*genes.tsv.gz, *barcodes.tsv.gz, *matrix.mtx.gz)
#    Note: Stage-1 notebook automatically excludes peripheral blood (blood*) and mouse* files.
# ------------------------------------------------------------------------------
echo ""
echo "[1/4] Processing Cohort: GSE136103..."
DIR_136103="${RAW_BASE_DIR}/GSE136103"
mkdir -p "${DIR_136103}"
TAR_136103="${DIR_136103}/GSE136103_RAW.tar"
URL_136103="https://ftp.ncbi.nlm.nih.gov/geo/series/GSE136nnn/GSE136103/suppl/GSE136103_RAW.tar"

download_file "${URL_136103}" "${TAR_136103}"
echo "  [EXTRACTING] ${TAR_136103} into ${DIR_136103}/"
tar -xf "${TAR_136103}" -C "${DIR_136103}"

# ------------------------------------------------------------------------------
# 2. GSE243977 (Andrews et al. - Normal Donor Liver 3' scRNA-seq Anchor Cohort)
#    Expected input: Per-sample 10x 3' files (*_SC_3pr*matrix.mtx.gz, features.tsv.gz, barcodes.tsv.gz)
#     plus GSE243977_series_matrix.txt.gz for clinical etiology metadata verification.
# ------------------------------------------------------------------------------
echo ""
echo "[2/4] Processing Cohort: GSE243977..."
DIR_243977="${RAW_BASE_DIR}/GSE243977"
mkdir -p "${DIR_243977}"
TAR_243977="${DIR_243977}/GSE243977_RAW.tar"
URL_243977="https://ftp.ncbi.nlm.nih.gov/geo/series/GSE243nnn/GSE243977/suppl/GSE243977_RAW.tar"
MAT_243977="${DIR_243977}/GSE243977_series_matrix.txt.gz"
URL_MAT_243977="https://ftp.ncbi.nlm.nih.gov/geo/series/GSE243nnn/GSE243977/matrix/GSE243977_series_matrix.txt.gz"

download_file "${URL_243977}" "${TAR_243977}"
download_file "${URL_MAT_243977}" "${MAT_243977}"
echo "  [EXTRACTING] ${TAR_243977} into ${DIR_243977}/"
tar -xf "${TAR_243977}" -C "${DIR_243977}"

# ------------------------------------------------------------------------------
# 3. GSE282701 (Patient-Paired HBV+ and HBV- HCC Tumour Core & Adjacent Liver)
#    Expected input: 12 paired libraries (P10-P15, T and P fractions)
# ------------------------------------------------------------------------------
echo ""
echo "[3/4] Processing Cohort: GSE282701..."
DIR_282701="${RAW_BASE_DIR}/GSE282701"
mkdir -p "${DIR_282701}"
TAR_282701="${DIR_282701}/GSE282701_RAW.tar"
URL_282701="https://ftp.ncbi.nlm.nih.gov/geo/series/GSE282nnn/GSE282701/suppl/GSE282701_RAW.tar"

download_file "${URL_282701}" "${TAR_282701}"
echo "  [EXTRACTING] ${TAR_282701} into ${DIR_282701}/"
tar -xf "${TAR_282701}" -C "${DIR_282701}"

# ------------------------------------------------------------------------------
# 4. GSE166635 (Meng et al. - Primary HCC Tumour Core Libraries HCC1 & HCC2)
#    Expected input: GSM5076749_HCC1 and GSM5076750_HCC2 10x matrices
# ------------------------------------------------------------------------------
echo ""
echo "[4/4] Processing Cohort: GSE166635..."
DIR_166635="${RAW_BASE_DIR}/GSE166635"
mkdir -p "${DIR_166635}"
TAR_166635="${DIR_166635}/GSE166635_RAW.tar"
URL_166635="https://ftp.ncbi.nlm.nih.gov/geo/series/GSE166nnn/GSE166635/suppl/GSE166635_RAW.tar"

download_file "${URL_166635}" "${TAR_166635}"
echo "  [EXTRACTING] ${TAR_166635} into ${DIR_166635}/"
tar -xf "${TAR_166635}" -C "${DIR_166635}"

echo ""
echo "======================================================================"
echo " [SUCCESS] All 4 GEO cohorts downloaded and extracted into:"
echo "   - ${DIR_136103}"
echo "   - ${DIR_243977}"
echo "   - ${DIR_282701}"
echo "   - ${DIR_166635}"
echo " Note: If any inner sample archives are packaged as .tar.gz directories,"
echo " the Stage-1 preprocessing notebooks automatically detect and parse them."
echo "======================================================================"