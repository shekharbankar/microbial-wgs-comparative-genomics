# Microbial WGS and Comparative Genomics

## Project Overview
A reproducible comparative-genomics reanalysis of six publicly available
Escherichia coli genome assemblies associated with a published study of
nitrofurantoin-sensitive and nitrofurantoin-resistant strains.

The project focuses on genome metadata and sequence quality checks,
annotation review, extraction of candidate genes (nfsA and nfsB),
multiple-sequence alignment, pairwise nucleotide comparisons, and
candidate codon-effect analysis.

## Research Question
What sequence differences are observed in nfsA and nfsB between the
parental E. coli strains and their aerobic or anaerobic resistant
derivatives?

## Dataset
- Organism: Escherichia coli
- NCBI BioProject: PRJNA238952
- Study: Xavier et al. (2014)
- Number of assemblies: 6

The assembly accessions, strain labels, and phenotype metadata are recorded
in `data/metadata/nitrofurantoin_six_genome_manifest.tsv`.

## Workflow Completed
1. Reviewed assembly accessions and metadata.
2. Checked the six assemblies and recorded sequence QC results.
3. Reviewed NCBI annotations for nfsA and nfsB.
4. Extracted the annotated candidate gene sequences.
5. Aligned the sequences using MAFFT.
6. Summarised pairwise nucleotide mismatches and alignment gaps.
7. Examined candidate codon effects using Python and Biopython.
8. Independently translated three reported stop-gain codon changes.
9. Cross-checked all 12 extracted gene sequences against their original GenBank CDS features.
10. Validated three candidate stop-gain variants against the original parental and derivative GenBank CDS sequences using `scripts/python/validate_stop_gain_variants.py`.
11. Mapped the three candidate stop-gain variants to genomic coordinates
    and validated the reference and derivative bases, codons, and strands.
12. Prepared a biological interpretation table and cross-referenced the
    candidate variants with published nitrofurantoin MIC data.
13. Documented the results, evidence limitations, and reproducibility files.

## Key Results
Three candidate stop-gain changes were identified and checked against the original GenBank CDS sequences. All 12 extracted gene sequences matched their corresponding annotated CDS features exactly. Each candidate parental–derivative pair had equal CDS lengths and exactly one nucleotide mismatch at the expected CDS position. The validation script reported PASS for all three candidates:

| Comparison | Gene | CDS position (1-based) | Codon change |
|---|---|---:|---|
| C1-ST540-P vs ST540an | nfsA | 298 | CAG -> TAG |
| ST2747-Parental vs ST2747a | nfsA | 58 | GAA -> TAA |
| ST2747-Parental vs ST2747a | nfsB | 169 | AAA -> TAA |

These are sequence-verified candidate stop-gain variants. The analysis does not establish that they caused nitrofurantoin resistance. Functional or experimental evidence would be needed to establish causation.

The ST540a nfsA and nfsB annotations are partial at the 3-prime end.
Their alignment gaps and predicted amino-acid effects require caution.

## Main Outputs
- `results/qc/six_genome_qc.tsv`
- `results/analysis/nitrofurantoin_gene_annotation_status.tsv`
- `results/analysis/nitrofurantoin_nfsA_nfsB_sequences.fasta`
- `results/analysis/pairwise_alignment_summary.tsv`
- `results/analysis/pairwise_mismatch_details.tsv`
- `results/analysis/aligned_codon_variant_details.tsv`
- `results/analysis/aligned_codon_comparison_summary.tsv`
- `results/analysis/comparative_genomics_report.md`
- `results/analysis/validated_stop_gain_variants.tsv`
- `results/analysis/stop_gain_genomic_coordinates.tsv`
- `results/analysis/variant_biological_interpretation.tsv`
- `results/analysis/phenotype_variant_evidence.tsv`
- `scripts/python/validate_stop_gain_variants.py`
- `scripts/python/map_stop_gain_genomic_coordinates.py`

## Tools
- Python
- Biopython
- MAFFT
- SeqKit
- NCBI assembly and annotation data

## Limitations
This is a computational reanalysis of previously published assemblies.
The three candidate stop-gain variants were validated against the original parental and derivative GenBank CDS features and mapped to genomic coordinates. Their biological interpretation and association with published nitrofurantoin MIC values are documented in the analysis tables. These are computational findings based on genome sequences and published phenotype data, not experiments performed by this project. The associations do not establish that any individual variant caused resistance. Functional experiments would be needed to establish causation.

## Reference
Xavier, B. B., et al. (2014). Complete Genome Sequences of
Nitrofurantoin-Sensitive and -Resistant Escherichia coli ST540 and ST2747
Strains. Genome Announcements, 2(2), e00239-14.
PMID: 24723707. BioProject: PRJNA238952.

## Verified genomic coordinates of candidate stop-gain variants

The three candidate stop-gain variants were mapped independently in the
reference and derivative GenBank CDS features. The mapping script verified
the CDS nucleotide, genomic forward-strand nucleotide, codon, strand,
and CDS length. Coordinates below are 1-based genomic coordinates.

| Gene | CDS position | Reference assembly | Reference record | Reference coordinate | Strand | Derivative assembly | Derivative record | Derivative coordinate | Codon change |
|---|---:|---|---|---:|:---:|---|---|---:|---|
| nfsA | 298 | GCF_000597845.1 | NZ_CP007265.1 | 386979 | - | GCF_000599645.1 | NZ_CP007391.1 | 3059910 | CAG -> TAG |
| nfsA | 58 | GCF_000599665.1 | NZ_CP007392.1 | 1595566 | + | GCF_000599685.1 | NZ_CP007393.1 | 1604255 | GAA -> TAA |
| nfsB | 169 | GCF_000599665.1 | NZ_CP007392.1 | 1318382 | - | GCF_000599685.1 | NZ_CP007393.1 | 1328785 | AAA -> TAA |

Reproducibility:
- Mapping script: `scripts/python/map_stop_gain_genomic_coordinates.py`
- Detailed output: `results/analysis/stop_gain_genomic_coordinates.tsv`
- Sequence validation output: `results/analysis/validated_stop_gain_variants.tsv`

These are sequence-validated candidate stop-gain variants, not proof of
causation. The observed variants are consistent with premature stop codons
in the annotated CDS sequences, but their contribution to nitrofurantoin
resistance requires further evidence and, ideally, functional validation.

## Biological interpretation and evidence grading

The three sequence-validated candidate variants introduce premature stop
codons in the annotated coding sequences:

| Gene | CDS position | Predicted protein consequence | Codon change | Interpretation |
|---|---:|---|---|---|
| nfsA | 298 | Q100* | CAG -> TAG | Candidate NfsA loss-of-function |
| nfsA | 58 | E20* | GAA -> TAA | Candidate NfsA loss-of-function |
| nfsB | 169 | K57* | AAA -> TAA | Candidate NfsB loss-of-function |

NfsA and NfsB are oxygen-insensitive nitroreductases involved in nitrofurantoin
activation. Published work supports loss of function in these pathways as an
important resistance mechanism. However, sequence-based predictions have
limitations: some susceptible isolates carry loss-of-function changes in one
of these genes, and resistance can also involve gene expression and other
genetic mechanisms.

The variants reported here are therefore classified as sequence-validated
candidate loss-of-function changes, not experimentally proven causes of
resistance. No enzyme activity or complementation assay was performed in
this project. Predicted protein consequences should be interpreted in the
context of the strain's complete genotype and the phenotype reported in the
original study.

Evidence references:
1. Vervoort et al. (2014). An In Vitro Deletion in ribE Encoding Lumazine
   Synthase Contributes to Nitrofurantoin Resistance in Escherichia coli.
   Antimicrobial Agents and Chemotherapy. DOI: 10.1128/AAC.03952-14.
2. Improving nitrofurantoin resistance prediction in Escherichia coli from
   whole-genome sequence by integrating NfsA/B enzyme assays (2024).
   Antimicrobial Agents and Chemotherapy. DOI: 10.1128/aac.00242-24.

Reproducible interpretation table:
`results/analysis/variant_biological_interpretation.tsv`

## Published phenotype cross-check

Published nitrofurantoin MIC values were cross-referenced with the
sequence-validated candidate stop-gain variants. These MIC values are
transcribed from the published study; they were not measured by this project.

| Strain | Candidate variant | Reported aerobic MIC (µg/mL) | Reported anaerobic MIC (µg/mL) |
|---|---|---:|---:|
| ST540-an | nfsA Q100* | 64 | 16 |
| ST2747-a | nfsA E20* | 128 | 32 |
| ST2747-a | nfsB K57* | 128 | 32 |

Source: Vervoort et al. (2014), *An In Vitro Deletion in ribE Encoding
Lumazine Synthase Contributes to Nitrofurantoin Resistance in Escherichia
coli*. Antimicrobial Agents and Chemotherapy.
DOI: 10.1128/aac.03952-14.

Interpretation: the candidate stop-gain variants occur in resistant
derivatives, supporting a genotype-phenotype association. Because ST2747-a
contains candidate stop-gains in both nfsA and nfsB, these observations
cannot independently determine the contribution of each variant. This
cross-check is not an experimental validation of causality.

Detailed table: `results/analysis/phenotype_variant_evidence.tsv`

## Reproducible environment

The core analysis environment is specified in `environment.yml`.

Create and activate it using:

    conda env create -f environment.yml
    conda activate microbial-wgs-comparative-genomics

The environment specification includes Python, Biopython, MAFFT, and SeqKit. Individual scripts may require additional inputs or tools; consult the script documentation before running them.

Genome assemblies and annotations were downloaded from NCBI. Refer to the data documentation and cited records for dataset provenance.
