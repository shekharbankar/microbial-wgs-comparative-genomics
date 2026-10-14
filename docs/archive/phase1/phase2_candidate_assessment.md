# Phase 2: Candidate Genome Assessment

## Dataset
20 unique Escherichia coli candidate assemblies were compiled in:
data/metadata/ecoli_all_candidates_review.csv

## Assembly Information
All 20 candidates are labelled Complete Genome in the current review table.
Completeness and contamination metrics are available for 19 of 20 candidates.

Reported completeness:
- Minimum: 95.98%
- Median: 99.03%
- Maximum: 99.55%

Reported contamination:
- Minimum: 0.15%
- Median: 0.42%
- Maximum: 1.71%

These are metadata-reported values and have not yet been independently validated.

## Metadata Availability
- Isolation source: 8 populated records, 12 missing
- Collection date: 16 populated records, 4 missing
- Geographic location: 10 populated records, 10 missing
- Serotype: 2 populated records, 18 missing
- Phenotype: 1 populated record, 19 missing

The counts above treat blank CSV cells as missing. Text values such as "missing" or "not applicable" require separate normalization where relevant.

## Dataset Diversity
Six candidates belong to BioProject PRJNA238952.
The final selection should avoid excessive representation of a single study where possible.

The candidate set includes laboratory strains and natural or clinical/environmental isolates. Their intended roles must be considered before selection.

## AMR Interpretation
One candidate, GCF_000814145.2 (strain 6409), has the phenotype field recorded as carbapenem resistant in the current metadata table.

For all other candidates, missing phenotype data must be treated as unknown.
AMR gene detection results will be reported separately from phenotype evidence.

## Current Decision
The final set of approximately 10 genomes has not yet been selected.
Selection will consider assembly quality, study diversity, strain type, metadata, and the planned AMR comparison.

## Next Steps
1. Normalize and review missing metadata.
2. Decide whether the main analysis will focus on natural/clinical isolates or include laboratory reference strains.
3. Apply consistent selection criteria.
4. Record the rationale for every selected assembly.
5. Download selected genomes only after the selection is reviewed.
