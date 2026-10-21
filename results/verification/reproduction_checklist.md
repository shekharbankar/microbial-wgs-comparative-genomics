# Scientific Reproduction Checklist

## Repository checks
- [x] Git repository exists.
- [x] Python syntax has previously been checked.
- [x] Environment versions have previously been recorded.
- [x] TSV structure has previously been checked.

## Scientific reproduction still to be demonstrated
- [ ] Confirm every assembly accession against the original source.
- [ ] Confirm the six input assemblies are present and unmodified.
- [ ] Identify the exact command and input files for every analysis script.
- [ ] Re-run genome QC from the original FASTA files.
- [ ] Re-run gene extraction from the original annotations.
- [ ] Re-run MAFFT alignments from the extracted sequences.
- [ ] Re-run codon-level variant analysis.
- [ ] Independently validate genomic coordinates.
- [ ] Cross-check MIC values against the primary publication.
- [ ] Compare regenerated results against the committed tables.

## Interpretation
Passing syntax and table checks does not establish scientific correctness.
A sequence variant associated with a resistant derivative is not necessarily
the cause of resistance. Published phenotype measurements must be identified
as literature-derived rather than measurements performed in this project.
