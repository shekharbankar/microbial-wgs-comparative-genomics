# Reproducibility Guide

## 1. Environment

    conda activate ngs
    python --version
    python -c "import Bio; print(Bio.__version__)"
    mafft --version
    seqkit version

## 2. Candidate variant validation

    python scripts/python/validate_stop_gain_variants.py

Output:
results/analysis/validated_stop_gain_variants.tsv

## 3. Genomic coordinate mapping

    python scripts/python/map_stop_gain_genomic_coordinates.py

Output:
results/analysis/stop_gain_genomic_coordinates.tsv

## 4. Gene extraction and alignment

Check the repository's extraction scripts and annotations before
regenerating missing gene FASTA files.

If the required gene FASTA files exist:

    mkdir -p results/analysis/alignments
    mafft --auto results/analysis/nfsA_sequences.fasta > results/analysis/alignments/nfsA_aligned.fasta
    mafft --auto results/analysis/nfsB_sequences.fasta > results/analysis/alignments/nfsB_aligned.fasta

Check the output files and alignment lengths before claiming success.

## 5. Validation

Review the verification logs, output table headers, record counts,
and regenerated results.

## 6. Scientific limitations

Sequence validation does not establish biological causality.
Published phenotype values must be checked against the original paper.
