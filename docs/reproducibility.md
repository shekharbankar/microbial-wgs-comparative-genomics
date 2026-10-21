# Reproducibility Guide

## Project Overview

This project investigates selected Escherichia coli genomes using
comparative microbial genomics, with particular attention to the
nitrofurantoin-associated genes nfsA and nfsB.

## Software Environment

The project environment is specified in environment.yml.

Activate the existing environment:

    conda activate ngs

Check software versions:

    python --version
    python -c "import Bio; print(Bio.__version__)"
    mafft --version
    seqkit version

## Project Structure

- data/raw/: original input data
- data/processed/: processed sequences and annotations
- scripts/python/: Python analysis scripts
- scripts/bash/: shell scripts
- results/qc/: genome quality-control outputs
- results/analysis/: analysis tables and alignments
- reports/: final project reports
- docs/: documentation

## Main Analysis Outputs

- results/qc/six_genome_qc.tsv
- results/analysis/validated_stop_gain_variants.tsv
- results/analysis/variant_biological_interpretation.tsv
- results/analysis/phenotype_variant_evidence.tsv
- results/analysis/final_variant_summary.tsv

## Reproducibility Procedure

1. Review the README.md and environment.yml files.
2. Confirm that the required genome and annotation inputs exist.
3. Review the scripts in scripts/python/ and scripts/bash/.
4. Run the analysis scripts in their documented order.
5. Verify that expected output files are regenerated.
6. Compare regenerated results with the recorded validation tables.
7. Investigate any differences before reporting conclusions.

Existing output files alone do not prove that the complete workflow
has been reproduced successfully.

## Scientific Limitations

The candidate stop-gain variants are sequence-based findings.
Their presence does not independently establish that they cause
nitrofurantoin resistance.

Phenotype values obtained from published studies must be identified
as literature-derived, not as measurements performed in this project.

Functional experiments and suitable phenotype analyses are required
to establish causal relationships.

## Final Verification

Check the current environment, output files and Git status before
publishing the repository.

Use git diff --check to detect whitespace errors.
