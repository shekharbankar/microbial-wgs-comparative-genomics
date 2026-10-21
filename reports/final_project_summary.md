# Microbial Whole-Genome and Comparative Genomics

## Project title

**Comparative analysis of `nfsA` and `nfsB` candidate variants in
nitrofurantoin-resistant *Escherichia coli* derivatives**

## Research question

Which sequence differences occur in the candidate nitrofurantoin-related
genes `nfsA` and `nfsB` when parental *E. coli* strains are compared with
their aerobic or anaerobic derivatives?

## Dataset

- Organism: *Escherichia coli*
- Number of genome assemblies: 6
- NCBI BioProject: PRJNA238952
- Published study context: Xavier et al. (2014)
- Genome accessions and sample labels: see
  `data/metadata/nitrofurantoin_six_genome_manifest.tsv`

## Workflow

1. Reviewed assembly metadata and accession records.
2. Performed basic genome FASTA quality checks.
3. Reviewed the `nfsA` and `nfsB` annotations.
4. Extracted the candidate gene coding sequences.
5. Compared gene sequences using MAFFT alignments.
6. Summarised nucleotide mismatches and alignment gaps.
7. examined candidate codon changes using Python and Biopython.
8. Checked the candidate codons against the original GenBank CDS records.
9. Mapped candidate variants to genomic coordinates.
10. Compared the candidate variants with reported phenotype evidence.
11. Documented technical and biological limitations.

## Genome quality checks

The project's recorded QC table contains six assemblies. Each has one
chromosome record, zero ambiguous `N` bases, zero other non-ACGTN bases,
and a sequence-integrity status of PASS.

See `results/qc/six_genome_qc.tsv`.

## Main sequence findings

Three candidate stop-gain variants were sequence-validated:

| Comparison | Gene | CDS position (1-based) | Reference codon | Derivative codon | Predicted protein change |
|---|---|---:|---|---|---|
| C1-ST540-P vs ST540an | nfsA | 298 | CAG | TAG | Q100* |
| ST2747-Parental vs ST2747a | nfsA | 58 | GAA | TAA | E20* |
| ST2747-Parental vs ST2747a | nfsB | 169 | AAA | TAA | K57* |

The existing validation results report equal CDS lengths and one nucleotide
mismatch at the expected CDS position for each of these three comparisons.
The candidate codons match the reported reference and derivative sequences.

See:
- `results/analysis/validated_stop_gain_variants.tsv`
- `results/analysis/final_variant_summary.tsv`
- `results/analysis/variant_biological_interpretation.tsv`

## Phenotype context

The project records published MIC values for the relevant derivatives in
`results/analysis/phenotype_variant_evidence.tsv`. These values are
literature-derived and were not experimentally measured by this project.

The ST2747-a comparison contains candidate stop-gain changes in both `nfsA`
and `nfsB`. This comparison alone cannot isolate the independent contribution
of either variant.

## Biological interpretation

A premature stop codon can potentially shorten a protein and affect its
function. Because `nfsA` and `nfsB` are involved in nitrofurantoin activation,
these changes are plausible candidates for further study.

**Important:** this is a computational comparative-genomics analysis.
Sequence validation does not prove loss of enzyme activity or establish that
a candidate variant caused antibiotic resistance. Functional experiments
and appropriately designed phenotype analyses would be needed to establish
causality.

## Important limitation

The `nfsA` and `nfsB` annotations for the ST540a derivative are recorded as
partial at the 3-prime end. Their alignments contain gaps. Those comparisons
require special caution, and the partial gene sequences should not be
treated as straightforward full-length coding sequences.

## Reproducibility files

- Environment specification: `environment.yml`
- Python analysis scripts: `scripts/python/`
- Shell scripts: `scripts/bash/`
- Genome QC table: `results/qc/six_genome_qc.tsv`
- Variant validation table: `results/analysis/validated_stop_gain_variants.tsv`
- Analysis outputs: `results/analysis/`
- Main project guide: `README.md`

## Conclusion

This project demonstrates a reproducible computational workflow for
microbial comparative genomics, combining genome QC, annotation review,
sequence extraction, alignment, codon-level comparison, coordinate mapping,
and evidence-aware biological interpretation.

The results support three sequence-validated candidate stop-gain variants.
They should be reported as candidates associated with the studied derivatives,
not as experimentally proven causes of resistance.
