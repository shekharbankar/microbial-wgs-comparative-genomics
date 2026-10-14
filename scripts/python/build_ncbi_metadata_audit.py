import csv
import json
from pathlib import Path

ROOT = Path(".")
ORIGINAL = ROOT / "data/metadata/ecoli_all_candidates_review.csv"
NCBI_REPORT = ROOT / "results/metadata_audit/ncbi_assembly_report.jsonl"
OUTPUT = ROOT / "results/metadata_audit/ncbi_candidate_metadata_audit.csv"

MISSING_VALUES = {
    "", "missing", "not applicable", "na", "n/a",
    "none", "unknown", "not provided"
}


def clean(value):
    if value is None:
        return ""
    value = str(value).strip()
    if value.lower() in MISSING_VALUES:
        return ""
    return value


def get_attributes(record):
    assembly = record.get("assembly_info", {})
    biosample = assembly.get("biosample", {})
    attributes = {}

    for item in biosample.get("attributes", []):
        name = item.get("name", "").strip().lower()
        value = clean(item.get("value"))
        if name and value:
            attributes[name] = value

    return assembly, biosample, attributes


with ORIGINAL.open(newline="", encoding="utf-8-sig") as f:
    original_rows = list(csv.DictReader(f))

with NCBI_REPORT.open(encoding="utf-8") as f:
    ncbi_records = [
        json.loads(line)
        for line in f
        if line.strip()
    ]

original_by_accession = {
    row["Accession"].strip(): row
    for row in original_rows
}

ncbi_by_accession = {
    record.get("accession", "").strip(): record
    for record in ncbi_records
}

fields = [
    "Accession",
    "Strain_original",
    "BioProject_original",
    "NCBI_study_title",
    "Assembly_level",
    "Assembly_status",
    "Assembly_method",
    "Annotation_pipeline",
    "Annotation_release_date",
    "Protein_coding_genes",
    "Collection_date_original",
    "Collection_date_NCBI",
    "Isolation_source_original",
    "Isolation_source_NCBI",
    "Geographic_location_original",
    "Geographic_location_NCBI",
    "Host_NCBI",
    "Serotype_original",
    "Phenotype_original",
    "NCBI_record_found",
]

rows = []

for accession in sorted(set(original_by_accession) | set(ncbi_by_accession)):
    original = original_by_accession.get(accession, {})
    record = ncbi_by_accession.get(accession)

    result = {field: "" for field in fields}
    result["Accession"] = accession
    result["Strain_original"] = clean(original.get("Strain"))
    result["BioProject_original"] = clean(original.get("BioProject"))
    result["Collection_date_original"] = clean(original.get("Collection_date"))
    result["Isolation_source_original"] = clean(original.get("Isolation_source"))
    result["Geographic_location_original"] = clean(
        original.get("Geographic_location")
    )
    result["Serotype_original"] = clean(original.get("Serotype"))
    result["Phenotype_original"] = clean(original.get("Phenotype"))
    result["NCBI_record_found"] = "yes" if record else "no"

    if record:
        assembly, biosample, attrs = get_attributes(record)
        annotation = record.get("annotation_info", {})
        gene_counts = (
            annotation.get("stats", {})
            .get("gene_counts", {})
        )

        lineage = assembly.get("bioproject_lineage", [])
        titles = []

        for entry in lineage:
            for project in entry.get("bioprojects", []):
                title = clean(project.get("title"))
                if title and title not in titles:
                    titles.append(title)

        result["NCBI_study_title"] = "; ".join(titles)
        result["Assembly_level"] = clean(assembly.get("assembly_level"))
        result["Assembly_status"] = clean(assembly.get("assembly_status"))
        result["Assembly_method"] = clean(assembly.get("assembly_method"))
        result["Annotation_pipeline"] = clean(
            annotation.get("pipeline") or annotation.get("provider")
        )
        result["Annotation_release_date"] = clean(
            annotation.get("release_date")
        )
        result["Protein_coding_genes"] = gene_counts.get(
            "protein_coding", ""
        )

        result["Collection_date_NCBI"] = clean(
            attrs.get("collection_date")
        )
        result["Isolation_source_NCBI"] = clean(
            attrs.get("isolation_source")
        )
        result["Geographic_location_NCBI"] = clean(
            attrs.get("geo_loc_name") or attrs.get("geographic_location")
        )
        result["Host_NCBI"] = clean(attrs.get("host"))

        if not result["Strain_original"]:
            result["Strain_original"] = clean(
                attrs.get("strain") or biosample.get("description", {}).get("organism")
            )

    rows.append(result)

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

with OUTPUT.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows)

print(f"Output: {OUTPUT}")
print(f"Original metadata rows: {len(original_rows)}")
print(f"NCBI records: {len(ncbi_records)}")
print(f"Audit rows written: {len(rows)}")
print(f"NCBI records found: {sum(r['NCBI_record_found'] == 'yes' for r in rows)}")
print("\nFirst five audit rows:")
for row in rows[:5]:
    print(
        row["Accession"],
        "|", row["Strain_original"],
        "|", row["NCBI_study_title"],
        "| protein-coding genes:", row["Protein_coding_genes"]
    )
