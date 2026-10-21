# Final Scientific Validation Report

## Project overview

This project examines selected Escherichia coli genome assemblies
using comparative microbial genomics, with a focus on nfsA and nfsB
candidate variants associated with nitrofurantoin susceptibility.

The workflow includes genome sequence quality checks, annotation
review, coding-sequence comparisons, sequence alignment, codon-level
interpretation, genomic coordinate mapping, and evidence review.

## Sequence-validated candidate variants

| Gene | CDS position (1-based) | Reference codon | Derivative codon | Predicted protein change |
|---|---:|---|---|---|
| nfsA | 298 | CAG | TAG | Q100* |
| nfsA | 58 | GAA | TAA | E20* |
| nfsB | 169 | AAA | TAA | K57* |

The repository's validation script compares the annotated coding
sequences and checks the expected nucleotide difference and codon
change. The regenerated output tables must be reviewed alongside
this report.

## Biological interpretation

Each listed substitution is predicted to introduce a premature
termination codon in the corresponding coding sequence.

These are sequence-based candidate effects. This computational
project does not establish enzyme activity, demonstrate the
independent contribution of each variant, or experimentally prove
that any individual substitution causes nitrofurantoin resistance.

Where multiple candidate variants occur in the same derivative,
their separate effects cannot be determined from sequence comparison
alone.

## Phenotype evidence

The phenotype evidence table records antimicrobial susceptibility
values attributed to a published study. These values were not
measured experimentally by this project.

The recorded values and their correspondence to the relevant strains
must be checked against the original publication before being used
in a final dissertation, report, or presentation.

## Reproducibility

The repository includes Python analysis scripts, an environment
specification, input genome assemblies, annotated coding sequences,
and tabular results.

This finalization run checks software availability, Python syntax,
required TSV structure, candidate variant validation, genomic
coordinate mapping, and available alignment files.

These checks do not independently establish that every earlier
analysis can be reproduced from scratch. A full reproducibility
claim requires rerunning the original workflow from documented inputs
and comparing all regenerated outputs with the saved results.

## Key outputs

- 
