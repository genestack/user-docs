# Loading from GEO

This article describes how to prepare a series matrix file from GEO to be loaded to ODM.

## Requirements

- Configured odm-sdk. See [Configured odm-sdk](../../configuration.md)
- Having `pandas` library installed. We recommend using the latest version available.
- Data file from GEO, for example [GSE29746_series_matrix.txt](loading-from-geo/GSE29746_series_matrix.txt)

## Instructions

Run the script providing the `GSE29746_series_matrix.txt` file as an argument

```bash
odm-geo-prepare GSE29746_series_matrix.txt
```

As a result, the script creates the folder with 3 files ([example](loading-from-geo/GSE29746.zip)), that you can use to load to ODM.
For example:

```bash
├── GSE29746
│   ├── GSE29746_expression.gct
│   ├── GSE29746_samples.tsv
│   └── GSE29746_study.tsv
```

Load your files to AWS S3 and then to ODM following the [instructions](uploading-study.md)
