#!/usr/bin/env python3

"""Basic reproducible QC summary for the six nitrofurantoin study genomes."""

import csv
from pathlib import Path

from Bio import SeqIO
from Bio.SeqUtils import gc_fraction

PROJECT_ROOT = Path(__file__).resolve().parents[2]
GENOME_DIR = (
    PROJECT_ROOT
    / "data/raw/ecoli/nitrofurantoin_six_genomes/ncbi_dataset/data"
)
MANIFEST = PROJECT_ROOT / "data/metadata/nitrofurantoin_six_genome_manifest.tsv"
OUTPUT = PROJECT_ROOT / "results/qc/six_genome_qc.tsv"


def main():
    with MANIFEST.open(newline="") as handle:
        samples = list(csv.DictReader(handle, delimiter="\t"))

    rows = []

    for sample in samples:
        accession = sample["assembly_accession"]
        fasta_files = list((GENOME_DIR / accession).glob("*_genomic.fna"))

        if len(fasta_files) != 1:
            raise ValueError(
                f"{accession}: expected exactly one genomic FASTA, "
                f"found {len(fasta_files)}"
            )

        records = list(SeqIO.parse(fasta_files[0], "fasta"))

        if not records:
            raise ValueError(f"{accession}: FASTA contains no sequences")

        sequence = "".join(str(record.seq).upper() for record in records)
        valid_bases = sum(sequence.count(base) for base in "ACGT")
        gc_bases = sequence.count("G") + sequence.count("C")
        n_bases = sequence.count("N")
        other_ambiguous = len(sequence) - valid_bases - n_bases

        rows.append({
            "assembly_accession": accession,
            "sample_name": sample["sample_name"],
            "strain": sample["strain"],
            "condition": sample["condition"],
            "chromosome_records": len(records),
            "total_length_bp": len(sequence),
            "GC_percent": round(gc_fraction(sequence) * 100, 2),
            "N_bases": n_bases,
            "other_non_ACGTN_bases": other_ambiguous,
            "sequence_integrity_check": (
                "PASS"
                if valid_bases + n_bases == len(sequence)
                else "REVIEW"
            ),
        })

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = list(rows[0].keys())

    with OUTPUT.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)

    print(f"Genomes analysed: {len(rows)}")
    print(f"QC summary saved to: {OUTPUT.relative_to(PROJECT_ROOT)}")
    print()
    with OUTPUT.open() as handle:
        print(handle.read())


if __name__ == "__main__":
    main()
