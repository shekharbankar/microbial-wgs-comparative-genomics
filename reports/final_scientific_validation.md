# Final Scientific Validation Report

## Project
Comparative whole-genome analysis of six selected Escherichia coli
genomes, focusing on candidate nfsA and nfsB variants associated
with nitrofurantoin susceptibility.

## Candidate variants

| Gene | CDS position | Reference codon | Derivative codon | Predicted change |
|---|---:|---|---|---|
| nfsA | 298 | CAG | TAG | Q100* |
| nfsA | 58 | GAA | TAA | E20* |
| nfsB | 169 | AAA | TAA | K57* |

These findings are reported as candidate sequence variants.
Their biological effects and contributions to resistance have
not been experimentally established by this project.

## Technical validation

Previous recorded terminal output reported successful independent
CDS checks for three candidate variants and successful mapping
of their genomic coordinates.

The latest execution status must be checked using the project
validation scripts and generated result tables.

## Phenotype evidence

MIC values recorded in the project are attributed to a published
study. They were not measured experimentally by this project.
The original publication and its supplementary data must be checked
before these values are used in a submitted report.

A variant-phenotype association does not establish causation.

## Limitations

- No new antimicrobial susceptibility experiments were performed.
- Enzyme activity was not measured.
- Complementation and allele-replacement experiments were not performed.
- Other mutations and genetic background may affect the phenotype.
- Full reproducibility requires regeneration and review of the
  extraction, alignment and analysis outputs.

## Principal outputs

- results/qc/six_genome_qc.tsv
- results/analysis/validated_stop_gain_variants.tsv
- results/analysis/stop_gain_genomic_coordinates.tsv
- results/analysis/variant_biological_interpretation.tsv
- results/analysis/phenotype_variant_evidence.tsv
- results/analysis/final_variant_summary.tsv
- docs/reproducibility.md
- environment.yml

## Conclusion

This project provides a computational comparative-genomics
workflow for investigating candidate nfsA and nfsB variants.
Sequence-level validation supports the reported sequence changes,
but does not establish that these variants independently cause
nitrofurantoin resistance.
