---
diataxis: how-to
tab: api-libraries
---

# Upload a study

This guide explains how to import a complete study into ODM using the `odm-import-data` script. The script handles everything in a single run: creating the study, importing samples and optional entity types (libraries, preparations, cell metadata), and linking all loaded data according to the ODM data model.

## Prerequisites

- Configured ODM SDK. See [Configure the ODM SDK](../configure.md).
- An API token or alias. See [Authentication and tokens](../../../odm-api/getting-started/authentication-and-tokens.md).
- The `pandas` library installed. The latest available version is recommended.
- All data files hosted at accessible URLs (HTTPS, S3, or NFS). The script does not load files from your local machine. See the supported data formats documentation for file format requirements.

## Basic usage

With a Genestack API token:

```shell
odm-import-data --token <TOKEN> --host <HOST> \
  --study <URL to study file> \
  --samples <URL to samples file>
```

With an Access (Bearer) token (when using an access token, you must always specify a template accession):

```shell
odm-import-data --access-token <TOKEN> --host <HOST> \
  --study <URL to study file> \
  --samples <URL to samples file> \
  --template <ACCESSION>
```

## Adding optional data files

Append any combination of the following flags to include additional entity types and data:

- `--expression <URL> --expression-metadata <URL>`, tabular expression data (TSV or GCT) and its metadata.
- `--variant <URL> --variant-metadata <URL>`, variant data (VCF) and its metadata.
- `--flow-cytometry <URL> --flow-cytometry-metadata <URL>`, flow cytometry data and its metadata.
- `--mapping-file <URL> --mapping-file-metadata <URL>`, cross-reference mapping file and its metadata.
- `--libraries <URL>`, libraries metadata.
- `--preparations <URL>`, preparations metadata.
- `--cell <URL>` (or `-c`), cell metadata (single-cell). The input format is TSV, matching the `/api/v1/jobs/import/cells` endpoint format.

For uploading cell expression, use the regular `--expression` parameter. For the full parameter list and behaviour-control flags, see [Script parameters reference](script-parameters-reference.md).

## Representative examples

### Basic study with expression data

```shell
odm-import-data --token <TOKEN> -H <HOST> \
  --study http://data_source/Test.study.tsv \
  --samples http://data_source/Test.samples.tsv \
  --expression-metadata http://data_source/Test.expression.gct.tsv \
  --expression http://data_source/Test.expression.gct
```

### Study with libraries and preparations

```shell
odm-import-data --token <TOKEN> -H <HOST> \
  --study http://data_source/Test.study.tsv \
  --samples http://data_source/Test.samples.tsv \
  --libraries http://data_source/Test.libraries.tsv \
  --preparations http://data_source/Test.preparations.tsv \
  --expression-metadata http://data_source/Test.expression.gct.tsv \
  --expression http://data_source/Test.expression.gct
```

### Single-cell study (Study → Samples → Cells → Expression)

```shell
odm-import-data \
  --server <HOST> \
  --token <TOKEN> \
  --study 's3://bio-test-data/User_guide_test_data/Single_cell_data/study_metadata.tsv' \
  --samples 's3://bio-test-data/User_guide_test_data/Single_cell_data/samples.tsv' \
  --cells 's3://bio-test-data/User_guide_test_data/Single_cell_data/cells_2_samples_full_match.tsv' \
  --expression 's3://bio-test-data/User_guide_test_data/Single_cell_data/expression_2_cells_linked_to_samples.tsv' \
  --data-class 'Single-cell transcriptomics' \
  --number-of-feature-attributes 1 \
  --allow-duplicates
```

## Verifying the import

The script returns a `jobExecutionIdentifier` (available since release 1.34) that you can use to monitor import progress via the API. See [Job status codes reference](../../../odm-api/reference/job-status-codes-reference.md).

## How linking works

The script links entities sequentially according to the data model: samples are linked to the study, then data files are linked to the immediately preceding entity (samples, libraries, preparations, or cells). Linking happens automatically as part of the script run.

For full details on data model variants (Study → Samples → Omics, Study → Samples → Libraries/Preparations → Omics, and the cell metadata variant), sequential linking rules, and the `--link-all-to-all` flag, see [Script parameters reference](script-parameters-reference.md).

## Explore script options

```shell
odm-import-data -h
```

## Restrictions

The script does not allow loading multiple studies in a single run. It also does not support loading files directly from your local machine; all source files must be hosted at accessible URLs.

## Related

- [Script parameters reference](script-parameters-reference.md), full parameter list, data model variants, link-all-to-all, versioning, and cross-reference mapping rules.
- [Share a study](share-a-study.md), make the imported study visible to your organisation.
- [Delete a study](delete-a-study.md)
- [Load from GEO](load-from-geo.md)
