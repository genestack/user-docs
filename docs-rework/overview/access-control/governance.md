---
diataxis: explanation
tab: overview
---

# Data governance

The ODM platform indexes both data and metadata to support efficient search and exploration.

## Metadata

A structured representation of metadata is stored in ODM's internal MySQL database. This acts as a partial copy of metadata, ensuring fast performance for search, filtering, and data exploration.

## Raw data

Raw files (for example images or BAM files) are not copied into ODM. Instead, ODM stores pointers to the files in their existing storage locations.

## Processed and indexed data

Processed data is stored in a columnar database, enabling it to be indexed and searchable within ODM.

## Attachments

When data files are imported via the GUI or attached to a study (for example, supplementary documents), they must be uploaded into the platform's S3 bucket. This creates a copy of the file in ODM, ensuring accessibility through the user interface. See [Attached files](../supported-data-formats/attached-files.md) for supported file types.

## Current limitation

ODM currently supports a single S3 bucket for attachments.

## Storage summary

| Type | Example | Details | Copy | Configurability |
|---|---|---|---|---|
| Attachments | .pdf, .ppt, .h5 — can be anything | ODM indexes basic file metadata (name, date, type, file contents for archives like .zip and .h5) | Copy always stored in ODM's S3 bucket | Can configure to use the customer's S3 bucket |
| Metadata | TSV metadata files (e.g. sample, library, preparation) | ODM captures and indexes study, sample, library/preparation, and other metadata | Copy always stored in ODM's databases | No region separation; use permissions to control access |
| Raw data | .fastq, .bam, images, and similar — not an attachment and not indexed data | ODM stores and indexes the pointer to the file only | No copy made | |
| Indexed data | Tabular data, VCFs, and similar | ODM indexes most of the data by storing a compressed partial copy of the data columns | Copy made | No configurability |
