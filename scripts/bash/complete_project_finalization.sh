#!/usr/bin/env bash

set -Eeuo pipefail

ROOT="$HOME/GitHub_Projects/microbial-wgs-comparative-genomics"
cd "$ROOT"

mkdir -p scripts/bash docs reports results/verification

# Activate the required environment.
source "$HOME/miniforge3/etc/profile.d/conda.sh"
conda activate ngs

STAMP="$(date +%Y%m%d_%H%M%S)"
AUDIT="results/verification/finalization_${STAMP}"
mkdir -p "$AUDIT"

exec > >(tee "$AUDIT/finalization.log") 2>&1

echo "=================================================="
echo "MICROBIAL WGS - COMPLETE PROJECT FINALIZATION"
echo "=================================================="
echo "Project: $ROOT"
echo "Date: $(date)"
echo "Commit before run: $(git rev-parse --short HEAD)"
echo

# --------------------------------------------------
# 1. SOFTWARE CHECK
# --------------------------------------------------

echo "========== 1. SOFTWARE CHECK =========="

python --version
python -c 'import Bio; print("Biopython:", Bio.__version__)'
mafft --version
seqkit version

# --------------------------------------------------
# 2. VERIFY REQUIRED FILES
# --------------------------------------------------

echo
echo "========== 2. REQUIRED FILES =========="

REQUIRED=(
    "README.md"
    "environment.yml"
    "docs/reproducibility.md"
    "results/qc/six_genome_qc.tsv"
    "results/analysis/validated_stop_gain_variants.tsv"
    "results/analysis/variant_biological_interpretation.tsv"
    "results/analysis/phenotype_variant_evidence.tsv"
    "results/analysis/final_variant_summary.tsv"
    "scripts/python/validate_stop_gain_variants.py"
    "scripts/python/map_stop_gain_genomic_coordinates.py"
)

MISSING=0

for FILE in "${REQUIRED[@]}"; do
    if [[ -s "$FILE" ]]; then
        echo "PASS: $FILE"
    else
        echo "MISSING OR EMPTY: $FILE"
        MISSING=1
    fi
done

if [[ "$MISSING" -ne 0 ]]; then
    echo "STOP: Resolve missing required files before finalization."
    exit 1
fi

# --------------------------------------------------
# 3. VERIFY VARIANTS FROM ANNOTATED CDS
# --------------------------------------------------

echo
echo "========== 3. REVALIDATE VARIANTS =========="

python scripts/python/validate_stop_gain_variants.py

echo
echo "========== 4. REVALIDATE GENOMIC COORDINATES =========="

python scripts/python/map_stop_gain_genomic_coordinates.py

# --------------------------------------------------
# 5. REGENERATE GENE FASTA AND ALIGNMENTS
# --------------------------------------------------

echo
echo "========== 5. GENE EXTRACTION AND ALIGNMENT =========="

python scripts/python/extract_nitrofurantoin_gene_sequences.py

# Align only if the extracted sequence files exist.
# Never pass an already-aligned FASTA back into MAFFT as raw input.

ALIGN_DIR="results/analysis/alignments"
mkdir -p "$ALIGN_DIR"

if [[ -s results/analysis/nfsA_sequences.fasta ]]; then
    mafft --auto results/analysis/nfsA_sequences.fasta         > "$ALIGN_DIR/nfsA_aligned.fasta"
    echo "Generated nfsA alignment."
else
    echo "NOTICE: nfsA_sequences.fasta was not generated at the expected path."
fi

if [[ -s results/analysis/nfsB_sequences.fasta ]]; then
    mafft --auto results/analysis/nfsB_sequences.fasta         > "$ALIGN_DIR/nfsB_aligned.fasta"
    echo "Generated nfsB alignment."
else
    echo "NOTICE: nfsB_sequences.fasta was not generated at the expected path."
fi

# --------------------------------------------------
# 6. TECHNICAL VALIDATION
# --------------------------------------------------

echo
echo "========== 6. PYTHON SYNTAX AND TSV CHECKS =========="

python - <<'PY'
import ast
import csv
import sys
from pathlib import Path

root = Path(".")
errors = []

scripts = sorted((root / "scripts/python").rglob("*.py"))

for path in scripts:
    try:
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except Exception as exc:
        errors.append(f"Python syntax error: {path}: {exc}")

print(f"Python scripts checked: {len(scripts)}")

tables = [
    "results/qc/six_genome_qc.tsv",
    "results/analysis/validated_stop_gain_variants.tsv",
    "results/analysis/variant_biological_interpretation.tsv",
    "results/analysis/phenotype_variant_evidence.tsv",
    "results/analysis/final_variant_summary.tsv",
    "results/analysis/stop_gain_genomic_coordinates.tsv",
]

for name in tables:
    path = root / name

    if not path.exists() or path.stat().st_size == 0:
        errors.append(f"Missing or empty table: {name}")
        continue

    with path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.reader(handle, delimiter="\t"))

    if not rows:
        errors.append(f"No rows: {name}")
        continue

    width = len(rows[0])

    if len(set(rows[0])) != width:
        errors.append(f"Duplicate column names: {name}")

    for line_number, row in enumerate(rows[1:], start=2):
        if len(row) != width:
            errors.append(
                f"Column mismatch: {name}, line {line_number}"
            )

    print(
        f"CHECKED: {name} | "
        f"{len(rows)-1} records | {width} columns"
    )

variant_path = root / "results/analysis/validated_stop_gain_variants.tsv"

if variant_path.exists():
    with variant_path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))

    expected = {
        ("nfsA", "298", "CAG", "TAG"),
        ("nfsA", "58", "GAA", "TAA"),
        ("nfsB", "169", "AAA", "TAA"),
    }

    observed = {
        (
            row.get("gene"),
            row.get("cds_position"),
            row.get("reference_codon"),
            row.get("derivative_codon"),
        )
        for row in rows
    }

    if observed != expected:
        errors.append(
            "Candidate variant set differs from the expected three records."
        )

    for row in rows:
        if row.get("validation_status") != "PASS":
            errors.append(
                f"Variant needs review: {row.get('gene')} "
                f"CDS {row.get('cds_position')}"
            )

if errors:
    print("\nVALIDATION FAILED:")
    for error in errors:
        print("FAIL:", error)
    sys.exit(1)

print("\nPASS: Python syntax, TSV structures and candidate checks.")
PY

# --------------------------------------------------
# 7. INDEPENDENT ALIGNMENT FILE CHECK
# --------------------------------------------------

echo
echo "========== 7. ALIGNMENT CHECK =========="

python - <<'PY'
from pathlib import Path
from Bio import AlignIO

directory = Path("results/analysis/alignments")

if not directory.exists():
    print("NOTICE: alignment directory not found.")
else:
    files = sorted(directory.glob("*aligned.fasta"))

    if not files:
        print("NOTICE: no aligned FASTA files found.")

    for path in files:
        if path.stat().st_size == 0:
            raise SystemExit(f"FAIL: empty alignment: {path}")

        try:
            alignment = AlignIO.read(str(path), "fasta")
        except Exception as exc:
            raise SystemExit(f"FAIL: {path}: {exc}")

        print(
            f"PASS: {path.name} | "
            f"{len(alignment)} sequences | "
            f"{alignment.get_alignment_length()} aligned positions"
        )
PY

# --------------------------------------------------
# 8. FINAL SCIENTIFIC REPORT
# --------------------------------------------------

echo
echo "========== 8. CREATE FINAL REPORT =========="

cat > reports/final_scientific_validation.md <<'EOF'
# Final Scientific Validation Report

## Project

Comparative whole-genome analysis of selected Escherichia coli
isolates, focusing on nfsA and nfsB sequence variants associated
with nitrofurantoin susceptibility.

## Candidate variants

| Gene | CDS position (1-based) | Reference codon | Derivative codon | Predicted protein change |
|---|---:|---|---|---|
| nfsA | 298 | CAG | TAG | Q100* |
| nfsA | 58 | GAA | TAA | E20* |
| nfsB | 169 | AAA | TAA | K57* |

These are candidate premature-stop variants identified through
coding-sequence comparisons. The validation tables record the
nucleotide and codon checks performed against the annotated CDSs.

## Biological interpretation

The observed codon changes are consistent with predicted premature
translation termination in NfsA or NfsB.

Sequence validation alone does not demonstrate loss of enzyme
activity or establish that an individual variant causes resistance.
The nfsA and nfsB candidates found in the same derivative must not
be interpreted as having independently established effects.

## Phenotype evidence

MIC values in the phenotype evidence table are recorded as published
measurements, not as measurements produced by this computational
project. Their exact values, strain labels, assay conditions and
citation must be checked against the original publication before
submission.

## Quality control and reproducibility

The workflow checks include software versions, input-file presence,
annotated-CDS variant validation, genomic-coordinate mapping,
Python syntax and TSV structure.

A successful technical check does not by itself establish full
reproducibility. Full reproduction requires running the documented
workflow from the original inputs and checking the regenerated
outputs against the reported results.

## Key files

- 
