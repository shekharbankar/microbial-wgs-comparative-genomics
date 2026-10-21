#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

STAMP="$(date +%Y%m%d_%H%M%S)"
BACKUP="reports/verification_backup_${STAMP}"

mkdir -p "$BACKUP" reports results/verification

LOG="reports/full_verification_${STAMP}.log"
exec > >(tee "$LOG") 2>&1

echo "=================================================="
echo "MICROBIAL WGS - FULL VERIFICATION"
echo "=================================================="
echo "Date: $(date)"
echo "Repository: $ROOT"
echo "Commit: $(git rev-parse --short HEAD)"
echo

echo "========== 1. ENVIRONMENT =========="

python --version
python -c "import Bio; print('Biopython:', Bio.__version__)"
mafft --version
seqkit version
git --version

echo
echo "========== 2. BACK UP MODIFIED OUTPUTS =========="

for file in \
    results/analysis/phenotype_variant_evidence.tsv \
    results/analysis/variant_biological_interpretation.tsv \
    results/analysis/final_variant_summary.tsv \
    results/analysis/comparative_genomics_report.md \
    results/analysis/validated_stop_gain_variants.tsv
do
    if [[ -f "$file" ]]; then
        mkdir -p "$BACKUP/$(dirname "$file")"
        cp -p "$file" "$BACKUP/$file"
        echo "Backed up: $file"
    fi
done

echo
echo "Backup directory: $BACKUP"

echo
echo "========== 3. CHECK GIT AND REPOSITORY =========="

git status --short
git log -5 --oneline

echo
echo "========== 4. CHECK INPUT FILES =========="

python - <<'PY'
from pathlib import Path

for folder in ("data/raw", "data/processed", "data/metadata",
               "scripts/python", "scripts/bash", "results/qc",
               "results/analysis", "reports", "docs"):
    p = Path(folder)
    if p.exists():
        files = [x for x in p.rglob("*") if x.is_file()]
        print(f"{folder}: {len(files)} files")
    else:
        print(f"MISSING DIRECTORY: {folder}")

print("\nPotential genome sequence files:")
for folder in (Path("data/raw"), Path("data/processed")):
    if folder.exists():
        for p in folder.rglob("*"):
            if p.is_file() and p.suffix.lower() in {
                ".fasta", ".fa", ".fna", ".fas", ".gbff", ".gbk"
            }:
                print(f"{p} | {p.stat().st_size} bytes")
PY

echo
echo "========== 5. VERIFY PYTHON SYNTAX =========="

python - <<'PY'
import ast
from pathlib import Path
import sys

files = sorted(Path("scripts/python").rglob("*.py"))
errors = []

for p in files:
    try:
        ast.parse(p.read_text(encoding="utf-8"), filename=str(p))
        print("PASS:", p)
    except Exception as e:
        print("FAIL:", p, repr(e))
        errors.append(p)

print("Python scripts checked:", len(files))

if errors:
    sys.exit(1)
PY

echo
echo "========== 6. VERIFY EXISTING TABLE STRUCTURE =========="

python - <<'PY'
import csv
from pathlib import Path
import sys

files = [
    "results/qc/six_genome_qc.tsv",
    "results/analysis/validated_stop_gain_variants.tsv",
    "results/analysis/variant_biological_interpretation.tsv",
    "results/analysis/phenotype_variant_evidence.tsv",
    "results/analysis/final_variant_summary.tsv",
]

failed = False

for name in files:
    p = Path(name)

    if not p.is_file():
        print("MISSING:", name)
        continue

    try:
        with p.open(encoding="utf-8-sig", newline="") as f:
            rows = list(csv.reader(f, delimiter="\t"))

        if not rows:
            print("EMPTY:", name)
            failed = True
            continue

        width = len(rows[0])
        bad = [
            i + 1 for i, row in enumerate(rows[1:], start=1)
            if len(row) != width
        ]

        if bad:
            print("FAIL:", name, "bad rows:", bad[:10])
            failed = True
        else:
            print(
                "PASS:", name,
                "| data rows:", len(rows) - 1,
                "| columns:", width
            )
    except Exception as e:
        print("ERROR:", name, repr(e))
        failed = True

if failed:
    print("At least one table needs review.")
PY

echo
echo "========== 7. CHECK FASTA FILES =========="

python - <<'PY'
from pathlib import Path
from Bio import SeqIO

extensions = {".fasta", ".fa", ".fna", ".fas"}
count = 0

for folder in (Path("data/raw"), Path("data/processed")):
    if not folder.exists():
        continue

    for p in sorted(folder.rglob("*")):
        if not p.is_file() or p.suffix.lower() not in extensions:
            continue

        count += 1
        records = 0
        bases = 0
        invalid = 0
        ambiguous = 0

        try:
            for rec in SeqIO.parse(str(p), "fasta"):
                records += 1
                seq = str(rec.seq).upper()
                bases += len(seq)
                invalid += sum(c not in "ACGTN" for c in seq)
                ambiguous += seq.count("N")

            if records == 0:
                print("FAIL: No FASTA records:", p)
            else:
                print(
                    f"{p}: records={records}, bases={bases}, "
                    f"N={ambiguous}, non-ACGTN={invalid}"
                )
        except Exception as e:
            print("READ ERROR:", p, repr(e))

print("FASTA files inspected:", count)
if count == 0:
    print("WARNING: No FASTA files found in expected data directories.")
PY

echo
echo "========== 8. CHECK MANIFESTS AND ACCESSIONS =========="

find data/metadata -maxdepth 2 -type f 2>/dev/null | sort || true

if [[ -f data/metadata/nitrofurantoin_six_genome_manifest.tsv ]]; then
    echo
    cat data/metadata/nitrofurantoin_six_genome_manifest.tsv
else
    echo "Six-genome manifest not found at the expected path."
fi

echo
echo "========== 9. CHECK ANALYSIS SCRIPT ARGUMENTS =========="

for script in scripts/python/*.py; do
    [[ -f "$script" ]] || continue

    echo
    echo "--- $script ---"
    grep -nE 'ArgumentParser|add_argument|sys.argv|argparse' \
        "$script" | head -25 || true
done

echo
echo "========== 10. REVIEW ANALYSIS DEPENDENCIES =========="

for file in environment.yml README.md; do
    if [[ -f "$file" ]]; then
        echo
        echo "--- $file ---"
        sed -n '1,160p' "$file"
    else
        echo "MISSING: $file"
    fi
done

echo
echo "========== 11. VERIFY ALIGNMENT FILES =========="

find results/analysis/alignments -maxdepth 1 -type f \
    -printf '%f | %s bytes\n' 2>/dev/null | sort || true

echo
echo "========== 12. REPRODUCIBILITY STATUS =========="

cat > results/verification/reproducibility_status.md <<'REPORT'
# Reproducibility Verification Status

This file records preliminary repository checks.

Passing Python syntax checks confirms that scripts parse, not that their
scientific results are correct.

Passing TSV structure checks confirms consistent column counts, not that
the underlying measurements or biological interpretations are correct.

Passing FASTA parsing confirms that sequence records can be read, not that
the assemblies are biologically complete or contamination-free.

Full reproducibility requires identifying the original inputs, checking
software versions and command parameters, rerunning the original workflow,
and comparing regenerated outputs with the recorded results.

Candidate sequence variants must not be described as experimentally proven
causes of antimicrobial resistance without appropriate supporting evidence.
REPORT

echo "Preliminary status written."

echo
echo "========== 13. FINAL GIT CHECK =========="

git diff --check
git status --short

echo
echo "=================================================="
echo "VERIFICATION FINISHED"
echo "=================================================="
echo "Log: $LOG"
echo "Backup: $BACKUP"
echo
echo "No scientific analysis was automatically overwritten."
echo "Review this log before deciding which analyses to rerun."
