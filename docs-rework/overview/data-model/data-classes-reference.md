---
diataxis: reference
tab: overview
---

# Data classes reference

Data classes categorise data objects in ODM. The class is selected at import time (via the UI or the API) and determines how data is indexed and how it appears in the Study Browser and Data tab.

| Data class | Code | Typical format | Notes |
|---|---|---|---|
| Bulk transcriptomics | | TSV, GCT 1.2 | |
| Single-cell transcriptomics | | | |
| Differential abundance (FC, pval, etc.) | | TSV | |
| Pathway analysis | | TSV | |
| Proteomics | | TSV | |
| Single-cell proteomics | | | |
| Metabolomics | `MTB` | TSV | Code renamed from `MTX` in release 1.62 |
| Lipidomics | | | Added in release 1.58 |
| Epigenomics | | TSV | |
| DNA methylation | | TSV | |
| Chemoinformatics | | TSV | |
| Imaging features | | TSV | |
| Gene panel data | | TSV | |
| Biomarker data | | TSV | |
| Physical measures | | TSV | |
| Blood counts | | TSV | |
| Other body fluid counts | | TSV | |
| Long-read sequencing (Nanopore, PacBio) | `LRS` | | Renamed from "Nanopore" in release 1.62 |
| Gene variant (VCF) | | VCF | |
| Flow Cytometry (FACS) | | FACS | Renamed from "Flow Cytometry" in release 1.59 |
| Flow Cytometry (FCS) | | FCS | Added in release 1.59 |
| Spatial transcriptomics | `SPT` | | Added in release 1.62 |
| Phenomics | `PHE` | | Added in release 1.62 |
| Copy number alterations | `CNA` | | Added in release 1.62 |
| Microbiome / Metagenomics | `MIC` | | Added in release 1.62 |
| Immune repertoire | `IMR` | | Added in release 1.62 |
| Genetic screens (CRISPR / RNAi) | `GSC` | | Added in release 1.62 |
| Cell imaging | `CIM` | | Added in release 1.62 |
| Document | | PDF, XLSX, DOCX, PPTX, images | Not indexed; for attached files |
| Other | | | Not indexed; for attached files |

The **Document** and **Other** classes are for attached files (PDFs, spreadsheets, images, and similar). The contents of files in these classes are not indexed or made searchable in ODM.

All other classes produce indexed data objects that are searchable and filterable in the Study Browser.
