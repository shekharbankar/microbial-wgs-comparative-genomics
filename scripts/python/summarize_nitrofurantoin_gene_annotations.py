#!/usr/bin/env python3

"""Summarize NCBI annotations for nfsA and nfsB across six genomes."""

import csv
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

MANIFEST = (
    PROJECT_ROOT
    / "data/metadata/nitrofurantoin_six_genome_manifest.tsv"
)

ANNOTATION_DIR = (
    PROJECT_ROOT
    / "data/processed/annotations/ncbi_dataset/data"
)

OUTPUT = (
    PROJECT_ROOT
    / "results/analysis/nitrofurantoin_gene_annotation_status.tsv"
)

TARGET_GENES = {"nfsA", "nfsB"}


def parse_attributes(attribute_text):
    """Convert GFF3 attributes into a dictionary."""
    attributes = {}

    for item in attribute_text.strip().split(";"):
        if "=" in item:
            key, value = item.split("=", 1)
            attributes[key] = value

    return attributes


def main():
    with MANIFEST.open(newline="") as handle:
        samples = list(csv.DictReader(handle, delimiter="\t"))

    rows = []

    for sample in samples:
        accession = sample["assembly_accession"]
        gff_file = ANNOTATION_DIR / accession / "genomic.gff"

        if not gff_file.is_file():
            raise FileNotFoundError(f"Missing annotation file: {gff_file}")

        found_genes = set()

        with gff_file.open() as handle:
            for line in handle:
                if line.startswith("#") or not line.strip():
                    continue

                fields = line.rstrip("\n").split("\t")

                if len(fields) != 9:
                    continue

                feature_type = fields[2]

                if feature_type not in {"gene", "pseudogene"}:
                    continue

                attributes = parse_attributes(fields[8])
                gene_name = attributes.get("gene") or attributes.get("Name")

                if gene_name not in TARGET_GENES:
                    continue

                if gene_name in found_genes:
                    raise ValueError(
                        f"Duplicate {gene_name} gene entry for {accession}"
                    )

                found_genes.add(gene_name)

                is_pseudogene = (
                    feature_type == "pseudogene"
                    or attributes.get("pseudo", "").lower() == "true"
                    or attributes.get("gene_biotype") == "pseudogene"
                )

                if is_pseudogene:
                    status = "pseudogene_annotated"
                elif attributes.get("gene_biotype") == "protein_coding":
                    status = "protein_coding_annotated"
                else:
                    status = "other_or_uncertain_annotation"

                rows.append({
                    "assembly_accession": accession,
                    "sample_name": sample["sample_name"],
                    "strain": sample["strain"],
                    "condition": sample["condition"],
                    "nitrofurantoin_MIC_ug_per_mL":
                        sample["nitrofurantoin_MIC_ug_per_mL"],
                    "gene": gene_name,
                    "annotation_status": status,
                    "start": fields[3],
                    "end": fields[4],
                    "strand": fields[6],
                    "locus_tag": attributes.get("locus_tag", ""),
                    "gff_feature_type": feature_type,
                })

        missing = TARGET_GENES - found_genes

        if missing:
            raise ValueError(
                f"{accession}: expected genes not found in GFF: "
                f"{', '.join(sorted(missing))}"
            )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "assembly_accession",
        "sample_name",
        "strain",
        "condition",
        "nitrofurantoin_MIC_ug_per_mL",
        "gene",
        "annotation_status",
        "start",
        "end",
        "strand",
        "locus_tag",
        "gff_feature_type",
    ]

    with OUTPUT.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
            delimiter="\t",
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Genomes analysed: {len(samples)}")
    print(f"Gene records summarised: {len(rows)}")
    print(f"Report saved to: {OUTPUT.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
