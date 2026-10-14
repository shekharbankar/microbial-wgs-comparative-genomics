from pathlib import Path
import csv
from Bio import SeqIO

alignment_dir = Path("results/analysis/alignments")
output_dir = Path("results/analysis")

alignment_files = sorted(
    p for p in alignment_dir.glob("*_aligned.fasta")
    if p.name.startswith(("ST540_parental_vs_", "ST2747_parental_vs_"))
)

if len(alignment_files) != 8:
    raise SystemExit(
        f"Expected 8 pairwise alignment files, found {len(alignment_files)}"
    )

summary_rows = []
detail_rows = []

for path in alignment_files:
    records = list(SeqIO.parse(path, "fasta"))

    if len(records) != 2:
        raise ValueError(f"{path}: expected 2 sequences, found {len(records)}")

    parental = str(records[0].seq).upper()
    derivative = str(records[1].seq).upper()

    if len(parental) != len(derivative):
        raise ValueError(f"{path}: aligned sequence lengths do not match")

    compared = 0
    mismatches = 0
    gap_columns = 0

    for position, (p_base, d_base) in enumerate(
        zip(parental, derivative), start=1
    ):
        if p_base == "-" or d_base == "-":
            gap_columns += 1
            continue

        compared += 1

        if p_base != d_base:
            mismatches += 1
            detail_rows.append({
                "comparison": path.stem,
                "alignment_position": position,
                "parental_base": p_base,
                "derivative_base": d_base,
                "change": f"{p_base}>{d_base}",
            })

    identity = (
        round((compared - mismatches) / compared * 100, 3)
        if compared else None
    )

    summary_rows.append({
        "comparison": path.stem,
        "parental_record": records[0].id,
        "derivative_record": records[1].id,
        "alignment_length_bp": len(parental),
        "comparable_positions": compared,
        "nucleotide_mismatches": mismatches,
        "gap_columns": gap_columns,
        "identity_percent_among_comparable_positions": identity,
    })

summary_path = output_dir / "pairwise_alignment_summary.tsv"
details_path = output_dir / "pairwise_mismatch_details.tsv"

with summary_path.open("w", newline="") as handle:
    writer = csv.DictWriter(
        handle, fieldnames=summary_rows[0].keys(), delimiter="\t"
    )
    writer.writeheader()
    writer.writerows(summary_rows)

detail_fields = [
    "comparison", "alignment_position",
    "parental_base", "derivative_base", "change"
]

with details_path.open("w", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=detail_fields, delimiter="\t")
    writer.writeheader()
    writer.writerows(detail_rows)

print("Pairwise comparisons summarized:", len(summary_rows))
print("Total nucleotide mismatches:", len(detail_rows))
print("Summary saved to:", summary_path)
print("Mismatch details saved to:", details_path)
