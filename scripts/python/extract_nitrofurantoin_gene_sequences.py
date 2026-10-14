#!/usr/bin/env python3

"""Extract nfsA and nfsB CDS records from six NCBI genome annotations."""

import csv
from pathlib import Path

from Bio import SeqIO

PROJECT_ROOT = Path(__file__).resolve().parents[2]

MANIFEST = PROJECT_ROOT / "data/metadata/nitrofurantoin_six_genome_manifest.tsv"
ANNOTATION_DIR = PROJECT_ROOT / "data/processed/annotations/ncbi_dataset/data"
STATUS_TABLE = PROJECT_ROOT / "results/analysis/nitrofurantoin_gene_annotation_status.tsv"
OUTPUT = PROJECT_ROOT / "results/analysis/nitrofurantoin_nfsA_nfsB_sequences.fasta"

TARGET_GENES = {"nfsA", "nfsB"}


def parse_header(description):
    """Read bracketed key=value fields from an NCBI CDS FASTA header."""
    attributes = {}

    for item in description.split("[")[1:]:
        if "]" not in item:
            continue
        field = item.split("]", 1)[0]
        if "=" in field:
            key, value = field.split("=", 1)
            attributes[key] = value

    return attributes


def main():
    with MANIFEST.open(newline="") as handle:
        samples = list(csv.DictReader(handle, delimiter="\t"))

    with STATUS_TABLE.open(newline="") as handle:
        status_rows = list(csv.DictReader(handle, delimiter="\t"))

    status_lookup = {
        (row["assembly_accession"], row["gene"]): row["annotation_status"]
        for row in status_rows
    }

    output_records = []
    seen = set()

    for sample in samples:
        accession = sample["assembly_accession"]
        cds_file = ANNOTATION_DIR / accession / "cds_from_genomic.fna"

        if not cds_file.is_file():
            raise FileNotFoundError(f"Missing CDS FASTA: {cds_file}")

        for record in SeqIO.parse(cds_file, "fasta"):
            attributes = parse_header(record.description)
            gene = attributes.get("gene")

            if gene not in TARGET_GENES:
                continue

            key = (accession, gene)
            if key in seen:
                raise ValueError(f"Duplicate {gene} sequence for {accession}")
            seen.add(key)

            locus_tag = attributes.get("locus_tag", "unknown")
            status = status_lookup.get(key, "status_not_found")
            pseudo = attributes.get("pseudo", "false").lower() == "true"
            partial = attributes.get("partial", "not_marked")

            record.id = (
                f"{accession}|{sample['sample_name']}|{gene}"
                f"|{status}|locus_tag={locus_tag}"
                f"|pseudo={str(pseudo).lower()}|partial={partial}"
            )
            record.description = ""
            output_records.append(record)

    expected = {
        (sample["assembly_accession"], gene)
        for sample in samples
        for gene in TARGET_GENES
    }

    if seen != expected:
        missing = sorted(expected - seen)
        extra = sorted(seen - expected)
        raise ValueError(f"Sequence set mismatch. Missing={missing}; extra={extra}")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    SeqIO.write(output_records, OUTPUT, "fasta")

    print(f"Genomes checked: {len(samples)}")
    print(f"Gene sequences extracted: {len(output_records)}")
    print(f"Output saved to: {OUTPUT.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
