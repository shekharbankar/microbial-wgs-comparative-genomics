# Microbial WGS Comparative Genomics

## Candidate variants
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

## Limitations
The candidate variants have passed the recorded sequence-level checks.
This does not prove that they cause nitrofurantoin resistance.
No new susceptibility experiments, enzyme activity measurements,
or genetic complementation experiments were performed.
Published MIC values require primary-source verification.
Full independent reproducibility requires regeneration and review
of the complete extraction, alignment, and analysis workflow.

## Completion status
Project documentation and recorded computational findings are
preserved in the repository. Full independent scientific
reproducibility and biological causality remain unconfirmed.
