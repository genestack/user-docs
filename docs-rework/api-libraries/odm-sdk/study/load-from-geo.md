---
diataxis: how-to
tab: api-libraries
---

# Load data from GEO

This guide explains how to prepare a GEO series matrix file for import into ODM using the `odm-geo-prepare` script.

## Prerequisites

- Configured ODM SDK. See [Configure the ODM SDK](../configure.md).
- The `pandas` library installed. The latest available version is recommended.
- A GEO series matrix file, for example [`GSE29746_series_matrix.txt`](../../../assets/tools/odm-sdk/terminal/study/loading-from-geo/GSE29746_series_matrix.txt).

## Steps

1. Run the preparation script, providing the series matrix file as an argument:

   ```shell
   odm-geo-prepare GSE29746_series_matrix.txt
   ```

2. The script creates a folder containing three files ready for import into ODM. For example:

   ```shell
   ├── GSE29746
   │   ├── GSE29746_expression.gct
   │   ├── GSE29746_samples.tsv
   │   └── GSE29746_study.tsv
   ```

3. Upload the generated files to AWS S3 or another accessible URL host, then import them into ODM using the [Upload a study](upload-a-study.md) workflow.

## Related

- [Upload a study](upload-a-study.md)
