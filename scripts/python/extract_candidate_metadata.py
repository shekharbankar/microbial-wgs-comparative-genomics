import json
import csv

input_file = "data/metadata/ecoli_candidates_detailed.jsonl"
output_file = "data/metadata/ecoli_candidates_review.csv"


def get_attributes(record):
    attributes = {}

    biosample = record.get("assembly_info", {}).get("biosample", {})
    for item in biosample.get("attributes", []):
        name = item.get("name", "").strip().lower().replace(" ", "_")
        value = item.get("value", "")
        if name:
            attributes[name] = value

    return attributes


fields = [
    "Accession",
    "Strain",
    "BioProject",
    "BioSample",
    "Genome_length_bp",
    "GC_percent",
    "Assembly_level",
    "Completeness_percent",
    "Contamination_percent",
    "Isolation_source",
    "Collection_date",
    "Geographic_location",
    "Serotype",
    "Phenotype",
]

with open(input_file, encoding="utf-8") as infile, \
     open(output_file, "w", newline="", encoding="utf-8") as outfile:

    writer = csv.DictWriter(outfile, fieldnames=fields)
    writer.writeheader()

    for line in infile:
        if not line.strip():
            continue

        record = json.loads(line)
        assembly = record.get("assembly_info", {})
        stats = record.get("assembly_stats", {})
        checkm = record.get("checkm_info", {})
        organism = record.get("organism", {})
        biosample = assembly.get("biosample", {})
        attrs = get_attributes(record)

        strain = organism.get("infraspecific_names", {}).get("strain", "")

        row = {
            "Accession": record.get("accession", ""),
            "Strain": strain,
            "BioProject": assembly.get("bioproject_accession", ""),
            "BioSample": biosample.get("accession", ""),
            "Genome_length_bp": stats.get("total_sequence_length", ""),
            "GC_percent": stats.get("gc_percent", ""),
            "Assembly_level": assembly.get("assembly_level", ""),
            "Completeness_percent": checkm.get("completeness", ""),
            "Contamination_percent": checkm.get("contamination", ""),
            "Isolation_source": attrs.get("isolation_source", ""),
            "Collection_date": attrs.get("collection_date", ""),
            "Geographic_location": attrs.get("geo_loc_name", ""),
            "Serotype": attrs.get("serotype", ""),
            "Phenotype": attrs.get("phenotype", ""),
        }

        writer.writerow(row)

print("Metadata review table saved to:", output_file)
