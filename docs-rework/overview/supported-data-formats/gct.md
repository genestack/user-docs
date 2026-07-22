---
diataxis: reference
tab: overview
---

# GCT (Gene Expression)

GCT (Gene Cluster Text) files store gene expression datasets: microarray and RNA-seq data. They provide a structured, tab-delimited format for organising expression values across samples. ODM automatically recognises GCT files as Expression files.

## Supported variants

- `.gct`: standard GCT file
- `.gct.gz`, `.gct.zip`: compressed versions (available via API)
- `.gct.tsv`, `.gct.tsv.gz`, `.gct.tsv.zip`: GCT files with additional expression metadata (available via API)

Example files:

- [Test_1000g.gct](https://s3.amazonaws.com/bio-test-data/odm/Test_1000g/Test_1000g.gct)
- [Test_1000g.gct.tsv](https://s3.amazonaws.com/bio-test-data/odm/Test_1000g/Test_1000g.gct.tsv)

## File structure

![GCT file structure](../../assets/user-guide/doc-odm-user-guide/doc-odm-user-guide/images/gct-file.png)

A GCT file has the following structure:

**Line 1 (file version)**: always `#1.2`.

**Line 2 (matrix dimensions)**: the number of features (rows) and samples (columns) in the expression matrix, excluding the identifier and description columns. Example: `2  4` means 2 features and 4 samples.

**Line 3 (header row)**: the first column must be labelled `Name` (case-insensitive), the second column must be `Description` (case-insensitive), followed by sample identifiers. Sample identifiers must be unique, single-word, and contain no whitespace.

**Data matrix**: each row corresponds to one feature (for example, a gene). The first column contains the unique identifier (for example, an Ensembl gene ID), the second column contains a text description, and the remaining columns contain expression values for each sample. The number of rows and columns must match the dimensions declared on line 2.

Names and descriptions may contain spaces. Missing intensity values may be left empty; NA or NULL text strings should be used if the field must not be blank.

## Expression metadata file (.gct.tsv)

`.gct.tsv`, `.gct.tsv.gz`, and `.gct.tsv.zip` files are tab-delimited files describing the expression data (for example, normalisation method and genome version). The first row contains key names; the second row contains the corresponding values.

| Expression Source | Normalization Method | Genome Version |
|---|---|---|
| 1000 Genomes Project | RPKM | GRCh38.91 |

## External reference

For the full GCT format specification, see the [GCT format, Connectopedia](https://clue.io/connectopedia/gct_format).
