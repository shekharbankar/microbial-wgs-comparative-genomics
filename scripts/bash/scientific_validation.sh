#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

STAMP="$(date +%Y%m%d_%H%M%S)"
OUT="results/verification/scientific_validation_${STAMP}"

mkdir -p "$OUT"

exec > >(tee "$OUT/validation.log") 2>&1

echo "Project: $ROOT"
echo "Commit: $(git rev-parse --short HEAD)"
echo "Date: $(date)"
echo

echo "========== 1. SOFTWARE VERSIONS =========="

python --version
python -c 'import Bio; print("Biopython:", Bio.__version__)'
mafft --version
seqkit version

echo
echo "========== 2. ORIGINAL GENOME ASSEMBLIES =========="

find data/raw/ecoli/nitrofurantoin_six_genomes \
  -type f -name '*.fna' -print | sort

echo
echo "========== 3. FASTA QUALITY AUDIT =========="

python - "$OUT" <<'PY'
from pathlib import Path
from Bio import SeqIO
import csv
import sys

out = Path(sys.argv[1])
roots = [
    Path("data/raw/ecoli/nitrofurantoin_six_genomes"),
    Path("data/processed/annotations"),
]

rows = []

for root in roots:
    if not root.exists():
        continue

    for path in sorted(root.rglob("*.fna")):
        if "cds_from_genomic" in path.name:
            continue

        records = list(SeqIO.parse(str(path), "fasta"))

        if not records:
            print("WARNING: no FASTA records:", path)
            continue

        total = sum(len(r.seq) for r in records)
        gc = sum(
            str(r.seq).upper().count("G")
            + str(r.seq).upper().count("C")
            for r in records
        )
        ns = sum(str(r.seq).upper().count("N") for r in records)

        invalid = sum(
            sum(base not in "ACGTN" for base in str(r.seq).upper())
            for r in records
        )

        rows.append({
            "file": str(path),
            "records": len(records),
            "total_length_bp": total,
            "GC_percent": round(100 * gc / total, 4) if total else 0,
            "N_bases": ns,
            "other_non_ACGTN_bases": invalid,
        })

        print(
            f"{path}: records={len(records)}, "
            f"length={total}, GC={100*gc/total:.3f}%, "
            f"N={ns}, other_invalid={invalid}"
        )

output = out / "fasta_quality_audit.tsv"

with output.open("w", newline="") as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=[
            "file", "records", "total_length_bp",
            "GC_percent", "N_bases", "other_non_ACGTN_bases"
        ],
        delimiter="\t",
    )
    writer.writeheader()
    writer.writerows(rows)

print("\nFASTA audit:", output)
print("Files audited:", len(rows))
PY

echo
echo "========== 4. VALIDATED VARIANT TABLE =========="

python - <<'PY'
import csv
from pathlib import Path

path = Path("results/analysis/validated_stop_gain_variants.tsv")

with path.open(encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f, delimiter="\t")
    rows = list(reader)

print("Candidate records:", len(rows))

for row in rows:
    print("\nGene:", row.get("gene"))
    print("CDS position:", row.get("cds_position"))
    print("Reference codon:", row.get("reference_codon"))
    print("Derivative codon:", row.get("derivative_codon"))
    print("Reference amino acid:", row.get("reference_amino_acid"))
    print("Derivative amino acid:", row.get("derivative_amino_acid"))
    print("Stop gain confirmed:", row.get("stop_gain_confirmed"))
    print("Validation status:", row.get("validation_status"))

    if row.get("equal_cds_lengths") != "True":
        print("REVIEW: unequal CDS lengths or non-True status.")

    if row.get("expected_single_mismatch") != "True":
        print("REVIEW: expected single-mismatch check did not pass.")

    if row.get("expected_codons_match") != "True":
        print("REVIEW: expected codon check did not pass.")
PY

echo
echo "========== 5. VERIFY GENOMIC COORDINATE SCRIPT =========="

sed -n '1,240p' scripts/python/map_stop_gain_genomic_coordinates.py

echo
echo "========== 6. VERIFY VARIANT VALIDATION SCRIPT =========="

sed -n '1,220p' scripts/python/validate_stop_gain_variants.py

echo
echo "========== 7. ALIGNMENT FILE AUDIT =========="

python - <<'PY'
from pathlib import Path
from Bio import AlignIO

root = Path("results/analysis/alignments")

if not root.exists():
    print("No alignments directory found.")
else:
    for path in sorted(root.glob("*.fasta")):
        if path.stat().st_size == 0:
            print("EMPTY ALIGNMENT:", path)
            continue

        try:
            alignment = AlignIO.read(str(path), "fasta")
            print(
                f"{path.name}: sequences={len(alignment)}, "
                f"alignment_length={alignment.get_alignment_length()}"
            )
        except Exception as exc:
            print("ALIGNMENT READ ERROR:", path.name, repr(exc))
PY

echo
echo "========== 8. PHENOTYPE EVIDENCE AUDIT =========="

python - <<'PY'
import csv
from pathlib import Path

path = Path("results/analysis/phenotype_variant_evidence.tsv")

with path.open(encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f, delimiter="\t")
    rows = list(reader)

print("Rows:", len(rows))

for row in rows:
    print(
        row.get("strain"),
        "|", row.get("gene"),
        "| aerobic MIC:", row.get("reported_aerobic_mic_ug_ml"),
        "| anaerobic MIC:", row.get("reported_anaerobic_mic_ug_ml"),
        "| DOI:", row.get("doi"),
    )

print(
    "\nImportant: this verifies the recorded table, not the published "
    "paper's underlying values. Those require primary-source review."
)
PY

echo
echo "========== 9. TECHNICAL VALIDATION =========="

python - <<'PY'
import ast
from pathlib import Path
import csv
import sys

errors = []

for path in sorted(Path("scripts/python").rglob("*.py")):
    try:
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except Exception as exc:
        errors.append(f"Python syntax: {path}: {exc}")

tables = [
    Path("results/qc/six_genome_qc.tsv"),
    Path("results/analysis/validated_stop_gain_variants.tsv"),
    Path("results/analysis/variant_biological_interpretation.tsv"),
    Path("results/analysis/phenotype_variant_evidence.tsv"),
    Path("results/analysis/final_variant_summary.tsv"),
]

for path in tables:
    if not path.exists() or path.stat().st_size == 0:
        errors.append(f"Missing/empty table: {path}")
        continue

    with path.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.reader(f, delimiter="\t"))

    if not rows:
        errors.append(f"No rows: {path}")
        continue

    width = len(rows[0])

    for line, row in enumerate(rows[1:], start=2):
        if len(row) != width:
            errors.append(
                f"Column mismatch: {path}, line {line}"
            )

if errors:
    print("\nVALIDATION ISSUES:")
    for error in errors:
        print("FAIL:", error)
    sys.exit(1)

print("Python syntax: PASS")
print("Required TSV structure: PASS")
PY

echo
echo "========== 10. SUMMARY =========="

cat > "$OUT/interpretation.md" <<'EOF'
# Scientific Validation Notes

This run records preliminary technical checks of the microbial
comparative-genomics repository.

FASTA parsing and sequence statistics do not establish genome identity,
assembly completeness, or contamination status.

Codon comparisons must be interpreted alongside the original annotated
coding sequences and the corresponding genomic coordinates.

Published antimicrobial susceptibility measurements must be checked
against the primary source. They must not be represented as laboratory
measurements generated by this project.

Sequence-validated candidate stop-gain variants do not, by themselves,
prove causation of nitrofurantoin resistance.

Full reproduction requires rerunning the original analysis steps from
documented inputs and comparing the regenerated outputs with the saved
results.
EOF

echo "Audit directory: $OUT"
echo
echo "========== GIT STATUS =========="

git diff --check
git status --short

echo
echo "SCIENTIFIC VALIDATION AUDIT COMPLETED."
echo "No original analysis outputs were overwritten."
