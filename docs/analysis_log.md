# Genome Base Composition Analysis Log

> **Historical preliminary analysis:** This log documents an earlier single-genome base-composition exercise using E. coli K-12 MG1655. It is separate from the six-genome nitrofurantoin comparative-genomics study described in the main README.

## Dataset
- Organism: Escherichia coli K-12 MG1655
- Assembly accession: GCF_000005845.2
- Sequence accession: NC_000913.3
- File format: FASTA

## Analysis Results
- Genome length: 4,641,652 bp
- Adenine (A): 1,142,742
- Thymine (T): 1,141,382
- Guanine (G): 1,177,437
- Cytosine (C): 1,180,091
- GC content: 50.79%

## Validation
- Python base counts sum matches genome length: PASS
- SeqKit genome length matches Python: PASS
- Unexpected DNA characters detected: None

## Tools
- Python: Base composition calculation and validation
- SeqKit: FASTA sequence statistics

## Limitation
This is a preliminary analysis of one reference genome.
It is not yet a comparative genomics analysis.
