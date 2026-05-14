# Getting Started: Data Contributor

A Data Contributor can create studies, import data, curate metadata, manage templates, share studies, and export data in the Open Data Manager. Contributors have all the read capabilities of a Consumer, plus write access: you can upload study metadata, import sample and experimental data, validate and correct metadata against templates, and control who can see your studies.

## Where to start

Work through [Your First Session](../tutorials/your-first-session.md) to get oriented in the ODM interface before importing your own data.

## Common tasks

- [Create a study](../how-to/studies-import/create-a-study.md) — set up a new study with a name and template
- [Import sample metadata (GUI)](../how-to/studies-import/import-samples-gui.md) — upload a TSV file of sample attributes through the interface
- [Import omics data (GUI)](../how-to/studies-import/import-omics-data-gui.md) — add experimental data files (GCT, VCF, TSV, FACS, etc.)
- [Edit metadata](../how-to/metadata-templates/edit-metadata.md) — curate and validate metadata against a template
- [Create a template](../how-to/metadata-templates/create-template.md) — define the metadata structure and validation rules for your studies
- [Share a study](../how-to/sharing-permissions/share-a-study.md) — grant other users or groups access to your study

## Using the interface

The ODM data model has five layers: Study, Samples, Libraries, Preparations, and Experimental Data. All layers are linked via shared identifiers (primarily `Sample Source ID`).

- **Create a study**: click **Create new study** on the dashboard or from the top-left menu. Assign a name and select a metadata template.
- **Add sample metadata**: on the **Samples** tab, click **Edit**, then click the upload icon to import a TSV file. Click **Publish** to save, adding a version label such as *"Sample metadata added"*.
- **Add libraries and preparations** (optional): click **+More** on the study tabs and upload TSV files. Ensure the `Sample Source ID` column links them to your samples.
- **Import experimental data**: on the **Data** tab, click **Add data**, select a data class (for example, Bulk Transcriptomics), and choose a file from your local computer or external storage (for example, AWS). The file is indexed and becomes searchable once linked via `Sample Source ID`.
- **Attach supplementary files**: use **Add data → Attach a file** for PDFs, presentations, or other documents. Attached files are not indexed or searchable.
- **Curate metadata**: on the **Samples** tab in Edit mode, invalid values are highlighted in red. Use ontology suggestions, bulk replace, or copy-values-to to correct data. Validated values turn green. Click **Publish** to save a new version.
- **Version history**: click the clock icon at the bottom of any tab to browse previous versions and restore one if needed.

## Using the API

Data Contributors can use the **Import/curate data** (`studyCurator`, `integrationCurator`) endpoint groups in addition to the Consumer query endpoints. The Swagger interface is available from the dashboard under **API Documentation**.

**Typical workflow to create a study via API:**

1. Upload study metadata: `POST /api/v1/jobs/import/study` — provide a link to your TSV file and optionally a template accession. Note the returned job ID and the study accession (for example, `GSF1147033`).
2. Upload sample metadata: `POST /api/v1/jobs/import/samples` — provide the TSV link. Note the sample group accession (for example, `GSF1147034`).
3. Upload experimental data: `POST /api/v1/jobs/import/expression` — supports GCT and tabular formats. Note the data accession (for example, `GSF1147049`).
4. Link samples to study: `POST /api/v1/as-curator/integration/link/sample/group/{sourceId}/to/study/{targetId}`.
5. Link experimental data to samples: `POST /api/v1/as-curator/integration/link/expression/group/{sourceId}/to/sample/group/{targetId}`.

Track any import job with `GET /api/v1/jobs/{jobExecId}/output`.

For step-by-step API import instructions, see:

- [Import samples via API](../how-to/studies-import/import-samples-api.md)
- [Import omics data via API](../how-to/studies-import/import-omics-data-api.md)
- [Generate an API token](../how-to/users-access/generate-api-token.md)

> **For full API capabilities, see the API how-to guides.**

## Go deeper

- [Roles & Permissions](../reference/roles-permissions.md) — understand Contributor permissions vs. Consumer and Admin
- [Key Concepts](../explanation/data-model.md) — data model, linking rules, templates, and versioning
- [Cross-reference mapping](../how-to/studies-import/xref-mapping.md) — look up gene-to-transcript mappings linked to expression data
