---
diataxis: explanation
tab: overview
---

# Metadata Editor

The Metadata Editor is the central interface for working with study, sample, and data metadata in ODM. It is where you go to read the metadata associated with a study and, if you have curation permissions, to edit and validate it.

## Getting there

To open an existing study in the Metadata Editor, click its title in the Study Browser. The editor opens in a new tab and shows everything ODM holds about that study: its descriptive metadata, sample attributes, any linked library or preparation entities, and the metadata for associated data files.

You can also arrive at the Metadata Editor by clicking **Create a new study** on the Dashboard. In that case, ODM opens a blank study and prompts you to select a metadata template before you begin.

## View mode and edit mode

Every user can open the Metadata Editor, but what you can do once you're there depends on your group membership. By default, the editor opens in view mode: you can read all the metadata in the study but cannot modify it.

Edit mode is available to members of the Curator group. In edit mode you can update metadata values, validate them against the applied template, and manage samples. To understand how metadata changes are tracked over time, see [About metadata versioning](../../contribute/version-metadata/about-metadata-versioning.md). For step-by-step guidance on making changes, see [Edit and validate metadata](../../contribute/curate-metadata/edit-and-validate-metadata.md).

## The study title drop-down menu

Clicking the study title at the top of the page opens a drop-down menu that provides several actions. **Share** lets you grant access to colleagues. See [Share a study](../../contribute/sharing/share-a-study.md) for details. **Export** generates a download link you can use to retrieve data. See [Export data](../../explore/export-data.md). **Rename** lets you change the study title directly. **Copy accession** copies the study's unique accession number to your clipboard. **More info** shows the study's creation date, last modification date, owner, and the groups it has been shared with. **Apply another template** changes the metadata template applied to the study. See [Change a study's template](../../contribute/templates/change-a-studys-template.md).

## The tabs

The Metadata Editor organises content across several tabs.

![Animated overview of the study tabs in the Metadata Editor](../../assets/user-guide/doc-odm-user-guide/doc-odm-user-guide/gifs/study-tabs.gif)

The **Study** tab holds the foundational framework for the research project (its objective, hypotheses, experimental design, and statistical methods) along with general information such as the study's description, contributors, and contact details. Any metadata column containing an invalid value is highlighted in red, making it easy to spot entries that need attention.

The **Samples** tab shows per-sample metadata: attributes such as organism, cell line, and disease. Columns that come from the applied template are highlighted in yellow to distinguish them from manually added columns.

The **+More** tab (if present) gives access to additional entity types (Libraries, Preparations, or others) when those entities are part of the study. Not all studies include these.

The **Data** tab shows metadata for the data files associated with the study, such as expression or variant data. If multiple versions of an omics file exist, you can toggle between them here to compare their metadata.

The **Explore** tab is a visualisation view: select up to two sample attributes to generate a plot and cross-examine your data. For step-by-step guidance, see [Explore sample data visually](../../explore/visualise-sample-data.md).

## Where to go from here

To curate metadata in the editor, start with [Edit and validate metadata](../../contribute/curate-metadata/edit-and-validate-metadata.md). To explore a study's metadata as a reader, see [View study metadata](../../explore/view-study-metadata.md). To understand how ODM tracks changes across metadata versions, visit the [version metadata section](../../contribute/version-metadata/index.md). To transfer ownership of a study to another user, see [Transfer study ownership](../../contribute/sharing/transfer-study-ownership.md).
