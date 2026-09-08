---
diataxis: reference
tab: overview
---

# TSV (Tabular data)

ODM accepts any tabular data formatted as TSV (tab-separated values). As long as your file represents a data frame, ODM can import and index it. A data frame organises data into a two-dimensional table of rows and columns.

A data frame contains two main elements:

- **Features**, the entities measured in an experiment (genes, proteins, metabolites, pathways, etc.).
- **Measurements (or values)**, the actual values recorded for each feature under different conditions (gene expression values, protein abundance, pathway activity, etc.).

## Per-entity TSV formats

### Study metadata file

Study metadata is supplied as a tab-delimited TSV file. There is a limit of 255 characters for attribute names.

Example file: [Test_1000g.study.tsv](https://s3.amazonaws.com/bio-test-data/odm/Test_1000g/Test_1000g.study.tsv)

### Samples metadata file

Samples metadata is supplied as a TSV file. Required columns:

- **Sample Source**: must be present with values filled in.
- **Sample Source ID**: values must match the column headers for samples in the GCT/VCF/other data files.

The remaining columns are metadata attributes. Attribute names cannot be duplicated. There is a limit of 255 characters for attribute names.

Example file: [Test_1000g.samples.tsv](https://s3.amazonaws.com/bio-test-data/odm/Test_1000g/Test_1000g.samples.tsv)

| Sample Source | Sample Source ID | Species | Sex | Population |
|---|---|---|---|---|
| 1000 Genomes Project | HG00119 | Homo sapiens | M | British |
| 1001 Genomes Project | HG00121 | Homo sapiens | F | British |

### Libraries file

Libraries metadata is a TSV file with information about how samples were prepared: quality, barcodes, and library properties (single-end vs paired-end). Each sample can have more than one corresponding library. Multiple samples can be pooled into the same library.

Required headings: **Sample Source ID**, **Library ID**.

Example file: [Test_RM.libraries.tsv](https://bio-test-data.s3.amazonaws.com/Research_Model_BR-205/Test_RM.libraries.tsv)

| Sample Source ID | Library ID | Library barcode | Library pool |
|---|---|---|---|
| SRR6441195 | LIB1 | A | |
| SRR6441196 | LIB2 | B | |
| SRR6441197 | LIB3 | A + B | 1\|2 |

### Preparations file

Preparations metadata follows the same format as libraries but contains proteomics-specific metadata.

Required headings: **Sample Source ID**, **Preparation ID**.

Example file: [Test_RM.preparations.tsv](https://bio-test-data.s3.amazonaws.com/Research_Model_BR-205/Test_RM.preparations.tsv)

## Generic tabular data (data frames)

### Structure

![Simple data frame](../../assets/user-guide/doc-odm-user-guide/doc-odm-user-guide/images/data-frame1.png)

The simplest data frame has features in the first column and measurements for each sample in the remaining columns.

![Complex data frame](../../assets/user-guide/doc-odm-user-guide/doc-odm-user-guide/images/data-frame2.png)

A complex data frame has multiple feature columns (gene name, protein name, peptide sequence, PTM site, etc.) and more than one measurement type per sample (intensity, quality flag, fold change, p-value, etc.).

### Requirements

- All columns must have names.
- All feature columns must be consecutive on the left side of the file. Specify the number of feature columns at upload time.
- Missing values must be coded as one of: ` ` (space), empty, `NaN`, `null`, `N/A`, `NA`, `filtered`, `Inf`, `-Inf`.
- A column is identified as string or numeric automatically. If a column that should be numeric contains any non-numeric character (other than the accepted missing value codes), it is treated as a string column, which disables ranged search.
- Measurement columns must contain only numeric values or missing values.

!!! note
    To enable faster search, put the most important feature identifier (gene name, protein name, etc.) as the first column.

### Multiple measurements per sample

If your file contains more than one measurement type per sample (for example, Fold Change and P-value), the system recognises them by the following rules:

- **Separator in column name**: the column name must contain a special symbol (or combination of symbols) as a separator between the sample name and the measurement type. Example: `Sample1.p-value` uses `.` as separator. If multiple separators exist in the name, only the first one is used for parsing.
- **Separator specification**: specify the separator explicitly at upload time (API or UI).
- **Consistency**: all columns in the file must include the separator.
- **Uniform measurement types**: every sample must include the same set of measurement types.

| Sample1.Intensity | Sample1.QualityPass | Sample2.Intensity | Sample2.QualityPass |
|---|---|---|---|
| 5.4 | Pass | 7.8 | Pass |
| 4.9 | Fail | 8.1 | Pass |

## Cross-reference mapping file

A cross-reference mapping file is a TSV file with two columns. The first row must contain the headers `TXNAME` and `GENEID`. The first column must be transcript IDs (must be unique). The file must be hosted at an HTTPS location accessible to ODM.
