# TSV (Tabular Data)

TSV (tab-separated values) is the primary format for uploading tabular metadata and omics data frames into ODM. Any two-dimensional table where columns have names and rows represent observations or features can be imported and indexed.

ODM uses TSV for several distinct object types — study metadata, sample metadata, libraries, preparations, and generic tabular (data frame) files — each with its own required columns.

---

## Study metadata file

Study metadata is supplied as a TSV file of study-level attributes. Attribute names are limited to 255 characters.

**Example file:** [Test_1000g.study.tsv](https://s3.amazonaws.com/bio-test-data/odm/Test_1000g/Test_1000g.study.tsv)

---

## Samples metadata file

Samples metadata is a TSV file where each row describes one sample.

**Example file:** [Test_1000g.samples.tsv](https://s3.amazonaws.com/bio-test-data/odm/Test_1000g/Test_1000g.samples.tsv)

### Required columns

| Column | Description |
|---|---|
| `Sample Source` | Must be present and populated for every row. |
| `Sample Source ID` | Values must match the column headers in linked GCT, VCF, or other data files. |

All remaining columns are metadata attributes. Attribute names must be unique and are limited to 255 characters.

### Example

| Sample Source        | Sample Source ID | Species      | Sex | Population |
|----------------------|------------------|--------------|-----|------------|
| 1000 Genomes Project | HG00119          | Homo sapiens | M   | British    |
| 1001 Genomes Project | HG00121          | Homo sapiens | F   | British    |
| 1002 Genomes Project | HG00183          | Homo sapiens | M   | Finnish    |
| 1003 Genomes Project | HG00176          | Homo sapiens | F   | Finnish    |

---

## Libraries file

Libraries metadata describes how samples were prepared: barcodes, library properties (single-end vs. paired-end), and pooling. Each sample can have more than one corresponding library. Multiple samples can be pooled into the same library.

**Example file:** [Test_RM.libraries.tsv](https://bio-test-data.s3.amazonaws.com/Research_Model_BR-205/Test_RM.libraries.tsv)

### Required columns

| Column | Description |
|---|---|
| `Sample Source ID` | Links the library to a sample. |
| `Library ID` | Unique identifier for the library. |

### Example

| Sample Source ID | Library ID | Library barcode | Library pool |
|-----------------|------------|-----------------|--------------|
| SRR6441195      | LIB1       | A               |              |
| SRR6441196      | LIB2       | B               |              |
| SRR6441197      | LIB3       | A + B           | 1\|2         |

---

## Preparations file

Preparations metadata follows the same structure as the Libraries file but contains proteomics-specific metadata.

**Example file:** [Test_RM.preparations.tsv](https://bio-test-data.s3.amazonaws.com/Research_Model_BR-205/Test_RM.preparations.tsv)

### Required columns

| Column | Description |
|---|---|
| `Sample Source ID` | Links the preparation to a sample. |
| `Preparation ID` | Unique identifier for the preparation. |

---

## Tabular data (data frames)

Any TSV file that represents a data frame can be uploaded and indexed in ODM. A data frame organizes data into a two-dimensional table of rows and columns — similar to a spreadsheet.

A data frame contains two main elements:

- **Features** — the entities measured in an experiment (e.g., genes, proteins, metabolites, pathways, sales regions).
- **Measurements (or values)** — the actual values recorded for each feature under different conditions (e.g., gene expression values, protein abundance, pathway activity, sales volume).

### Simple data frame

The simplest data frame has features in the first column and one measurement per sample in each remaining column:

![Simple data frame](../../doc-odm-user-guide/doc-odm-user-guide/images/data-frame1.png)

### Complex data frame

A complex data frame uses multiple columns to describe each feature (e.g., gene name, protein name, peptide sequence, PTM site) and may also include multiple measurement types per sample (e.g., expression level, quality flag, Fold Change, p-value):

![Complex data frame](../../doc-odm-user-guide/doc-odm-user-guide/images/data-frame2.png)

### Multiple measurements per sample

If each sample has more than one measurement type (e.g., Intensity and Quality Pass), column names must encode both the sample name and the measurement type using a separator:

- The separator must appear in every column name.
- Only the **first** occurrence of the separator is used for parsing.
- The separator must be specified at upload time (via API or GUI).
- Every sample must have the same set of measurement types.

**Example** (separator is `.`):

| Sample1.Intensity | Sample1.QualityPass | Sample2.Intensity | Sample2.QualityPass |
|-------------------|---------------------|-------------------|---------------------|
| 5.4               | Pass                | 7.8               | Pass                |
| 4.9               | Fail                | 8.1               | Pass                |

---

## Cross-reference mapping file

A cross-reference mapping file can be imported to link transcript IDs to gene IDs. It is a two-column TSV with headers `TXNAME` and `GENEID`. The first column (transcript IDs) must be unique. The file must be hosted at an HTTPS location accessible to ODM.

| TXNAME            | GENEID            |
|-------------------|-------------------|
| ENST00000438176.2 | ENSG00000231103.2 |
| ENST00000445563.2 | ENSG00000226662.2 |

---

## File requirements and limitations

- All columns must have names.
- All feature columns must be consecutive on the left side of the file. The number of feature columns must be specified explicitly during upload.
- Missing values must be coded as one of: ` ` (space), empty (no symbol between two tabs), `NaN`, `null`, `N/A`, `NA`, `filtered`, `Inf`, `-Inf`.
- ODM automatically classifies each feature column as string or numeric. If a column intended as numeric contains any non-numeric value (other than the accepted missing-value codes), it is treated as a string column, disabling range-based search for that column.
- Measurement columns must contain only numeric values or accepted missing values.

!!! note "Recommended column ordering"
    When a file has more than one feature column, place the most important identifier (e.g., Gene Name, Protein Name) as the first column. This enables faster search after upload.
