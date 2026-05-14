# Cross-reference mapping explained

## What is a cross-reference mapping?

A **cross-reference (xref) mapping** is a lookup table that links identifiers from one biological namespace to identifiers in another. In ODM the most common use case is mapping transcript IDs to gene IDs — for example, mapping an Ensembl transcript identifier such as `ENST00000438176.2` to its parent gene `ENSG00000231103.2`.

The mapping file itself is a simple two-column TSV where the first column holds the transcript IDs (which must be unique) and the second column holds the corresponding gene IDs:

| TXNAME            | GENEID            |
|-------------------|-------------------|
| ENST00000438176.2 | ENSG00000231103.2 |
| ENST00000445563.2 | ENSG00000226662.2 |

The first row must contain column headers. The file must be hosted at an HTTPS location accessible to ODM before it can be imported. Additional metadata about the mapping (such as organism) can be supplied as key–value pairs at import time.

## Why cross-reference mappings are needed

Omics data is commonly measured and stored at the transcript level, but researchers typically think and query at the gene level. Without a mapping between the two, it is impossible to answer questions such as "find all samples where expression of gene X exceeds threshold Y" when the underlying data files use transcript identifiers.

By importing an xref mapping and linking it to an expression data file, ODM can resolve transcript-level features to gene-level identifiers on the fly. This means users can supply either gene IDs or transcript IDs to OMICS query endpoints and get consistent results, regardless of how the original data was stored.

Mappings are associated with expression data files but are shared across an organisation: once a mapping is uploaded, any user can query it. A single mapping file can also be linked to multiple expression data objects if they share the same identifier space.

## When you need a cross-reference mapping

You need a cross-reference mapping when:

- Your expression data files use transcript-level identifiers (e.g. Ensembl transcript IDs) but you want to query or filter at the gene level.
- You want to enable transcript↔gene lookups across studies in your organisation.
- You are integrating data from pipelines that produce transcript-level quantification (e.g. Salmon, kallisto) with downstream analysis that expects gene-level features.

You do not need a cross-reference mapping if your expression data already uses gene-level identifiers, or if transcript-to-gene resolution is handled entirely outside ODM.

[PLACEHOLDER: expand with examples of when xref mapping is needed]

## See also

- [`../how-to/studies-import/xref-mapping.md`](../how-to/studies-import/xref-mapping.md) — step-by-step instructions for importing and linking a cross-reference mapping file
