# How-to guides

Task-oriented guides for solving specific problems in ODM.

## Users & Access

- [Manage your profile](users-access/manage-your-profile.md) — view and update your profile, check assigned permissions.
- [Manage users](users-access/manage-users.md) — create users, assign permissions, and deactivate accounts. *(Administrator)*
- [Manage groups](users-access/manage-groups.md) — create and manage user groups, assign curator groups. *(Administrator)*
- [Generate an API token](users-access/generate-api-token.md) — generate a personal API token for programmatic access.
- [Authenticate with Azure AD](users-access/azure-authentication.md) — set up Azure Active Directory authentication.

## Studies & Import

- [Create a study](studies-import/create-a-study.md) — create a new empty study via the interface. *(Contributor)*
- [Import samples and libraries (interface)](studies-import/import-samples-gui.md) — import sample metadata, libraries, and preparations via the GUI. *(Contributor)*
- [Import omics data (interface)](studies-import/import-omics-data-gui.md) — import experimental data and link files via the GUI. *(Contributor)*
- [Attach files to a study](studies-import/import-attached-files.md) — attach non-indexed files (PDFs, scripts) to a study. *(Contributor)*
- [Import samples and libraries (API)](studies-import/import-samples-api.md) — authoritative guide for metadata import via the REST API. *(Contributor)*
- [Import omics data (API)](studies-import/import-omics-data-api.md) — import expression, variant, FACS, and attached files via API. *(Contributor)*
- [Import data using the Python script](studies-import/import-data-python.md) — use the `import_ODM_data.py` helper script. *(Contributor)*
- [Manage cross-reference mappings](studies-import/xref-mapping.md) — import, query, update, and remove xref mappings. *(Contributor/Consumer)*
- [Gene-transcript mapping](studies-import/gene-transcript-mapping.md) — map gene and transcript IDs. *(Contributor)*
- [Transform attached files (CSV to TSV)](studies-import/transform-attachments.md) — convert attached CSV files to TSV format. *(Contributor)*
- [Manage study versions](studies-import/manage-versions.md) — publish, discard, and restore metadata versions. *(Contributor)*

## Metadata & Templates

- [View study metadata](metadata-templates/view-metadata.md) — navigate and read study, sample, and data metadata.
- [Edit study metadata](metadata-templates/edit-metadata.md) — edit study, sample, and data metadata fields. *(Contributor)*
- [Bulk replace metadata values](metadata-templates/bulk-replace-metadata.md) — replace a value across many rows at once. *(Contributor)*
- [Validate metadata](metadata-templates/validate-metadata.md) — run validation and review errors. *(Contributor)*
- [Create and customise a template](metadata-templates/create-template.md) — build or modify a metadata template. *(Contributor)*
- [Export a template](metadata-templates/export-template.md) — download a template for reuse. *(Contributor)*

## Search & Export

- [Search for studies and data](search-export/search-studies.md) — use the Study Browser to find studies by keyword or attribute.
- [Filter and facet search results](search-export/filter-facets.md) — narrow results using facets and filter panels.
- [Export data from a study](search-export/export-data.md) — download study data in various formats.

## Sharing & Permissions

- [Share a study with a group](sharing-permissions/share-a-study.md) — grant a user group access to a study. *(Contributor/Administrator)*

## Single Cell

- [Import single-cell data](single-cell/import-single-cell-data.md) — upload and register H5AD files. *(Contributor)*
- [HDF5 transformations](single-cell/hdf5-transformations.md) — run and configure the HDF5 transformation pipeline. *(Contributor)*
