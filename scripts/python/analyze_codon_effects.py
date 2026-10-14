from Bio import SeqIO
from Bio.Seq import Seq
from pathlib import Path
import csv

INPUT = Path("results/analysis/nitrofurantoin_nfsA_nfsB_sequences.fasta")
OUTPUT = Path("results/analysis/codon_effect_summary.tsv")

records = {}
for record in SeqIO.parse(INPUT, "fasta"):
    parts = record.id.split("|")
    if len(parts) >= 3:
        accession, strain, gene = parts[:3]
        records[(accession, strain, gene)] = str(record.seq).upper()

comparisons = [
    ("GCF_000597845.1", "C1-ST540-P", "GCF_000599625.1", "ST540a"),
    ("GCF_000597845.1", "C1-ST540-P", "GCF_000599645.1", "ST540an"),
    ("GCF_000599665.1", "ST2747-Parental", "GCF_000599685.1", "ST2747a"),
    ("GCF_000599665.1", "ST2747-Parental", "GCF_000599705.1", "ST2747an"),
]

rows = []

for ref_acc, ref_name, alt_acc, alt_name in comparisons:
    for gene in ("nfsA", "nfsB"):
        ref = records.get((ref_acc, ref_name, gene))
        alt = records.get((alt_acc, alt_name, gene))

        if ref is None or alt is None:
            rows.append({
                "comparison": f"{ref_name}_vs_{alt_name}",
                "gene": gene,
                "status": "SEQUENCE_NOT_FOUND",
                "cds_position_1based": "",
                "reference_codon": "",
                "alternate_codon": "",
                "reference_aa": "",
                "alternate_aa": "",
                "effect": "",
            })
            continue

        if len(ref) != len(alt):
            rows.append({
                "comparison": f"{ref_name}_vs_{alt_name}",
                "gene": gene,
                "status": "LENGTH_DIFFERENCE_REQUIRES_ALIGNMENT",
                "cds_position_1based": "",
                "reference_codon": "",
                "alternate_codon": "",
                "reference_aa": "",
                "alternate_aa": "",
                "effect": "",
            })
            continue

        for i, (rbase, abase) in enumerate(zip(ref, alt)):
            if rbase == abase:
                continue

            codon_start = (i // 3) * 3
            ref_codon = ref[codon_start:codon_start + 3]
            alt_codon = alt[codon_start:codon_start + 3]

            if len(ref_codon) != 3 or len(alt_codon) != 3:
                ref_aa = alt_aa = ""
                effect = "INCOMPLETE_CODON"
            else:
                ref_aa = str(Seq(ref_codon).translate())
                alt_aa = str(Seq(alt_codon).translate())

                if alt_aa == "*" and ref_aa != "*":
                    effect = "STOP_GAINED"
                elif ref_aa == alt_aa:
                    effect = "SYNONYMOUS"
                else:
                    effect = "AMINO_ACID_CHANGE"

            rows.append({
                "comparison": f"{ref_name}_vs_{alt_name}",
                "gene": gene,
                "status": "OK_CDS_COORDINATES",
                "cds_position_1based": i + 1,
                "reference_codon": ref_codon,
                "alternate_codon": alt_codon,
                "reference_aa": ref_aa,
                "alternate_aa": alt_aa,
                "effect": effect,
            })

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
fields = [
    "comparison", "gene", "status", "cds_position_1based",
    "reference_codon", "alternate_codon",
    "reference_aa", "alternate_aa", "effect"
]

with OUTPUT.open("w", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t")
    writer.writeheader()
    writer.writerows(rows)

print(f"Comparisons configured: {len(comparisons) * 2}")
print(f"Variant rows written: {len(rows)}")
print(f"Saved to: {OUTPUT}")
print("Note: unequal-length sequences require alignment-aware analysis.")
