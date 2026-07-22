---
diataxis: reference
tab: api-libraries
---

# Script parameters reference: `odm-import-data`

This reference describes every parameter of the `odm-import-data` script, the data model variants it supports, and the rules governing linking, cross-reference mapping, versioning, and multiple tabular files.

For a practical walkthrough of common usage patterns, see [Upload a study](upload-a-study.md).

---

## Authentication parameters

| Flag | Description |
|------|-------------|
| `-t, --token` | Genestack API token. |
| `-at, --access-token` | Identity provider Bearer token. When using an access token, always specify `--template`. |
| `-H, --host, -srv, --server` | URL of the ODM instance, e.g. `https://odm.genestack.com/`. |
| `-u, --user` | Alias registered via `odm-user-setup`. |

---

## Data source parameters

| Flag | Description |
|------|-------------|
| `-s, --study` | URL of the study TSV file. |
| `-sa, --study-accession` | Accession of an existing study to update. |
| `-sm, --samples` | URL of the samples TSV file, or accession of existing samples. |
| `-lb, --libraries` | URL of the libraries TSV file, or accession of existing libraries. |
| `-pr, --preparations` | URL of the preparations TSV file, or accession of existing preparations. |
| `-c, --cell, --cells` | URL of the cell metadata TSV file. Input format is TSV (same as `/api/v1/jobs/import/cells`). Supports multiple imports in one run. Linking targets: Samples, Libraries, or Preparations. |
| `-e, --expression` | URL of a tabular data file (TSV or GCT). Also used for cell expression data. |
| `-em, --expression-metadata` | URL of the expression metadata TSV file. |
| `-v, --variant` | URL of the variant data file (VCF). |
| `-vm, --variant-metadata` | URL of the variant metadata TSV file. |
| `-f, --flow-cytometry` | URL of the flow cytometry data file (`.facs`). |
| `-fm, --flow-cytometry-metadata` | URL of the flow cytometry metadata TSV file. |
| `-fl, --file` | URL of an attachment file. |
| `-flm, --file-metadata` | URL of the metadata file for the attachment. |
| `-tmpl, --template` | Accession of a template to validate against. If not specified, the organisation default template is used. Required when using `--access-token`. |

---

## Cross-reference mapping parameters

| Flag | Description |
|------|-------------|
| `-mpf, --mapping-file` | URL of the mapping file. |
| `-mpfm, --mapping-file-metadata` | URL of the mapping metadata file. |
| `-mpfa, --mapping-file-accession` | Accession of an existing mapping file to link. |

Rules:

1. `--mapping-file` and `--mapping-file-metadata` can only be specified together with expression data. If used without expression data, the script returns: "mapping file is supported with expression matrices only."
2. `--mapping-file-accession` also requires expression data to be present.
3. `--mapping-file-metadata` cannot be specified without `--mapping-file`.
4. For each sample group, specify either the pair (`--mapping-file` + `--mapping-file-metadata`) or `--mapping-file-accession`, not both.
5. Mapping file parameters must appear after the expression data parameters in the command.
6. If `--link-all-to-all` is also specified, the script links the mapping file to all expression data that was specified. Only one mapping file can be specified alongside `--link-all-to-all`.

---

## Behaviour-control parameters

| Flag | Description |
|------|-------------|
| `--allow-duplicates` | Re-import files that have already been loaded into ODM (useful for testing). |
| `-lata, --link-all-to-all` | Bypass sequential linking — see "Link all to all" below. |
| `--debug` | Enable debug output. |
| `-ile, --ignore-linking-errors` | Continue the import even if linking errors occur between study entities. |
| `-nfa N, --number-of-feature-attributes N` | Number of leading columns in expression files that are feature attributes rather than sample values. |
| `-ms ':', --measurement-separator ':'` | Character used to distinguish the sample/library/preparation name from the measurement name in column headers when expression files contain multiple measurements. |
| `-dc 'C', --data-class 'C'` | Data class for the uploaded omics data. If not specified, defaults to `Other`. |

---

## Data class values

Accepted values for `--data-class`:

`Bulk transcriptomics`, `Single cell transcriptomics`, `Differential abundance (FC, pval, etc.)`, `Pathway analysis`, `Proteomics`, `Single cell proteomics`, `Metabolomics`, `Lipidomics`, `Epigenomics`, `DNA methylation`, `Chemoinformatics`, `Imaging features`, `Gene panel data`, `Biomarker data`, `Physical measures`, `Blood counts`, `Other body fluid counts`, `Long-read sequencing (Nanopore, PacBio)`, `Gene variant (VCF)`, `Flow Cytometry`, `Spatial transcriptomics`, `Phenomics`, `Copy number alterations`, `Microbiome / Metagenomics`, `Genetic screens (CRISPR / RNAi)`, `Cell imaging`, `Document`, `Other`.

---

## Data model variants

The script supports three data model variants, and selects among them based on which parameters are supplied:

- **Study → Samples → Omics data**, used when no libraries, preparations, or cell metadata parameters are specified.
- **Study → Samples → Libraries/Preparations → Omics data**, used when libraries or preparations parameters are specified. Omics data is linked only to libraries or preparations. Only expression data (via `--expression` and `--expression-metadata`) is supported at this level.
- **Study → Samples → (optional Libraries/Preparations) → Cell metadata → Omics data**, used when the `--cell` or `--cells` parameter is specified. Expression data is linked to cell metadata.

The script works sequentially, linking each object to the one immediately preceding it in the chain.

### Sequential linking examples

**Example 1 (two expression files linked to the same samples):**

```shell
odm-import-data --token [token] -H [HOST] \
  --study http://data_source/study.csv \
  --samples http://data_source/samples_1.csv \
  --expression http://data_source/expression_1.gct \
  --expression-metadata http://data_source/expression_metadata_1.gct.tsv \
  --expression http://data_source/expression_2.gct \
  --expression-metadata http://data_source/expression_metadata_2.gct.tsv
```

- `samples_1` linked to `study`
- `expression_1` linked to `samples_1`
- `expression_2` linked to `samples_1`

**Example 2 (libraries and preparations with separate expression files):**

```shell
odm-import-data --token [token] -H [HOST] \
  --study http://data_source/study.csv \
  --samples http://data_source/samples_1.csv \
  --libraries http://data_source/libraries_1.csv \
  --expression http://data_source/expression_1.gct \
  --expression-metadata http://data_source/expression_metadata_1.gct.tsv \
  --preparations http://data_source/preparations_1.csv \
  --expression http://data_source/expression_2.gct \
  --expression-metadata http://data_source/expression_metadata_2.gct.tsv
```

- `samples_1` linked to `study`
- `libraries_1` linked to `samples_1`
- `expression_1` linked to `libraries_1`
- `preparations_1` linked to `samples_1`
- `expression_2` linked to `preparations_1`

**Example 3 (multiple samples, libraries, and preparations):**

```shell
odm-import-data --token [token] -H [HOST] \
  --study http://data_source/study.csv \
  --samples http://data_source/samples_1.csv \
  --samples http://data_source/samples_2.csv \
  --libraries http://data_source/libraries_1.csv \
  --preparations http://data_source/preparations_1.csv \
  --expression http://data_source/expression_1.gct \
  --expression-metadata http://data_source/expression_metadata_1.gct.tsv
```

- `samples_1` linked to `study`
- `samples_2` linked to `study`
- `libraries_1` linked to `samples_2`
- `preparations_1` linked to `samples_2`
- `expression_1` linked to `preparations_1`

**Example 4 (cell metadata with libraries):**

```shell
odm-import-data --token [token] -H [HOST] \
  --study http://data_source/study.csv \
  --samples http://data_source/samples_1.csv \
  --samples http://data_source/samples_2.csv \
  --libraries http://data_source/libraries_1.csv \
  --cell http://data_source/cell_1.csv \
  --expression http://data_source/expression_1.gct \
  --expression-metadata http://data_source/expression_metadata_1.gct.tsv
```

- `samples_1` linked to `study`
- `samples_2` linked to `study`
- `libraries_1` linked to `samples_2`
- `cell_1` linked to `libraries_1`
- `expression_1` linked to `cell_1`

---

## Link all to all

The `--link-all-to-all` (`-lata`) flag bypasses sequential linking. Its behaviour depends on the data model:

- If only samples are present: the script links all omics data to all samples.
- If libraries or preparations are present, linking works in two steps: first all libraries and all preparations are linked to all samples; then all omics data is linked to all libraries and preparations.

**Example 1, without `--link-all-to-all` (sequential):**

```shell
odm-import-data --token [token] -H [HOST] \
    --study http://data_source/study.csv \
    --samples http://data_source/samples_1.csv \
    --samples http://data_source/samples_2.csv \
    --expression http://data_source/expression_1.gct \
    --expression-metadata http://data_source/expression_metadata_1.gct.tsv
```

- `samples_1` linked to `study`
- `samples_2` linked to `study`
- `expression_1` linked only to `samples_2`

**Example 2 (with `--link-all-to-all`):**

```shell
odm-import-data --token [token] -H [HOST] \
    --study http://data_source/study.csv \
    --samples http://data_source/samples_1.csv \
    --samples http://data_source/samples_2.csv \
    --expression http://data_source/expression_1.gct \
    --expression-metadata http://data_source/expression_metadata_1.gct.tsv \
    --link-all-to-all
```

- `samples_1` linked to `study`
- `samples_2` linked to `study`
- `expression_1` linked to `samples_1` and `samples_2`

**Example 3 (with `--link-all-to-all` and libraries):**

```shell
odm-import-data --token [token] -H [HOST] \
    --study http://data_source/study.csv \
    --samples http://data_source/samples_1.csv \
    --samples http://data_source/samples_2.csv \
    --libraries http://data_source/libraries_1.csv \
    --preparations http://data_source/preparations_1.csv \
    --expression http://data_source/expression_1.gct \
    --expression-metadata http://data_source/expression_metadata_1.gct.tsv \
    --link-all-to-all
```

- `samples_1` linked to `study`
- `samples_2` linked to `study`
- `libraries_1` linked to `samples_1` and `samples_2`
- `preparations_1` linked to `samples_1` and `samples_2`
- `expression_1` linked to `preparations_1` and `libraries_1`

---

## Study name handling

By default, the value of the `Study Title` field in the study metadata file is used as the study name. If no `Study Title` field is present, the name is set to `New Study`. Studies can be renamed after import via the ODM UI.

---

## Importing multiple tabular files with different feature attribute counts

When a dataset contains multiple tabular files in TSV format with different numbers of feature attribute columns, specify the `-nfa` flag separately for each file. The `-dc` flag also applies per file; if omitted for a given file, the data class defaults to `Other`.

Example:

```shell
odm-import-data \
--token <TOKEN> \
--server <HOST> \
--study https://s3.amazonaws.com/bio-test-data/odm/Test_1000g/Test_1000g.study.tsv \
--samples https://bio-test-data.s3.us-east-1.amazonaws.com/odm/user-guide/Test_samples.tsv \
--expression https://bio-test-data.s3.us-east-1.amazonaws.com/odm/user-guide/Test_basic_generic_expression.tsv \
-nfa 4 \
-dc "Lipidomics" \
--expression https://bio-test-data.s3.us-east-1.amazonaws.com/odm/user-guide/Test_basic_generic_expression_3nfa.tsv \
-nfa 3
```

In this example, the first expression file has 4 feature attribute columns and the data class `Lipidomics`; the second has 3 feature attribute columns and defaults to `Other`.

---

## Versioning

You can update an existing omics data file by appending the accession of the file to be updated in square brackets to the data file URL. Previous versions of the file are retained; the active version is set to the most recently uploaded.

```shell
odm-import-data --token [token] -H [HOST] \
    --study-accession GSF994039 \
    --samples GSF994040 \
    --expression http://exampl.com/expression.gct[GSF994565]  \
    --expression-metadata http://exampl.com/expression_metadata.tsv  \
    --variant http://exampl.com/variations.vcf[GSF994700] \
    --variant-metadata http://exampl.com/variant_metadata.tsv
```

This updates the expression file as a new version of `GSF994565` and the variant file as a new version of `GSF994700`. Versioning only works for data files linked to existing studies and samples; you cannot create a new study or new samples at the same time as updating a data file version.

---

## Debugging

Add `--debug` to any command to generate more detailed output. The debug output includes the message returned by the server, which can help diagnose issues with input files.
