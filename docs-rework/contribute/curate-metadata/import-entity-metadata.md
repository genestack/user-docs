---
diataxis: how-to
tab: contribute
---

# Import entity metadata from a file

When you need to describe a single entity, you can load its metadata from a TSV file instead of typing the values field by field. This works for a study, for an individual data file, and for an attached file.

!!! info "Before you begin"
    - You are a member of the Curator group.
    - The entity you want to describe already exists: the study is created, and the data file is imported or the file is attached. See [Create a study](../create-a-study.md) and [Import data](../import-data/index.md).

!!! note "Not the same as importing a sample sheet"
    This guide covers metadata for one entity at a time. To replace the whole sample table from a multi-row sample sheet, see [Edit and validate metadata](edit-and-validate-metadata.md), which describes the separate import control on the Samples tab.

## File format

List the attribute names in the first row of your file and their values in the second row. Where a single attribute takes more than one value, separate the values with a pipe character (`|`).

| Study Source | Study Description |
|---|---|
| 1000 Genomes Project | Subset of 1000 Genomes Project |

Technical, read-only keys such as `genestack:accession` are ignored, so you can leave them in the file.

!!! warning "Importing overwrites existing values"
    Values already present on the entity are replaced by the values in your file. Review the file before you import it.

## Steps

1. Open the study in the Metadata Editor and go to the tab holding the entity you want to describe. Study metadata lives on the **Study** tab; data files and attached files live on the **Data** tab.

2. Click **Edit** at the bottom of the page. The **Import metadata** button is available only in edit mode.

3. Click **Import metadata** and select your TSV file.

    <figure markdown="span">
    ![Import metadata on the Study tab](../../assets/user-guide/curate-metadata/metadata_from_tsv.png)
    <figcaption>Importing study metadata from the Study tab in edit mode</figcaption>
    </figure>

    For a data file or an attached file, the same button appears once you select the entity on the Data tab.

    <figure markdown="span">
    ![Import metadata on the Data tab](../../assets/user-guide/curate-metadata/metadata_from_tsv_data_tab.png)
    <figcaption>Importing metadata for a data file from the Data tab in edit mode</figcaption>
    </figure>

4. Click **Publish** and name the version, as you would after any other edit in the Metadata Editor.

---

To correct values by hand once they are loaded, see [Edit and validate metadata](edit-and-validate-metadata.md). For the TSV requirements of each entity type, see [TSV format](../../overview/supported-data-formats/tsv.md).
