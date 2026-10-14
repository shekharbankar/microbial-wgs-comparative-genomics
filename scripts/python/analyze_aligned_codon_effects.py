from pathlib import Path
from Bio import SeqIO
from Bio.Seq import Seq
import csv

ALIGNMENT_DIR = Path("results/analysis/alignments")
OUTPUT_DIR = Path("results/analysis")

COMPARISONS = [
    ("GCF_000597845.1", "C1-ST540-P", "GCF_000599625.1", "ST540a"),
    ("GCF_000597845.1", "C1-ST540-P", "GCF_000599645.1", "ST540an"),
    ("GCF_000599665.1", "ST2747-Parental", "GCF_000599685.1", "ST2747a"),
    ("GCF_000599665.1", "ST2747-Parental", "GCF_000599705.1", "ST2747an"),
]

variant_rows = []
summary_rows = []

def translate_codon(sequence, position):
    start = ((position - 1) // 3) * 3
    codon = sequence[start:start + 3]
    if len(codon) != 3 or any(base not in "ACGT" for base in codon):
        return codon, "", "CODON_REQUIRES_REVIEW"
    return codon, str(Seq(codon).translate()), ""

for gene in ("nfsA", "nfsB"):
    alignment_file = ALIGNMENT_DIR / f"{gene}_aligned.fasta"
    records = {}

    for record in SeqIO.parse(alignment_file, "fasta"):
        parts = record.id.split("|")
        if len(parts) >= 3:
            records[(parts[0], parts[1], parts[2])] = str(record.seq).upper()

    for ref_acc, ref_name, alt_acc, alt_name in COMPARISONS:
        ref_aligned = records.get((ref_acc, ref_name, gene))
        alt_aligned = records.get((alt_acc, alt_name, gene))
        comparison = f"{ref_name}_vs_{alt_name}"
        mismatch_count = 0
        gap_columns = 0

        if ref_aligned is None or alt_aligned is None:
            summary_rows.append({
                "comparison": comparison,
                "gene": gene,
                "status": "SEQUENCE_NOT_FOUND",
                "nucleotide_mismatches": "",
                "gap_columns": "",
            })
            continue

        if len(ref_aligned) != len(alt_aligned):
            summary_rows.append({
                "comparison": comparison,
                "gene": gene,
                "status": "ALIGNMENT_LENGTH_MISMATCH",
                "nucleotide_mismatches": "",
                "gap_columns": "",
            })
            continue

        ref_seq = ref_aligned.replace("-", "")
        alt_seq = alt_aligned.replace("-", "")
        ref_position = 0
        alt_position = 0

        for col, (rb, ab) in enumerate(zip(ref_aligned, alt_aligned), start=1):
            if rb != "-":
                ref_position += 1
            if ab != "-":
                alt_position += 1

            if rb == "-" or ab == "-":
                if rb != ab:
                    gap_columns += 1
                continue

            if rb == ab or rb not in "ACGT" or ab not in "ACGT":
                continue

            mismatch_count += 1
            ref_codon, ref_aa, ref_note = translate_codon(ref_seq, ref_position)
            alt_codon, alt_aa, alt_note = translate_codon(alt_seq, alt_position)

            if ref_note or alt_note:
                effect = "CODON_REQUIRES_REVIEW"
            elif ref_aa != "*" and alt_aa == "*":
                effect = "STOP_GAINED"
            elif ref_aa == "*" and alt_aa != "*":
                effect = "STOP_LOST"
            elif ref_aa == alt_aa:
                effect = "SYNONYMOUS"
            else:
                effect = "AMINO_ACID_CHANGE"

            note = ""
            if alt_name == "ST540a":
                note = "NCBI-annotated partial 3-prime CDS; interpret cautiously"

            variant_rows.append({
                "comparison": comparison,
                "gene": gene,
                "alignment_position_1based": col,
                "reference_cds_position_1based": ref_position,
                "derivative_cds_position_1based": alt_position,
                "reference_base": rb,
                "derivative_base": ab,
                "reference_codon": ref_codon,
                "derivative_codon": alt_codon,
                "reference_aa": ref_aa,
                "derivative_aa": alt_aa,
                "effect": effect,
                "note": note,
            })

        summary_rows.append({
            "comparison": comparison,
            "gene": gene,
            "status": "REVIEW_PARTIAL_CDS" if alt_name == "ST540a" else "OK",
            "nucleotide_mismatches": mismatch_count,
            "gap_columns": gap_columns,
        })

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

variant_fields = [
    "comparison", "gene", "alignment_position_1based",
    "reference_cds_position_1based", "derivative_cds_position_1based",
    "reference_base", "derivative_base", "reference_codon",
    "derivative_codon", "reference_aa", "derivative_aa", "effect", "note",
]
summary_fields = [
    "comparison", "gene", "status", "nucleotide_mismatches", "gap_columns",
]

with (OUTPUT_DIR / "aligned_codon_variant_details.tsv").open("w", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=variant_fields, delimiter="\t")
    writer.writeheader()
    writer.writerows(variant_rows)

with (OUTPUT_DIR / "aligned_codon_comparison_summary.tsv").open("w", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=summary_fields, delimiter="\t")
    writer.writeheader()
    writer.writerows(summary_rows)

print(f"Comparisons summarized: {len(summary_rows)}")
print(f"Nucleotide variant rows: {len(variant_rows)}")
print("Saved: results/analysis/aligned_codon_variant_details.tsv")
print("Saved: results/analysis/aligned_codon_comparison_summary.tsv")
print("Interpretation: candidate sequence effects, not proof of resistance causation.")
