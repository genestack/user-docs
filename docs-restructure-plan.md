# ODM User Guide — Diataxis Restructure Plan

## Target structure

```
docs/user-guide/
├── index.md
├── getting-started/
│   ├── index.md
│   ├── consumer.md
│   ├── contributor.md
│   └── admin.md
├── tutorials/
│   ├── index.md
│   ├── your-first-session.md
│   ├── curate-a-study.md
│   └── single-cell/
│       ├── index.md
│       ├── sc-workflow.md
│       ├── sc-rnaseq-demo.md
│       └── sc-transformations-demo.md
├── how-to/
│   ├── index.md
│   ├── users-access/
│   │   ├── manage-your-profile.md
│   │   ├── manage-users.md
│   │   ├── manage-groups.md
│   │   ├── generate-api-token.md
│   │   └── azure-authentication.md
│   ├── studies-import/
│   │   ├── create-a-study.md
│   │   ├── import-samples-gui.md
│   │   ├── import-samples-api.md
│   │   ├── import-omics-data-gui.md
│   │   ├── import-omics-data-api.md
│   │   ├── import-attached-files.md
│   │   ├── import-data-python.md
│   │   ├── xref-mapping.md
│   │   ├── gene-transcript-mapping.md
│   │   ├── transform-attachments.md
│   │   └── manage-versions.md
│   ├── metadata-templates/
│   │   ├── view-metadata.md
│   │   ├── edit-metadata.md
│   │   ├── bulk-replace-metadata.md
│   │   ├── validate-metadata.md
│   │   ├── create-template.md
│   │   └── export-template.md
│   ├── search-export/
│   │   ├── search-studies.md
│   │   ├── filter-facets.md
│   │   └── export-data.md
│   ├── sharing-permissions/
│   │   └── share-a-study.md
│   └── single-cell/
│       ├── import-single-cell-data.md
│       └── hdf5-transformations.md
├── reference/
│   ├── index.md
│   ├── roles-permissions.md
│   ├── data-formats/
│   │   ├── index.md
│   │   ├── tsv.md
│   │   ├── gct.md
│   │   ├── vcf.md
│   │   ├── hdf5.md
│   │   ├── facs.md
│   │   └── attached-files.md
│   ├── api/
│   │   └── processors-api.md
│   └── single-cell/
│       ├── transformation-config.md
│       ├── transformation-pipeline.md
│       ├── attribute-mapping.md
│       └── example-configs.md
└── explanation/
    ├── index.md
    ├── data-model.md
    ├── templates-and-validation.md
    ├── xref-mapping-concepts.md
    └── single-cell/
        └── hdf5-transformations.md
```

---

## Design decisions summary

- **Hybrid structure:** Diataxis is the primary axis. Role-based landing pages (Getting Started) act as entry points that link into the shared Diataxis content — no content is duplicated per role.
- **GUI vs API:** GUI how-tos are short and task-focused. API how-tos are the authoritative deep guides. GUI pages end with a callout linking to the API equivalent.
- **Single-cell:** First-class sub-section within every quadrant (tutorials, how-to, reference, explanation) — not merged into the flat structure.
- **Granularity:** Split files only when they cover multiple distinct user goals that a user might arrive at independently. Do not split for its own sake.
- **Notebooks:** Promoted to first-class tutorials, not supplementary downloads.
- **Gaps:** Not scoped in this plan. Each section that is missing content is marked `[PLACEHOLDER]`.

---

## Phase 0 — Directory setup

### Task 0.1 — Create new folder structure

Create the following empty directories (do not move or create files yet):

```
docs/user-guide/getting-started/
docs/user-guide/tutorials/
docs/user-guide/tutorials/single-cell/
docs/user-guide/how-to/
docs/user-guide/how-to/users-access/
docs/user-guide/how-to/studies-import/
docs/user-guide/how-to/metadata-templates/
docs/user-guide/how-to/search-export/
docs/user-guide/how-to/sharing-permissions/
docs/user-guide/how-to/single-cell/
docs/user-guide/reference/
docs/user-guide/reference/data-formats/
docs/user-guide/reference/api/
docs/user-guide/reference/single-cell/
docs/user-guide/explanation/
docs/user-guide/explanation/single-cell/
```

---

## Phase 1 — Getting Started (role landing pages)

Each role landing page replaces two existing quick-start files (GUI + API). The page is not a tutorial — it is a curated index with brief orientation text. Structure for each page:

1. One-paragraph description of what this role can do in ODM
2. **Where to start** — link to `tutorials/your-first-session.md`
3. **Common tasks** — bulleted links to the most relevant how-to guides for this role
4. **Using the interface** — links to GUI-specific how-tos
5. **Using the API** — links to API-specific how-tos, plus link to `how-to/users-access/generate-api-token.md`
6. **Go deeper** — links to relevant explanation and reference pages

---

### Task 1.1 — MERGE → `getting-started/consumer.md`

**Sources:**
- `quick-start/consumer-gui.md` — sections: Main Page, Browse Studies, Search for Data, Select a Study, Visualize Data, Export Data
- `quick-start/consumer-api.md` — sections: Access the API Endpoints, Using Swagger, API token, Use Case Example

**Destination:** `docs/user-guide/getting-started/consumer.md`

**Instructions:**
- Write a short intro: a Data Consumer can browse, search, filter, visualize, and export data. They cannot create or modify studies.
- Section "Using the interface": summarise the GUI quick-start (keep it to 5–8 bullet points linking to relevant how-to pages: search-studies.md, filter-facets.md, export-data.md). Do not reproduce full step-by-step instructions.
- Section "Using the API": summarise the API quick-start. Include the Swagger intro text and the use-case example walkthrough. Link to `how-to/users-access/generate-api-token.md`.
- Add a callout: "For full API capabilities, see the API how-to guides."
- Retire both source files after this task.

---

### Task 1.2 — MERGE → `getting-started/contributor.md`

**Sources:**
- `quick-start/contributor-gui.md`
- `quick-start/contributor-api.md`

**Destination:** `docs/user-guide/getting-started/contributor.md`

**Instructions:**
- Same structure as Task 1.1.
- Intro: A Data Contributor can create studies, import data, curate metadata, manage templates, share studies, and export data.
- "Using the interface": link to create-a-study.md, import-samples-gui.md, import-omics-data-gui.md, edit-metadata.md, create-template.md, share-a-study.md.
- "Using the API": cover the API quick-start content. Link to import-samples-api.md, import-omics-data-api.md, generate-api-token.md.
- Retire both source files after this task.

---

### Task 1.3 — MERGE → `getting-started/admin.md`

**Sources:**
- `quick-start/admin-gui.md`
- `quick-start/admin-api.md`

**Destination:** `docs/user-guide/getting-started/admin.md`

**Instructions:**
- Same structure as Task 1.1.
- Intro: An Administrator can manage users and groups, assign permissions, deactivate accounts, and delete data.
- "Using the interface": link to manage-users.md, manage-groups.md, manage-your-profile.md.
- "Using the API": cover the admin API quick-start content. Link to manage-users.md (API sections), manage-groups.md (API sections), generate-api-token.md.
- Retire both source files after this task.

---

### Task 1.4 — NEW → `getting-started/index.md`

**Destination:** `docs/user-guide/getting-started/index.md`

**Instructions:**
- Three-card layout (or simple list) linking to consumer.md, contributor.md, admin.md.
- One sentence per role describing who it is for.
- Note: "Not sure which role you have? See [Roles & Permissions](../reference/roles-permissions.md)."

---

## Phase 2 — Tutorials

Tutorials are learning-oriented. Each tutorial guides a user through a complete, meaningful task to teach them how the system works — not just how to click buttons. Each tutorial should have: goal, prerequisites, numbered steps, explanation of what happened, and a "What's next" section.

---

### Task 2.1 — EXTRACT+NEW → `tutorials/your-first-session.md`

**Source:** `doc-odm-user-guide/quickstart_user.md` — sections: Dashboard, Study Browser (first two sub-sections), Metadata Editor (overview paragraph)

**Destination:** `docs/user-guide/tutorials/your-first-session.md`

**Instructions:**
- This is a brand-new tutorial assembled from the orientation content in quickstart_user.md.
- Goal: "By the end of this tutorial you will have logged in, navigated the dashboard, found a study, and opened its metadata."
- Prerequisites: an ODM account (any role).
- Steps: (1) Log in and orient yourself on the dashboard, (2) Open the Study Browser and find a study, (3) Open the study and explore its metadata in the Metadata Editor.
- Pull the descriptive text and screenshots from quickstart_user.md — do not just copy the file; reframe it as a walkthrough with "you will see…", "notice that…" narration.
- "What's next": link to the role landing page for the user's role.
- After content is extracted, the source `quickstart_user.md` can be retired (its index-style intro becomes part of getting-started pages).

---

### Task 2.2 — PROMOTE → `tutorials/curate-a-study.md`

**Source:** `doc-odm-user-guide/curator_guide.md` (full file)

**Destination:** `docs/user-guide/tutorials/curate-a-study.md`

**Instructions:**
- Move the file as-is and reframe the title and intro to make it explicitly a tutorial: "In this tutorial you will take a newly imported study from raw to validated state."
- Add a Prerequisites section at the top: requires Contributor role, a study with imported samples, a template already assigned.
- Add a "What's next" section at the end linking to: validate-metadata.md, share-a-study.md, manage-versions.md.
- Intended audience: Contributor role.
- Retire source file after move.

---

### Task 2.3 — PROMOTE → `tutorials/single-cell/sc-workflow.md`

**Source:** `doc-odm-user-guide/quickstart-sc.md` (full file)

**Destination:** `docs/user-guide/tutorials/single-cell/sc-workflow.md`

**Instructions:**
- Move file as-is. Adjust title to "Tutorial: End-to-end single-cell workflow in ODM".
- Add Prerequisites section: Contributor role, an H5AD file ready to upload, API token generated.
- The 5-step structure (Upload → Transform → Index → Confirm → Query) is already good tutorial structure — preserve it.
- Add "What's next" section linking to: how-to/single-cell/hdf5-transformations.md, reference/single-cell/transformation-config.md, explanation/single-cell/hdf5-transformations.md.
- Retire source file after move.

---

### Task 2.4 — PROMOTE → `tutorials/single-cell/sc-rnaseq-demo.md`

**Source:** `doc-odm-user-guide/doc-odm-user-guide/notebooks/sc_rnaseq_demo.ipynb`

**Destination:** `docs/user-guide/tutorials/single-cell/sc-rnaseq-demo.md`

**Instructions:**
- Create a wrapper markdown page (not a conversion of the notebook).
- Structure: Goal → Prerequisites → What you'll learn → link/embed to download the notebook → section-by-section description of what each notebook section covers.
- Prerequisites: Python environment with ODM SDK or requests, API token, a public ODM instance or local install with SC data indexed.
- The notebook file stays at its current path; this page links to it.
- "What's next": link to sc-transformations-demo.md, reference/single-cell/transformation-config.md.

---

### Task 2.5 — PROMOTE → `tutorials/single-cell/sc-transformations-demo.md`

**Source:** `doc-odm-user-guide/doc-odm-user-guide/notebooks/sc_transformations_demo.ipynb`

**Destination:** `docs/user-guide/tutorials/single-cell/sc-transformations-demo.md`

**Instructions:**
- Same wrapper-page pattern as Task 2.4.
- Goal: demonstrate the full SC HDF5 transformation workflow via Python.
- Prerequisites: completed sc-workflow.md tutorial, API token, H5AD file.
- "What's next": link to reference/single-cell/transformation-config.md, reference/single-cell/example-configs.md.

---

### Task 2.6 — NEW → `tutorials/index.md`

**Destination:** `docs/user-guide/tutorials/index.md`

**Instructions:**
- List all tutorials with one-sentence descriptions and role tags (e.g., "All roles", "Contributor", "Contributor + API").
- Group: General (your-first-session, curate-a-study) and Single-cell (sc-workflow, sc-rnaseq-demo, sc-transformations-demo).

---

## Phase 3 — How-to: Users & Access

Source file for Tasks 3.1–3.4: `doc-odm-user-guide/setup.md`

The source file has these top-level sections (verified from headings):
- `## Accessing Your Profile and Permissions` (lines 3–19)
- `## Create/Deactivate users` (lines 20–30)
- `## Users and permissions` (lines 31–73) — includes Available Permissions, Setting and Managing User Permissions
- `## Groups` (lines 74–105) — includes Permission limitations
- `## Creating a Group` / `## Managing Groups` (lines 106–146)
- `## Curator Group` (lines 147–end)

All four destination files are Admin role content unless noted.

---

### Task 3.1 — SPLIT → `how-to/users-access/manage-your-profile.md`

**Source:** `doc-odm-user-guide/setup.md`, section `## Accessing Your Profile and Permissions`

**Destination:** `docs/user-guide/how-to/users-access/manage-your-profile.md`

**Instructions:**
- Extract only the "Accessing Your Profile and Permissions" section.
- Add a brief intro sentence: "This page describes how to view your own profile, check your assigned permissions, and update your display name or password."
- Role: any authenticated user.
- "See also": link to reference/roles-permissions.md for a description of what each permission means.

---

### Task 3.2 — SPLIT → `how-to/users-access/manage-users.md`

**Source:** `doc-odm-user-guide/setup.md`, sections `## Create/Deactivate users` and `## Users and permissions` (including sub-sections Available Permissions, Setting and Managing User Permissions)

**Destination:** `docs/user-guide/how-to/users-access/manage-users.md`

**Instructions:**
- Combine both sections into one how-to covering the full user lifecycle: create → assign permissions → deactivate.
- Role: Administrator.
- Add callout at top: "Need to understand what each permission grants? See [Roles & Permissions](../../reference/roles-permissions.md)."
- "See also": manage-groups.md.

---

### Task 3.3 — SPLIT → `how-to/users-access/manage-groups.md`

**Source:** `doc-odm-user-guide/setup.md`, sections `## Groups`, `## Creating a Group`, `## Managing Groups`, `## Curator Group`

**Destination:** `docs/user-guide/how-to/users-access/manage-groups.md`

**Instructions:**
- Combine all group-related sections into one how-to.
- Role: Administrator.
- "See also": manage-users.md, share-a-study.md (groups are used to share studies).

---

### Task 3.4 — MERGE → `how-to/users-access/generate-api-token.md`

**Sources:**
- `doc-odm-user-guide/getting-a-genestack-api-token.md` (full file — primary content)
- `key-concepts/key-concepts.md`, section `## API Token` (the "Importance of API Tokens" explanation paragraph)

**Destination:** `docs/user-guide/how-to/users-access/generate-api-token.md`

**Instructions:**
- Lead with the "why" paragraph from key-concepts.md (importance/security rationale) as a brief intro.
- Then include the full step-by-step token generation content from getting-a-genestack-api-token.md.
- Role: any authenticated user.
- "See also": azure-authentication.md.
- Retire both source files' content that was moved here.

---

### Task 3.5 — MOVE → `how-to/users-access/azure-authentication.md`

**Source:** `doc-odm-user-guide/getting-access-token-azure.md` (full file)

**Destination:** `docs/user-guide/how-to/users-access/azure-authentication.md`

**Instructions:**
- Move file as-is. Adjust title to "Authenticate with Azure AD".
- Add a note at the top: "This guide applies if your organisation uses Azure Active Directory. For standard token generation, see [Generate an API token](generate-api-token.md)."
- Retire source file.

---

## Phase 4 — How-to: Studies & Import

---

### Task 4.1 — MOVE → `how-to/studies-import/create-a-study.md`

**Source:** `doc-odm-user-guide/create-study.md` (full file)

**Destination:** `docs/user-guide/how-to/studies-import/create-a-study.md`

**Instructions:**
- Move as-is. Update title to "Create a study".
- Role: Contributor.
- Add callout: "This guide covers the GUI workflow. To create a study via API, see [Import samples (API)](import-samples-api.md) — study creation is the first step in that guide."
- Retire source file.

---

### Task 4.2 — SPLIT → `how-to/studies-import/import-samples-gui.md`

**Source:** `doc-odm-user-guide/import-data-in-odm.md`, sections:
- `## What Can Be Imported?`
- `## Importing Sample Information (Metadata)`
- `## Import Libraries and Preparations`

**Destination:** `docs/user-guide/how-to/studies-import/import-samples-gui.md`

**Instructions:**
- Extract the three sections listed above.
- Title: "Import samples and libraries (interface)".
- Role: Contributor.
- Add intro: "This guide covers importing sample metadata, libraries, and preparations via the ODM interface."
- Add callout at end: "For larger imports or automation, see [Import samples (API)](import-samples-api.md)."

---

### Task 4.3 — SPLIT → `how-to/studies-import/import-omics-data-gui.md`

**Source:** `doc-odm-user-guide/import-data-in-odm.md`, sections:
- `## Import experimental Data and attach files` → sub-section `### Import Experimental Data` and `### Linking Data`
- `## Important Considerations for Data Import`

**Destination:** `docs/user-guide/how-to/studies-import/import-omics-data-gui.md`

**Instructions:**
- Extract the experimental data and linking sections.
- Title: "Import omics data (interface)".
- Role: Contributor.
- Add callout at end: "For full import options including expression, variant, and FACS data via API, see [Import omics data (API)](import-omics-data-api.md)."
- Note: the "Attach a file" sub-section (`### Attach a file`) goes to Task 4.4, not here.

---

### Task 4.4 — SPLIT → `how-to/studies-import/import-attached-files.md`

**Source:** `doc-odm-user-guide/import-data-in-odm.md`, section `### Attach a file`

**Destination:** `docs/user-guide/how-to/studies-import/import-attached-files.md`

**Instructions:**
- Extract the "Attach a file" sub-section.
- Title: "Attach files to a study".
- Role: Contributor.
- Add intro: "Attached files are non-indexed uploads (PDFs, scripts, supplementary data) associated with a study."
- "See also": reference/data-formats/attached-files.md.
- After Tasks 4.2, 4.3, 4.4 are complete, retire `import-data-in-odm.md`.

---

### Task 4.5 — SPLIT → `how-to/studies-import/import-samples-api.md`

**Source:** `doc-odm-user-guide/import-data-using-api.md`, sections:
- `## What can I import?`
- `## Can I capture the relationships between studies, samples, and data?`
- `## Data Loading via APIs`
- `## Where can I import the data from?`
- `## Prerequisites`
- `## Core Data Import Workflow` (all sub-sections: Import Study, Import Samples, Import Libraries, Import Preparations, Import Cell metadata, Multipart form-data upload endpoints, Linking entities, Working with the jobExecId)

**Destination:** `docs/user-guide/how-to/studies-import/import-samples-api.md`

**Instructions:**
- Title: "Import samples and libraries (API)".
- Role: Contributor.
- This is the authoritative, deep guide for metadata import via API.
- Add callout at top: "For a simpler GUI workflow, see [Import samples (interface)](import-samples-gui.md)."
- Add "What's next" at end: link to import-omics-data-api.md for importing signal data.

---

### Task 4.6 — SPLIT → `how-to/studies-import/import-omics-data-api.md`

**Source:** `doc-odm-user-guide/import-data-using-api.md`, section `## Signal Data Import` (all sub-sections: Expression data, Variant data, Flow Cytometry Data, Attached Files, Check that you can query the relationships)

**Destination:** `docs/user-guide/how-to/studies-import/import-omics-data-api.md`

**Instructions:**
- Title: "Import omics data (API)".
- Role: Contributor.
- This section covers expression (GCT/TSV), variant (VCF), flow cytometry (FACS), and attached files import via API.
- Add intro: "Prerequisites: you must have already imported a study and samples. See [Import samples (API)](import-samples-api.md)."
- Add callout: "For a simpler GUI workflow for expression data, see [Import omics data (interface)](import-omics-data-gui.md)."
- After Tasks 4.5 and 4.6 are complete, retire `import-data-using-api.md`.

---

### Task 4.7 — MOVE → `how-to/studies-import/import-data-python.md`

**Source:** `doc-odm-user-guide/import-data-using-python-script.md` (full file)

**Destination:** `docs/user-guide/how-to/studies-import/import-data-python.md`

**Instructions:**
- Move as-is. Update title to "Import data using the Python script".
- Role: Contributor.
- Add a note at the top: "This guide covers the `import_ODM_data.py` helper script. For direct API calls, see [Import samples (API)](import-samples-api.md) and [Import omics data (API)](import-omics-data-api.md)."
- Retire source file.

---

### Task 4.8 — SPLIT (how-to part) → `how-to/studies-import/xref-mapping.md`

**Source:** `doc-odm-user-guide/xref-mapping.md`, all sections **except** `## What can I import?` (that section goes to Task 10.3):
- `## Importing a cross-reference mapping` (all sub-sections)
- `## Querying cross-reference mappings`
- `## Retrieving the mapping for a given gene in a study`
- `## Performing OMICS queries using gene/transcript IDs`
- `## Checking a mapping is available for a given expression data file`
- `## Checking which expression data files are linked to a given mapping file`
- `## Updating a mapping file`
- `## Removing a mapping file`
- `## Who can do what?`

**Destination:** `docs/user-guide/how-to/studies-import/xref-mapping.md`

**Instructions:**
- Title: "Manage cross-reference mappings".
- Role: Contributor (import/update/remove), Consumer (query).
- Add callout at top: "Not sure what cross-reference mappings are? See [Cross-reference mapping explained](../../explanation/xref-mapping-concepts.md)."
- Source file is retired after Task 4.8 and Task 10.3 are both complete.

---

### Task 4.9 — MOVE → `how-to/studies-import/gene-transcript-mapping.md`

**Source:** `doc-odm-user-guide/gene-transcript-mapping.md` (full file)

**Destination:** `docs/user-guide/how-to/studies-import/gene-transcript-mapping.md`

**Instructions:**
- Move as-is.
- Add a note: "Related: for general cross-reference mapping (including non-gene mappings), see [Manage cross-reference mappings](xref-mapping.md)."
- Retire source file.

---

### Task 4.10 — MOVE → `how-to/studies-import/transform-attachments.md`

**Source:** `doc-odm-user-guide/attachment-transformation.md` (full file)

**Destination:** `docs/user-guide/how-to/studies-import/transform-attachments.md`

**Instructions:**
- Move as-is. Update title to "Transform attached files (CSV to TSV)".
- Retire source file.

---

### Task 4.11 — MOVE → `how-to/studies-import/manage-versions.md`

**Source:** `doc-odm-user-guide/versioning.md` (full file)

**Destination:** `docs/user-guide/how-to/studies-import/manage-versions.md`

**Instructions:**
- Move as-is. Update title to "Manage study versions".
- Retire source file.

---

## Phase 5 — How-to: Metadata & Templates

Source file for Tasks 5.1–5.4: `doc-odm-user-guide/metadata-editor.md`

Verified headings in source file:
- `## Getting to the Metadata Editor`
- `## Exploring the Metadata Editor` (sub-sections: Study tab, Study Ownership Transfer via GUI, Samples tab, Data tab)
- `## Metadata validation and curation`

---

### Task 5.1 — SPLIT → `how-to/metadata-templates/view-metadata.md`

**Source:** `doc-odm-user-guide/metadata-editor.md`, sections:
- `## Getting to the Metadata Editor`
- `## Exploring the Metadata Editor` (read-only / navigation content only — how to open tabs, what each tab shows)

**Destination:** `docs/user-guide/how-to/metadata-templates/view-metadata.md`

**Instructions:**
- Title: "View study metadata".
- Role: any authenticated user (Consumer can view, Contributor can also edit).
- Extract only the navigation and display content from "Exploring the Metadata Editor". If the section mixes view and edit instructions, keep only the view/navigation parts here and move edit instructions to Task 5.2.
- "See also": edit-metadata.md.

---

### Task 5.2 — SPLIT → `how-to/metadata-templates/edit-metadata.md`

**Source:** `doc-odm-user-guide/metadata-editor.md`, within `## Exploring the Metadata Editor`:
- `### Study tab` — editing study-level metadata fields
- `#### Study Ownership Transfer via GUI`
- `### Samples tab` — editing sample metadata (excluding bulk replace, which goes to Task 5.3)
- `### Data tab` — editing data-level metadata

**Destination:** `docs/user-guide/how-to/metadata-templates/edit-metadata.md`

**Instructions:**
- Title: "Edit study metadata".
- Role: Contributor.
- Add intro: "You must switch the Metadata Editor to Edit mode before making changes."
- Add callout: "To replace a value across many rows at once, see [Bulk replace metadata values](bulk-replace-metadata.md)."
- "See also": validate-metadata.md, manage-versions.md.

---

### Task 5.3 — SPLIT → `how-to/metadata-templates/bulk-replace-metadata.md`

**Source:** `doc-odm-user-guide/metadata-editor.md` — locate the bulk replace / find-and-replace feature content within the Samples tab or Data tab section.

**Destination:** `docs/user-guide/how-to/metadata-templates/bulk-replace-metadata.md`

**Instructions:**
- Title: "Bulk replace metadata values".
- Role: Contributor.
- If the source file does not have a dedicated section for bulk replace (it may be described inline within the Samples tab section), extract and reformat that content as a standalone how-to.
- Add intro: "Use bulk replace to update the same metadata field across many samples or data rows at once."

---

### Task 5.4 — SPLIT → `how-to/metadata-templates/validate-metadata.md`

**Source:** `doc-odm-user-guide/metadata-editor.md`, section `## Metadata validation and curation`

**Destination:** `docs/user-guide/how-to/metadata-templates/validate-metadata.md`

**Instructions:**
- Title: "Validate metadata".
- Role: Contributor.
- Add callout: "To understand what validation checks and why it matters, see [Templates and validation explained](../../explanation/templates-and-validation.md)."
- After Tasks 5.1–5.4 are complete, retire `metadata-editor.md`.

---

### Task 5.5 — SPLIT → `how-to/metadata-templates/create-template.md`

**Source:** `doc-odm-user-guide/template-editor.md`, sections:
- `## Accessing the Template Editor`
- `## What is a template?` — keep the brief definition; the deeper explanation goes to Task 10.2
- `## Create and edit template`
- `## Grouping/compounding metadata fields`
- `## Change template`
- `## Template validity checks`

**Destination:** `docs/user-guide/how-to/metadata-templates/create-template.md`

**Instructions:**
- Title: "Create and customise a template".
- Role: Contributor.
- Keep "What is a template?" as a one-paragraph intro, then add: "For a deeper explanation of how templates work and when to create vs. reuse, see [Templates and validation explained](../../explanation/templates-and-validation.md)."
- Add callout: "For the GUI workflow, this guide covers all steps. The template API is not yet documented — [PLACEHOLDER]."

---

### Task 5.6 — SPLIT → `how-to/metadata-templates/export-template.md`

**Source:** `doc-odm-user-guide/template-editor.md`, section `## Export template`

**Destination:** `docs/user-guide/how-to/metadata-templates/export-template.md`

**Instructions:**
- Title: "Export a template".
- Role: Contributor.
- This is a short, standalone how-to — the section in the source is brief and self-contained.
- After Tasks 5.5 and 5.6 are complete, retire `template-editor.md`.

---

## Phase 6 — How-to: Search & Export

Source file for Tasks 6.1–6.2: `doc-odm-user-guide/studybrowser.md`

Verified headings:
- `## Getting to the Study Browser`
- `## Search for Data`
- `## Filter Data` → `### Metadata validity status`
- `## Bookmark studies`
- `## Configuring the filter panel`
- `## Navigation and Help`

---

### Task 6.1 — SPLIT → `how-to/search-export/search-studies.md`

**Source:** `doc-odm-user-guide/studybrowser.md`, sections:
- `## Getting to the Study Browser`
- `## Search for Data`
- `## Bookmark studies`
- `## Navigation and Help`

**Destination:** `docs/user-guide/how-to/search-export/search-studies.md`

**Instructions:**
- Title: "Search for studies and data".
- Role: any authenticated user (primarily Consumer).
- "See also": filter-facets.md, export-data.md.

---

### Task 6.2 — SPLIT → `how-to/search-export/filter-facets.md`

**Source:** `doc-odm-user-guide/studybrowser.md`, sections:
- `## Filter Data` (including the `### Metadata validity status` sub-section)
- `## Configuring the filter panel`

**Destination:** `docs/user-guide/how-to/search-export/filter-facets.md`

**Instructions:**
- Title: "Filter and facet search results".
- Role: any authenticated user.
- After Tasks 6.1 and 6.2 are complete, retire `studybrowser.md`.

---

### Task 6.3 — MOVE → `how-to/search-export/export-data.md`

**Source:** `doc-odm-user-guide/exporting-data.md` (full file)

**Destination:** `docs/user-guide/how-to/search-export/export-data.md`

**Instructions:**
- Move as-is. Update title to "Export data from a study".
- Retire source file.

---

## Phase 7 — How-to: Sharing & Permissions

### Task 7.1 — MOVE → `how-to/sharing-permissions/share-a-study.md`

**Source:** `doc-odm-user-guide/sharing.md` (full file)

**Destination:** `docs/user-guide/how-to/sharing-permissions/share-a-study.md`

**Instructions:**
- Move as-is. Update title to "Share a study with a group".
- Add "See also": manage-groups.md (groups must exist before they can be assigned), reference/roles-permissions.md.
- Retire source file.

---

## Phase 8 — How-to: Single-cell

### Task 8.1 — MOVE → `how-to/single-cell/import-single-cell-data.md`

**Source:** `doc-odm-user-guide/single-cell.md` (full file)

**Destination:** `docs/user-guide/how-to/single-cell/import-single-cell-data.md`

**Instructions:**
- Move as-is. Update title to "Import single-cell data".
- Add callout: "For a full end-to-end tutorial including transformation and querying, see [Tutorial: End-to-end single-cell workflow](../../tutorials/single-cell/sc-workflow.md)."
- Add callout: "For HDF5 transformation options, see [HDF5 transformation how-tos](hdf5-transformations.md)."
- Retire source file.

---

### Task 8.2 — MOVE → `how-to/single-cell/hdf5-transformations.md`

**Source:** `doc-odm-user-guide/how-to-sc-hdf5-transformations.md` (full file)

**Destination:** `docs/user-guide/how-to/single-cell/hdf5-transformations.md`

**Instructions:**
- Move as-is.
- Add callout at top: "For background on what HDF5 transformations are and why they're needed, see [About HDF5 transformations](../../explanation/single-cell/hdf5-transformations.md)."
- Add "See also": reference/single-cell/transformation-config.md.
- Retire source file.

---

## Phase 9 — Reference

---

### Task 9.1 — MOVE → `reference/roles-permissions.md`

**Source:** `users-roles-permissions/users-roles-permissions.md` (full file)

**Destination:** `docs/user-guide/reference/roles-permissions.md`

**Instructions:**
- Move as-is.
- Retire source file and folder.

---

### Tasks 9.2–9.7 — SPLIT+MERGE → `reference/data-formats/*.md`

**Sources (both files must be read for each format):**
- `supported-data/supported-data.md` — user-facing descriptions of each format, ODM capabilities per format
- `doc-odm-user-guide/supported-formats.md` — technical file format specifications (columns, structure, example files)

These two files cover the same formats from different angles. Merge them per format into one authoritative reference page. The "Searching for Imported Data via API" and "Attached Files Endpoints" sections from `supported-formats.md` go to Task 9.7.

Structure for each format reference page:
1. What this format is
2. Supported variants (e.g., GCT 1.2 vs 1.3)
3. File structure and required columns
4. How ODM uses this format (indexed fields, searchable attributes)
5. Limitations

---

#### Task 9.2 — TSV → `reference/data-formats/tsv.md`

**Source sections:**
- `supported-data.md`: `## TSV (Tabular data)` (Simple Data Frame, Complex Data Frame)
- `supported-formats.md`: `## Samples metadata file`, `## Libraries file`, `## Preparations file`, `## Tabular data`

---

#### Task 9.3 — GCT → `reference/data-formats/gct.md`

**Source sections:**
- `supported-data.md`: `## GCT (Gene Expression)`
- `supported-formats.md`: `## Expression data in GCT (transcriptomics)`

---

#### Task 9.4 — VCF → `reference/data-formats/vcf.md`

**Source sections:**
- `supported-data.md`: `## VCF (Variants)`
- `supported-formats.md`: `## Variant data (genomics)` (including full structure description)

---

#### Task 9.5 — HDF5 → `reference/data-formats/hdf5.md`

**Source sections:**
- `supported-data.md`: `## HDF5 (e.g. Single Cell)`
- `supported-formats.md`: no dedicated HDF5 section (check file — if none exists, note `[PLACEHOLDER]`)

---

#### Task 9.6 — FACS → `reference/data-formats/facs.md`

**Source sections:**
- `supported-data.md`: `## FACS (Flow Cytometry)`
- `supported-formats.md`: no dedicated FACS section (check — note `[PLACEHOLDER]` if missing)

---

#### Task 9.7 — Attached Files → `reference/data-formats/attached-files.md`

**Source sections:**
- `supported-data.md`: `## Attached Files`
- `supported-formats.md`: `## Attached Files Endpoints` section (from "Searching for Imported Data via API")

Note: the `## Study metadata file` section from `supported-formats.md` does not map to a specific data format reference page — add it to `reference/data-formats/tsv.md` or create a brief `reference/data-formats/study-metadata.md` if the content is substantial.

After Tasks 9.2–9.7 are complete, retire both `supported-data/supported-data.md` and `doc-odm-user-guide/supported-formats.md`.

---

### Task 9.8 — MOVE → `reference/api/processors-api.md`

**Source:** `doc-odm-user-guide/api-reference.md` (full file)

**Destination:** `docs/user-guide/reference/api/processors-api.md`

**Instructions:**
- Move as-is.
- Retire source file.

---

### Task 9.9 — MOVE → `reference/single-cell/transformation-config.md`

**Source:** `doc-odm-user-guide/configuration-reference.md` (full file)

**Destination:** `docs/user-guide/reference/single-cell/transformation-config.md`

**Instructions:**
- Move as-is.
- Retire source file.

---

### Task 9.10 — MOVE → `reference/single-cell/transformation-pipeline.md`

**Source:** `doc-odm-user-guide/transformation-process-reference.md` (full file)

**Destination:** `docs/user-guide/reference/single-cell/transformation-pipeline.md`

**Instructions:**
- Move as-is.
- Retire source file.

---

### Task 9.11 — MOVE → `reference/single-cell/attribute-mapping.md`

**Source:** `doc-odm-user-guide/attribute-mapping.md` (full file)

**Destination:** `docs/user-guide/reference/single-cell/attribute-mapping.md`

**Instructions:**
- Move as-is.
- Retire source file.

---

### Task 9.12 — NEW → `reference/single-cell/example-configs.md`

**Source assets:** `doc-odm-user-guide/doc-odm-user-guide/extras/`:
- `aggregated_config_1.json`, `aggregated_config_2.json`, `aggregated_config_3.json`
- `GSE156793.json`, `GSE165045.json`
- `public-dataset-configurations-mapping.md` (existing doc)
- `dataset-import-commands.md` (existing doc)

**Destination:** `docs/user-guide/reference/single-cell/example-configs.md`

**Instructions:**
- Create a reference page that surfaces these configs as named, annotated examples.
- Structure: for each config file, one sub-section with: what dataset it represents, link to download, brief description of what the config demonstrates.
- Incorporate the content from `public-dataset-configurations-mapping.md` and `dataset-import-commands.md` as sections.
- The JSON files stay at their current paths; this page links to them.

---

## Phase 10 — Explanation

---

### Task 10.1 — SPLIT → `explanation/data-model.md`

**Source:** `key-concepts/key-concepts.md`, sections:
- `## How data is organized in ODM` (full section including the Study → Sample → Library → Data hierarchy)
- `## Objects vs. Groups` (both sub-sections)

**Destination:** `docs/user-guide/explanation/data-model.md`

**Instructions:**
- Title: "How data is organised in ODM".
- This is explanation, not a how-to — write in a "here's why it works this way" register, not step-by-step instructions.
- Add "See also": reference/data-formats/ (for format-specific details), how-to/studies-import/create-a-study.md.

---

### Task 10.2 — SPLIT → `explanation/templates-and-validation.md`

**Source:** `key-concepts/key-concepts.md`, sections:
- `## Templates`
- `## Validation` (including `### Importance of Validation`)
- Also incorporate the "What is a template?" content from `template-editor.md` (extracted in Task 5.5) if it contains conceptual depth beyond the one-line definition kept there.

**Destination:** `docs/user-guide/explanation/templates-and-validation.md`

**Instructions:**
- Title: "Templates and validation in ODM".
- Explain: what a template is, why templates exist (harmonisation, data quality), what validation enforces, what happens when data fails validation, and when to create a new template vs. reuse an existing one.
- After Tasks 10.1 and 10.2 are complete, retire `key-concepts/key-concepts.md`.

---

### Task 10.3 — SPLIT → `explanation/xref-mapping-concepts.md`

**Source:** `doc-odm-user-guide/xref-mapping.md`, section `## What can I import?` only.

**Destination:** `docs/user-guide/explanation/xref-mapping-concepts.md`

**Instructions:**
- Title: "Cross-reference mapping explained".
- Expand beyond just the "What can I import?" section: explain what a cross-reference mapping is conceptually, why it is needed (transcript→gene resolution), and when a user would need one.
- This page can be brief (200–400 words) if the source section is thin — add `[PLACEHOLDER: expand with examples of when xref mapping is needed]` if so.
- "See also": how-to/studies-import/xref-mapping.md for the procedural steps.

---

### Task 10.4 — MOVE → `explanation/single-cell/hdf5-transformations.md`

**Source:** `doc-odm-user-guide/about-sc-hdf5-transformations.md` (full file)

**Destination:** `docs/user-guide/explanation/single-cell/hdf5-transformations.md`

**Instructions:**
- Move as-is.
- Add "See also": how-to/single-cell/hdf5-transformations.md, reference/single-cell/transformation-config.md, tutorials/single-cell/sc-workflow.md.
- Retire source file.

---

## Phase 11 — Index pages and cleanup

### Task 11.1 — UPDATE → `index.md`

**Source:** `docs/user-guide/index.md` (existing)

**Instructions:**
- Keep as the top-level landing page.
- Replace the current role-based article list with three prominent links: Consumer → `getting-started/consumer.md`, Contributor → `getting-started/contributor.md`, Administrator → `getting-started/admin.md`.
- Add a secondary section: "Browse by type" with links to tutorials/index.md, how-to/index.md, reference/index.md, explanation/index.md.
- Remove all inline article lists (they now live on the section index pages).

---

### Task 11.2 — NEW → Section index pages

Create `index.md` for each of the following new sections. Each index should list all pages in the section with one-sentence descriptions.

- `how-to/index.md` — grouped by sub-section (users-access, studies-import, metadata-templates, search-export, sharing-permissions, single-cell)
- `reference/index.md` — grouped by sub-section (roles-permissions, data-formats, api, single-cell)
- `explanation/index.md` — flat list (data-model, templates-and-validation, xref-mapping-concepts, single-cell/hdf5-transformations)

---

### Task 11.3 — UPDATE internal links

After all moves are complete, do a global find-and-replace pass to update internal links in all files.

**Key redirects:**
| Old path | New path |
|---|---|
| `doc-odm-user-guide/setup.md` | split — link to specific sub-page |
| `doc-odm-user-guide/import-data-in-odm.md` | split — link to specific sub-page |
| `doc-odm-user-guide/import-data-using-api.md` | split — link to specific sub-page |
| `doc-odm-user-guide/metadata-editor.md` | split — link to specific sub-page |
| `doc-odm-user-guide/studybrowser.md` | split — link to specific sub-page |
| `doc-odm-user-guide/xref-mapping.md` | split — `how-to/studies-import/xref-mapping.md` or `explanation/xref-mapping-concepts.md` |
| `key-concepts/key-concepts.md` | split — `explanation/data-model.md` or `explanation/templates-and-validation.md` |
| `supported-data/supported-data.md` | split — `reference/data-formats/<format>.md` |
| `quick-start/consumer-gui.md` | `getting-started/consumer.md` |
| `quick-start/contributor-gui.md` | `getting-started/contributor.md` |
| `quick-start/admin-gui.md` | `getting-started/admin.md` |

---

### Task 11.4 — UPDATE MkDocs nav

Update `mkdocs.yml` (or equivalent nav config) to reflect the new structure. The nav should mirror the folder structure defined in Phase 0.

---

## Retirement checklist

Files to delete once all tasks referencing them are complete:

- `quick-start/consumer-gui.md` (after Task 1.1)
- `quick-start/consumer-api.md` (after Task 1.1)
- `quick-start/contributor-gui.md` (after Task 1.2)
- `quick-start/contributor-api.md` (after Task 1.2)
- `quick-start/admin-gui.md` (after Task 1.3)
- `quick-start/admin-api.md` (after Task 1.3)
- `quick-start/index.md` (after Tasks 1.1–1.3)
- `doc-odm-user-guide/quickstart_user.md` (after Task 2.1)
- `doc-odm-user-guide/curator_guide.md` (after Task 2.2)
- `doc-odm-user-guide/quickstart-sc.md` (after Task 2.3)
- `doc-odm-user-guide/getting-a-genestack-api-token.md` (after Task 3.4)
- `doc-odm-user-guide/getting-access-token-azure.md` (after Task 3.5)
- `doc-odm-user-guide/setup.md` (after Tasks 3.1–3.4)
- `doc-odm-user-guide/create-study.md` (after Task 4.1)
- `doc-odm-user-guide/import-data-in-odm.md` (after Tasks 4.2–4.4)
- `doc-odm-user-guide/import-data-using-api.md` (after Tasks 4.5–4.6)
- `doc-odm-user-guide/import-data-using-python-script.md` (after Task 4.7)
- `doc-odm-user-guide/xref-mapping.md` (after Tasks 4.8 + 10.3)
- `doc-odm-user-guide/gene-transcript-mapping.md` (after Task 4.9)
- `doc-odm-user-guide/attachment-transformation.md` (after Task 4.10)
- `doc-odm-user-guide/versioning.md` (after Task 4.11)
- `doc-odm-user-guide/metadata-editor.md` (after Tasks 5.1–5.4)
- `doc-odm-user-guide/template-editor.md` (after Tasks 5.5–5.6)
- `doc-odm-user-guide/studybrowser.md` (after Tasks 6.1–6.2)
- `doc-odm-user-guide/exporting-data.md` (after Task 6.3)
- `doc-odm-user-guide/sharing.md` (after Task 7.1)
- `doc-odm-user-guide/single-cell.md` (after Task 8.1)
- `doc-odm-user-guide/how-to-sc-hdf5-transformations.md` (after Task 8.2)
- `users-roles-permissions/users-roles-permissions.md` (after Task 9.1)
- `supported-data/supported-data.md` (after Tasks 9.2–9.7)
- `doc-odm-user-guide/supported-formats.md` (after Tasks 9.2–9.7)
- `doc-odm-user-guide/api-reference.md` (after Task 9.8)
- `doc-odm-user-guide/configuration-reference.md` (after Task 9.9)
- `doc-odm-user-guide/transformation-process-reference.md` (after Task 9.10)
- `doc-odm-user-guide/attribute-mapping.md` (after Task 9.11)
- `doc-odm-user-guide/about-sc-hdf5-transformations.md` (after Task 10.4)
- `key-concepts/key-concepts.md` (after Tasks 10.1–10.2)
- `doc-odm-user-guide/doc-odm-user-guide/extras/public-dataset-configurations-mapping.md` (after Task 9.12)
- `doc-odm-user-guide/doc-odm-user-guide/extras/dataset-import-commands.md` (after Task 9.12)
