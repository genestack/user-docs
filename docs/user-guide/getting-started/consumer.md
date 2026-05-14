# Getting Started: Data Consumer

A Data Consumer can browse, search, filter, visualize, and export data in the Open Data Manager. This role is the default for all users — you do not need to create or modify studies to get value from ODM. As a Consumer, your access is read-only: you can explore study metadata, view sample attributes, and download datasets, but you cannot import or edit data.

## Where to start

Work through [Your First Session](../tutorials/your-first-session.md) to get hands-on with browsing and searching studies.

## Common tasks

- [Search for studies](../how-to/search-export/search-studies.md) — find studies by keyword, organism, data class, or other criteria
- [Filter with facets](../how-to/search-export/filter-facets.md) — narrow results using the left-hand filter panel
- [Export data](../how-to/search-export/export-data.md) — download study data and metadata as a compressed archive

## Using the interface

The ODM dashboard gives you a starting point for all consumer activities:

- Open the dashboard and click **Browse studies** to see the full list of available studies.
- Use the left-hand filter panel to narrow results by attributes such as Organism, Data Class, Study Type, and more. Available filters depend on your ODM configuration.
- Type keywords (for example, *bowel*) into the search bar; the autocomplete feature also suggests ontology terms.
- Click a study card to open it. Each study has three tabs: **Study** (metadata), **Samples** (sample attributes), and **Data** (linked and attached files).
- Note the study's accession number (format: `GSF…`) — you will need it when accessing the same study via the API.
- Open the **Explore** tab inside a study to generate plots for one or two sample attributes.
- Click **Export** (top right of a study) to download all study data as a compressed archive. Note that studies with externally stored files that are no longer accessible cannot be exported.

## Using the API

The ODM REST API lets you retrieve study and sample metadata programmatically. The built-in Swagger interface is the easiest way to explore endpoints without writing code.

**Accessing Swagger:**

1. From the dashboard, click **API Documentation** to open the Swagger interface.
2. Endpoints are grouped by use case. As a Consumer, the relevant group is **Query/retrieve data** (`studyUser` definition). The **Import/curate data** and **Manage organisation** groups require Curator or Admin permissions.
3. Select an endpoint (for example, `GET /api/v1/as-user/studies`) and click **Try it out** to activate it.
4. Authorize your session by clicking **Authorize** and supplying your API token (Access Token or Genestack API token).

**Example: retrieve study metadata**

1. In Swagger, select the **studyUser** definition.
2. Open the endpoint **List or search for study metadata objects** (`GET /api/v1/as-user/studies`).
3. Click **Try it out**, then paste a study accession number (for example, `GSF1102568`) into the `query` field and click **Execute**.
4. The response is a JSON object containing the study's metadata. You can download it directly from the Swagger response panel.

To generate an API token, see [Generate an API token](../how-to/users-access/generate-api-token.md).

> **For full API capabilities, see the API how-to guides.**

## Go deeper

- [Roles & Permissions](../reference/roles-permissions.md) — understand what Consumers can and cannot do
- [Key Concepts](../explanation/data-model.md) — data model, accession numbers, and ontologies explained
