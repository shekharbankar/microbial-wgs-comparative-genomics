# Reproducibility Guide

Activate the environment:

    conda activate ngs

Validate candidate variants:

    python scripts/python/validate_stop_gain_variants.py

Map genomic coordinates:

    python scripts/python/map_stop_gain_genomic_coordinates.py

Check required input FASTA files before generating gene alignments.
If an input is missing, identify and run the repository's gene
extraction workflow first.

Example MAFFT command after input verification:

    mafft --auto results/analysis/nfsA_sequences.fasta > results/analysis/alignments/nfsA_aligned.fasta

Repeat for nfsB when its input FASTA exists.

Sequence validation alone does not prove resistance causality.
Verify published phenotype values against the original paper.
