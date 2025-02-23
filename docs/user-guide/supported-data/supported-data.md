# Supported Data Formats

!!! info "About this guide"
    This guide provides a basic overview of file formats and data supported in the ODM.
    For a detailed description and instructions on using various data formats and working with them
    (sorting, filtering, sampling), visit the **[Supported Data Formats page](../doc-odm-user-guide/supported-formats.md)** 
    in our **Advanced User Guide**. 

<div class="grid cards" markdown>

- :octicons-table-16: __[TSV (Tabular data)](../supported-data/supported-data.md/#tsv-tabular-data)__

    ---

    Upload and manage tabular data (TSV files) seamlessly within the ODM. Work with Samples, 
    Libraries, Preparations, Expression data, and more.

- :fontawesome-solid-signal:{ .lg .middle } __[GCT (Gene Expression)](../supported-data/supported-data.md/#gct-gene-xpression)__ 

    ---

    Upload and work with GCT (Gene Cluster Text) files in the Open Data Manager (ODM). 
    Optimize the analysis of matrix-compatible datasets.

- :material-dna:{ .lg .middle } __[VCF (Variants)](../supported-data/supported-data.md/#vcf-variants)__

    ---

    Upload and work with VCF (Variant Call Format) files to search, filter, retrieve, and analyze 
    genetic variants in the ODM.

- :fontawesome-solid-disease:{ .lg .middle } __[HDF5 (e.g. Single Cell)](../supported-data/supported-data.md/#hdf5-single-cell)__

    ---
    Upload and store HDF5 (Hierarchical Data Format 5) files as attachments in the ODM. Future releases will enable 
    seamless analysis of Single Cell data stored within TSV and HDF5 formats.

- :fontawesome-solid-wave-square:{ .lg .middle } __[FACS (Flow Cytometry)](../supported-data/supported-data.md/#facs-flow-cytometry)__

    ---
    Upload and work with FACS (Fluorescence-Activated Cell Sorting) files in the Open Data Manager (ODM) 
    to efficiently analyze Flow Cytometry data.

- :fontawesome-solid-file-lines:{ .lg .middle } __[Attached Files](../supported-data/supported-data.md/#attached-files)__

    ---
    Upload and organize a diverse range of attached non-indexed files in the ODM. 
    Easily manage your entire data catalog, access and collaboration across any file types.

</div>

## TSV (Tabular data)

In ODM, you can upload any tabular data formatted as **TSV (tab-separated values)**. 
As long as your file represents a data frame, ODM can import and index it. A data frame is a data structure that 
organizes data into a two-dimensional table of **rows** and **columns**, similar to a spreadsheet.

A data frame contains two main elements:

- **Features**: These are the entities measured in an experiment (e.g., genes, proteins, metabolites, 
pathways, sales regions, etc.).
- **Measurements (or values)**: These are the actual values recorded for each feature under different 
conditions (e.g., gene expression values, protein abundance, pathway activity, sales volume, etc.).

### Simple Data Frame 

The example below demonstrates the simplest and most common type of data frame. 

![Data Frame Simple](../doc-odm-user-guide/doc-odm-user-guide/images/data-frame1.png)

Here, the features (genes) 
are listed in the first column, while the rest of the table contains measurements of gene expression across 
multiple samples. Each column represents a different sample, with the column name indicating the 
corresponding dataset of gene expression values.

### Complex Data Frame

![Data Frame Complex](../doc-odm-user-guide/doc-odm-user-guide/images/data-frame2.png)

This format provides a wide range of data types that can be uploaded and indexed in ODM.

For a detailed description and instructions on using TSV, visit the **[Supported Data Formats page](../doc-odm-user-guide/supported-formats.md)**
in our **Advanced User Guide**.

## GCT (Gene xpression)

For a detailed description and instructions on using GCT, visit the **[Supported Data Formats page](../doc-odm-user-guide/supported-formats.md)**
in our **Advanced User Guide**.

## VCF (Variants)

For a detailed description and instructions on using VCF, visit the **[Supported Data Formats page](../doc-odm-user-guide/supported-formats.md)**
in our **Advanced User Guide**.

## HDF5 (e.g. Single Cell)

For a detailed description and instructions on using HDF5, visit the **[Supported Data Formats page](../doc-odm-user-guide/supported-formats.md)**
in our **Advanced User Guide**.

## FACS (Flow Cytometry)

For a detailed description and instructions on using FACS, visit the **[Supported Data Formats page](../doc-odm-user-guide/supported-formats.md)**
in our **Advanced User Guide**.

## Attached Files

For a detailed description and instructions on using Attached Files, visit the **[Supported Data Formats page](../doc-odm-user-guide/supported-formats.md)**
in our **Advanced User Guide**.
