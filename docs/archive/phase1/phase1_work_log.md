# Phase 1 Work Log

## Project
Comparative Genomics and Antimicrobial Resistance Gene Profiling of Escherichia coli

## Phase 1 Scope
Project setup, reference genome acquisition, nucleotide composition analysis, and candidate genome metadata collection.

## Completed Work

### 1. Project Setup
- Created the project directory and its working structure.
- Organized folders for scripts, raw data, processed data, results, reports, figures, and documentation.

### 2. Reference Genome
- Organism: Escherichia coli
- Reference strain: K-12 MG1655
- Assembly accession: GCF_000005845.2
- Sequence accession: NC_000913.3
- Downloaded the reference genome in FASTA format using NCBI Datasets.

### 3. Base Composition Analysis
- Script: scripts/python/base_composition.py
- Output: results/base_composition.csv
- Genome length: 4,641,652 bp
- GC percentage: 50.79%
- Verified that A, T, G, and C counts sum to the reported genome length.

### 4. Candidate Genome Metadata
- Retrieved metadata for candidate E. coli assemblies.
- Generated candidate summary and review CSV files.
- Reviewed available strain, assembly, sequencing, and sample metadata.
- The working candidate collection contains 20 unique candidates.

## Pending Work
- Verify and archive the Phase 1 files.
- Finalize the selection criteria for approximately 10 genomes.
- Select a diverse and suitable genome dataset.
- Download the selected genomes.
- Perform genome size and GC percentage comparisons.
- Perform genome similarity and phylogenetic analysis.
- Install and use a suitable AMR gene detection tool.
- Document results, limitations, and software versions.

## Scientific Cautions
- Missing AMR phenotype information does not mean an isolate is susceptible.
- Detection of an AMR gene does not by itself prove clinical resistance.
- Candidate genomes have not yet been finalized.
- Comparative genomics and AMR profiling are not yet complete.

## Phase Boundary
Phase 1 covers the work performed so far.
Phase 2 will begin with final dataset selection and subsequent comparative analysis.

## Documentation Note
This log summarizes the currently documented project work. It is not a complete record of every terminal command or session.
