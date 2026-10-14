#!/usr/bin/env python3

"""Validate candidate nfsA/nfsB stop-gain variants against NCBI GenBank CDS records."""

import csv
from pathlib import Path

from Bio import SeqIO
from Bio.Seq import Seq

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ANNOTATION_DIR = (
    PROJECT_ROOT / "data/processed/annotations/ncbi_dataset/data"
)
OUTPUT = PROJECT_ROOT / "results/analysis/validated_stop_gain_variants.tsv"

VARIANTS = [
    {
        "reference_accession": "GCF_000597845.1",
        "reference_locus_tag": "BU34_RS01915",
        "derivative_accession": "GCF_000599645.1",
        "derivative_locus_tag": "CF61_RS25690",
        "gene": "nfsA",
        "cds_position": 298,
        "expected_reference_codon": "CAG",
        "expected_derivative_codon": "TAG",
    },
    {
        "reference_accession": "GCF_000599665.1",
        "reference_locus_tag": "CF58_RS07610",
        "derivative_accession": "GCF_000599685.1",
        "derivative_locus_tag": "CF59_RS07610",
        "gene": "nfsA",
        "cds_position": 58,
        "expected_reference_codon": "GAA",
        "expected_derivative_codon": "TAA",
    },
    {
        "reference_accession": "GCF_000599665.1",
        "reference_locus_tag": "CF58_RS06210",
        "derivative_accession": "GCF_000599685.1",
        "derivative_locus_tag": "CF59_RS06250",
        "gene": "nfsB",
        "cds_position": 169,
        "expected_reference_codon": "AAA",
        "expected_derivative_codon": "TAA",
    },
]


def get_cds(accession, locus_tag):
    """Return an annotated CDS sequence and its GenBank record metadata."""
    gbff = ANNOTATION_DIR / accession / "genomic.gbff"

    for record in SeqIO.parse(gbff, "genbank"):
        for feature in record.features:
            if feature.type != "CDS":
                continue

            if locus_tag in feature.qualifiers.get("locus_tag", []):
                sequence = str(feature.extract(record.seq)).upper()
                return sequence, record.id, str(feature.location)

    raise ValueError(f"CDS not found: {accession}, {locus_tag}")


def translate_codon(codon):
    """Translate a complete three-base codon."""
    if len(codon) != 3:
        return "INVALID"
    return str(Seq(codon).translate())


def main():
    results = []

    for variant in VARIANTS:
        ref_seq, ref_record, ref_location = get_cds(
            variant["reference_accession"],
            variant["reference_locus_tag"],
        )
        alt_seq, alt_record, alt_location = get_cds(
            variant["derivative_accession"],
            variant["derivative_locus_tag"],
        )

        pos = variant["cds_position"]

        if pos < 1 or pos + 1 > len(ref_seq) or pos + 1 > len(alt_seq):
            raise ValueError(
                f"CDS position {pos} is outside a sequence for {variant['gene']}"
            )

        start = ((pos - 1) // 3) * 3
        ref_codon = ref_seq[start:start + 3]
        alt_codon = alt_seq[start:start + 3]

        ref_base = ref_seq[pos - 1]
        alt_base = alt_seq[pos - 1]

        mismatches = [
            i + 1
            for i, (ref, alt) in enumerate(zip(ref_seq, alt_seq))
            if ref != alt
        ]

        same_length = len(ref_seq) == len(alt_seq)
        one_mismatch_at_expected_position = mismatches == [pos]

        codons_match_expected = (
            ref_codon == variant["expected_reference_codon"]
            and alt_codon == variant["expected_derivative_codon"]
        )

        stop_gain_confirmed = (
            translate_codon(ref_codon) != "*"
            and translate_codon(alt_codon) == "*"
        )

        passed = (
            same_length
            and one_mismatch_at_expected_position
            and codons_match_expected
            and stop_gain_confirmed
        )

        results.append({
            "gene": variant["gene"],
            "cds_position": pos,
            "reference_accession": variant["reference_accession"],
            "reference_locus_tag": variant["reference_locus_tag"],
            "reference_record": ref_record,
            "reference_location": ref_location,
            "reference_base": ref_base,
            "reference_codon": ref_codon,
            "reference_amino_acid": translate_codon(ref_codon),
            "derivative_accession": variant["derivative_accession"],
            "derivative_locus_tag": variant["derivative_locus_tag"],
            "derivative_record": alt_record,
            "derivative_location": alt_location,
            "derivative_base": alt_base,
            "derivative_codon": alt_codon,
            "derivative_amino_acid": translate_codon(alt_codon),
            "reference_cds_length": len(ref_seq),
            "derivative_cds_length": len(alt_seq),
            "full_cds_mismatch_count": len(mismatches),
            "mismatch_positions": ",".join(map(str, mismatches)),
            "equal_cds_lengths": same_length,
            "expected_single_mismatch": one_mismatch_at_expected_position,
            "expected_codons_match": codons_match_expected,
            "stop_gain_confirmed": stop_gain_confirmed,
            "validation_status": "PASS" if passed else "REVIEW",
        })

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(results[0].keys()),
            delimiter="\t",
        )
        writer.writeheader()
        writer.writerows(results)

    print("Candidate stop-gain validation")
    print("=" * 38)

    for row in results:
        print(
            f"{row['gene']} CDS position {row['cds_position']}: "
            f"{row['reference_codon']} -> {row['derivative_codon']} | "
            f"CDS mismatches={row['full_cds_mismatch_count']} | "
            f"{row['validation_status']}"
        )

    print(f"\nVariants checked: {len(results)}")
    print(f"PASS: {sum(r['validation_status'] == 'PASS' for r in results)}")
    print(f"REVIEW: {sum(r['validation_status'] == 'REVIEW' for r in results)}")
    print(f"Detailed results: {OUTPUT.relative_to(PROJECT_ROOT)}")
    print(
        "\nNote: sequence validation does not establish that a variant "
        "causes nitrofurantoin resistance."
    )


if __name__ == "__main__":
    main()
