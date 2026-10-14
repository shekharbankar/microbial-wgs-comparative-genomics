import json
import csv

input_file = "data/metadata/ecoli_candidates.jsonl"
output_file = "data/metadata/ecoli_candidates_summary.csv"

fields = [
    "Accession",
    "Strain",
    "Genome_length_bp",
    "GC_percent",
    "Assembly_level",
    "Sequencing_technology",
    "Completeness_percent",
    "Contamination_percent",
    "BioProject"
]

with open(input_file, "r") as infile, open(output_file, "w", newline="") as outfile:
    writer = csv.DictWriter(outfile, fieldnames=fields)
    writer.writeheader()

    for line in infile:
        record = json.loads(line)

        assembly_info = record.get("assembly_info", {})
        biosample = assembly_info.get("biosample", {})
        assembly_stats = record.get("assembly_stats", {})
        checkm = record.get("checkm_info", {})
        organism = record.get("organism", {})

        row = {
            "Accession": record.get("accession", ""),
            "Strain": organism.get("infraspecific_names", {}).get("strain", ""),
            "Genome_length_bp": assembly_stats.get("total_sequence_length", ""),
            "GC_percent": assembly_stats.get("gc_percent", ""),
            "Assembly_level": assembly_info.get("assembly_level", ""),
            "Sequencing_technology": assembly_info.get("sequencing_tech", ""),
            "Completeness_percent": checkm.get("completeness", ""),
            "Contamination_percent": checkm.get("contamination", ""),
            "BioProject": assembly_info.get("bioproject_accession", "")
        }

        writer.writerow(row)

print("Candidate summary saved to:", output_file)
