# Microbial Whole-Genome and Comparative Genomics
## Candidate nfsA and nfsB Sequence Variants in Nitrofurantoin-Resistant E. coli Derivatives

### 1. Objective
To compare nfsA and nfsB gene sequences between parental and nitrofurantoin-resistant derivative strains of Escherichia coli and identify candidate nucleotide changes that may affect protein translation.

### 2. Dataset
Six E. coli genome assemblies were analysed from the Xavier et al. (2014) study, available under NCBI BioProject PRJNA238952.

The dataset includes parental ST540 and ST2747 strains and their aerobic and anaerobic resistant derivatives.

### 3. Methods
1. Reviewed assembly metadata and gene annotations.
2. Checked the nucleotide sequences and genome assembly records.
3. Extracted annotated nfsA and nfsB coding sequences.
4. Aligned the sequences using MAFFT.
5. Summarised pairwise nucleotide mismatches and alignment gaps.
6. Examined candidate codon changes using Python and Biopython.
7. Independently translated the reported reference and derivative codons.
8. Compared all 12 extracted gene sequences against their corresponding CDS features in the original GenBank annotations; all 12 matched exactly.
9. Validated the three candidate stop-gain variants against the original parental and derivative GenBank CDS sequences using `scripts/python/validate_stop_gain_variants.py`. All three comparisons had equal CDS lengths and exactly one nucleotide mismatch at the expected CDS position.

### 4. Results

#### 4.1 Candidate stop-gain variants

| Comparison | Gene | CDS position (1-based) | Reference codon | Derivative codon | Predicted effect |
|---|---|---:|---|---|---|
| C1-ST540-P vs ST540an | nfsA | 298 | CAG (Gln, Q) | TAG (Stop) | Stop gained |
| ST2747-Parental vs ST2747a | nfsA | 58 | GAA (Glu, E) | TAA (Stop) | Stop gained |
| ST2747-Parental vs ST2747a | nfsB | 169 | AAA (Lys, K) | TAA (Stop) | Stop gained |

The three candidate variants were checked against the original GenBank CDS sequences. Each parental–derivative pair had equal CDS lengths and exactly one nucleotide mismatch at the expected CDS position. The reference and derivative codons matched the expected sequences, and each derivative codon translated to a stop signal.

The validation script reported PASS for all three candidates. Detailed results are saved in `results/analysis/validated_stop_gain_variants.tsv`.

These are sequence-verified candidate stop-gain variants. Their contribution to resistance has not been established by this computational comparison.

#### 4.2 Other sequence observations
Pairwise comparisons identified nucleotide mismatches in several parental–derivative comparisons. The ST540a nfsA and nfsB annotations are marked as partial at the 3-prime end. Their alignments contain trailing gaps, so amino-acid predictions for these partial coding sequences require additional review.

Some other derivative comparisons showed no nucleotide mismatches in the extracted candidate gene sequence.

### 5. Interpretation
A premature stop codon may truncate a protein and potentially impair its function. Because nfsA and nfsB are associated with nitrofurantoin activation, changes affecting these genes are plausible candidates for further investigation.

However, sequence differences alone cannot demonstrate that a variant causes resistance. Additional validation would be required, including confirmation of genomic coordinates, annotation review, and functional or experimental evidence.

### 6. Limitations
- This is a computational reanalysis of previously published genome assemblies, not a new experimental study.
- NCBI gene annotations and pseudogene labels were used as supporting information; they do not independently establish protein function.
- Partial CDS annotations require caution when interpreting alignment gaps and predicted amino-acid effects.
- The three candidate stop-gain variants were checked against original GenBank CDS sequences, including the expected codon and single-mismatch position. Mapping these CDS positions to explicit genomic variant coordinates and establishing the biological effect still require further review.
- Sequence validation does not establish that a variant causes nitrofurantoin resistance; functional or experimental evidence would be needed.
- The findings are limited to the six assemblies and the candidate genes analysed.

### 7. Conclusion
Comparative sequence analysis identified three candidate stop-gain changes in nfsA or nfsB across the analysed parental–derivative comparisons. These variants provide hypotheses for further study, but their causal contribution to nitrofurantoin resistance remains unconfirmed.

### 8. Reference
Xavier, B. B., et al. (2014). Complete Genome Sequences of Nitrofurantoin-Sensitive and -Resistant Escherichia coli ST540 and ST2747 Strains. Genome Announcements, 2(2), e00239-14. PMID: 24723707. BioProject: PRJNA238952.

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
