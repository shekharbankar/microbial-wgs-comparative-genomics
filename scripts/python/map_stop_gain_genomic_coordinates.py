#!/usr/bin/env python3

import csv
from pathlib import Path
from Bio import SeqIO

ROOT = Path(".")
INPUT = ROOT / "results/analysis/validated_stop_gain_variants.tsv"
OUTPUT = ROOT / "results/analysis/stop_gain_genomic_coordinates.tsv"
ANNOTATIONS = ROOT / "data/processed/annotations/ncbi_dataset/data"

COMPLEMENT = str.maketrans("ACGT", "TGCA")


def find_cds(accession, locus_tag, gene):
    gbff = ANNOTATIONS / accession / "genomic.gbff"

    if not gbff.exists():
        raise FileNotFoundError(f"GenBank file missing: {gbff}")

    for record in SeqIO.parse(str(gbff), "genbank"):
        for feature in record.features:
            if feature.type != "CDS":
                continue
            if locus_tag not in feature.qualifiers.get("locus_tag", []):
                continue
            if gene not in feature.qualifiers.get("gene", []):
                continue
            return record, feature

    raise ValueError(f"CDS not found: {accession}, {locus_tag}, {gene}")


def map_position(accession, locus_tag, gene, cds_position, expected_base):
    record, feature = find_cds(accession, locus_tag, gene)
    cds = str(feature.extract(record.seq)).upper()
    pos = int(cds_position)

    if not 1 <= pos <= len(cds):
        raise ValueError(f"CDS position out of range: {gene} {pos}")

    cds_base = cds[pos - 1]

    if cds_base != expected_base:
        raise ValueError(
            f"CDS base mismatch: {accession} {gene} position {pos}: "
            f"expected {expected_base}, found {cds_base}"
        )

    if feature.location.strand == 1:
        coordinate = int(feature.location.start) + pos
        strand = "+"
        genomic_base = str(record.seq[coordinate - 1]).upper()
    else:
        coordinate = int(feature.location.end) - pos + 1
        strand = "-"
        genomic_base = str(record.seq[coordinate - 1]).upper()
        genomic_base = genomic_base.translate(COMPLEMENT)

    if genomic_base != cds_base:
        raise ValueError(
            f"Strand/base verification failed: {accession} {gene} "
            f"CDS position {pos}"
        )

    codon_start = ((pos - 1) // 3) * 3
    codon = cds[codon_start:codon_start + 3]

    return {
        "record": record.id,
        "coordinate": coordinate,
        "strand": strand,
        "cds_base": cds_base,
        "genomic_forward_base": str(record.seq[coordinate - 1]).upper(),
        "codon": codon,
        "cds_length": len(cds),
    }


with INPUT.open(newline="") as handle:
    variants = list(csv.DictReader(handle, delimiter="\t"))

results = []

for row in variants:
    gene = row["gene"]
    pos = int(row["cds_position"])

    reference = map_position(
        row["reference_accession"],
        row["reference_locus_tag"],
        gene,
        pos,
        row["reference_base"],
    )

    derivative = map_position(
        row["derivative_accession"],
        row["derivative_locus_tag"],
        gene,
        pos,
        row["derivative_base"],
    )

    if reference["codon"] != row["reference_codon"]:
        raise ValueError(f"Reference codon mismatch: {gene}, CDS position {pos}")

    if derivative["codon"] != row["derivative_codon"]:
        raise ValueError(f"Derivative codon mismatch: {gene}, CDS position {pos}")

    if reference["cds_length"] != derivative["cds_length"]:
        raise ValueError(f"CDS length mismatch: {gene}, CDS position {pos}")

    if reference["cds_base"] == derivative["cds_base"]:
        raise ValueError(f"No nucleotide difference found: {gene}, position {pos}")

    results.append({
        "gene": gene,
        "cds_position": pos,
        "reference_accession": row["reference_accession"],
        "reference_locus_tag": row["reference_locus_tag"],
        "reference_record": reference["record"],
        "reference_genomic_coordinate_1based": reference["coordinate"],
        "reference_strand": reference["strand"],
        "reference_cds_base": reference["cds_base"],
        "reference_genomic_forward_base": reference["genomic_forward_base"],
        "reference_codon": reference["codon"],
        "derivative_accession": row["derivative_accession"],
        "derivative_locus_tag": row["derivative_locus_tag"],
        "derivative_record": derivative["record"],
        "derivative_genomic_coordinate_1based": derivative["coordinate"],
        "derivative_strand": derivative["strand"],
        "derivative_cds_base": derivative["cds_base"],
        "derivative_genomic_forward_base": derivative["genomic_forward_base"],
        "derivative_codon": derivative["codon"],
        "validation_status": "PASS",
    })

if len(results) != 3:
    raise ValueError(f"Expected 3 variants, found {len(results)}")

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

with OUTPUT.open("w", newline="") as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=list(results[0].keys()),
        delimiter="\t",
    )
    writer.writeheader()
    writer.writerows(results)

print(f"Variants mapped and verified: {len(results)}")
for result in results:
    print(
        f"{result['validation_status']}: {result['gene']} "
        f"CDS {result['cds_position']} | "
        f"{result['reference_genomic_coordinate_1based']} "
        f"({result['reference_strand']}) -> "
        f"{result['derivative_genomic_coordinate_1based']} "
        f"({result['derivative_strand']})"
    )

print(f"Output: {OUTPUT}")
