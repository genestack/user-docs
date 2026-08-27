---
diataxis: reference
tab: overview
---

# Data classes reference

Data classes categorise data objects in ODM. You choose the class when you import a file, in the UI or through the API, and the class determines how the data is indexed and how it appears in the Study Browser and the study's Data tab.

Every class also has a three-letter code. That code is the badge shown next to a study in the Study Browser, so you can see at a glance which kinds of data a study holds. Flow Cytometry (FACS) and Flow Cytometry (FCS) are separate classes that share the `FCY` badge.

| Data class | Code |
|---|---|
| Bulk transcriptomics | `EXP` |
| Single-cell transcriptomics | `SCT` |
| Differential abundance (FC, pval, etc.) | `DAN` |
| Pathway analysis | `PWA` |
| Proteomics | `PTX` |
| Single-cell proteomics | `SCP` |
| Metabolomics | `MTB` |
| Lipidomics | `LIP` |
| Epigenomics | `EPX` |
| DNA methylation | `DMT` |
| Chemoinformatics | `CHX` |
| Imaging features | `IMG` |
| Gene panel data | `PAN` |
| Biomarker data | `BMK` |
| Physical measures | `PHM` |
| Blood counts | `BLC` |
| Other body fluid counts | `OFC` |
| Long-read sequencing (Nanopore, PacBio) | `LRS` |
| Gene variant (VCF) | `VAR` |
| Flow Cytometry (FACS) | `FCY` |
| Flow Cytometry (FCS) | `FCY` |
| Spatial transcriptomics | `SPT` |
| Phenomics | `PHE` |
| Copy number alterations | `CNA` |
| Microbiome / Metagenomics | `MIC` |
| Immune repertoire | `IMR` |
| Genetic screens (CRISPR / RNAi) | `GSC` |
| Cell imaging | `CIM` |
| Document | `DOC` |
| Other | `OTR` |

## File format follows the import route, not the class

A data class does not imply a file format. The format you can supply is decided by the endpoint you import through, and the data class travels as a separate parameter on that request. The same class can therefore legitimately arrive in more than one format: Proteomics is TSV when you import it as a measurement matrix, and PDF when you attach it as a file.

| Import route | Format | Data classes accepted |
|---|---|---|
| [`/api/v1/jobs/import/expression`](../../odm-api/contribute/import-data/import-expression-data.md) | TSV or GCT | Any data class |
| [`/api/v1/jobs/import/file`](../../odm-api/contribute/import-data/import-attached-files.md) | Any file, held as an attachment | Any data class |
| [`/api/v1/jobs/import/variant`](../../odm-api/contribute/import-data/import-variant-data.md) | VCF, with TSV metadata | Gene variant (VCF) |
| [`/api/v1/jobs/import/flow-cytometry`](../../odm-api/contribute/import-data/import-flow-cytometry-data.md) | FACS or FCS, with TSV metadata | Flow Cytometry (FACS), Flow Cytometry (FCS) |

Two constraints sit on top of that. A GCT file must always be imported as Bulk transcriptomics, whereas a TSV file accepts any class. Single-cell data is a different format family altogether: it is read from HDF5 files with the extensions `.h5`, `.h5ad`, and `.h5mu`, described in [HDF5](../supported-data-formats/hdf5.md).

## Indexing

The **Document** and **Other** classes are for attached files (PDFs, spreadsheets, images, and similar). The contents of files in these classes are not indexed or made searchable in ODM.

All other classes produce indexed data objects that are searchable and filterable in the Study Browser.
