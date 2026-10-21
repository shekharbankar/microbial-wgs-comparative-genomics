# Microbial WGS Comparative Genomics — Completion Status

## Project scope
Comparative genomic analysis of selected Escherichia coli isolates,
focusing on candidate nfsA and nfsB variants.

## Candidate sequence changes

| Gene | CDS position | Codon change | Predicted protein change |
|---|---:|---|---|
| nfsA | 298 | CAG -> TAG | Q100* |
| nfsA | 58 | GAA -> TAA | E20* |
| nfsB | 169 | AAA -> TAA | K57* |

## Principal outputs
- results/qc/six_genome_qc.tsv
- results/analysis/validated_stop_gain_variants.tsv
- results/analysis/stop_gain_genomic_coordinates.tsv
- results/analysis/variant_biological_interpretation.tsv
- results/analysis/phenotype_variant_evidence.tsv
- results/analysis/final_variant_summary.tsv
- docs/reproducibility.md
- environment.yml

## Recorded technical checks
Previous terminal logs recorded successful Python syntax checks,
TSV structure checks, and sequence-level checks for three candidate
stop-gain variants. Genomic coordinate mapping was also reported
as successful.

## Scientific limitations
- Sequence changes alone do not prove resistance causality.
- No new antimicrobial susceptibility experiments were performed.
- Enzyme activity and genetic complementation were not tested.
- Published MIC values require checking against the primary paper.
- Complete independent reproducibility requires regeneration and
  review of the full extraction, alignment, and analysis workflow.

## Completion statement
This file records the project's current documentation status.
It does not certify experimental validation or complete independent
reproducibility. The presence and correctness of principal outputs
must be checked against the actual repository files.
