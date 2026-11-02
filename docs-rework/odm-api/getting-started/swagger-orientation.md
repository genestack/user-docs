---
diataxis: reference
tab: odm-api
---

# Swagger orientation

The ODM Swagger UI provides browsable, interactive documentation for all ODM API endpoints, reached from the ODM Dashboard via **API Documentation**. It lets you explore endpoints, understand parameters and response schemas, and execute test requests directly from your browser. Swagger is primarily useful for exploration and one-off requests; for day-to-day integrations and automation, use the ODM SDK or Python/R API clients (see [API Libraries](../../api-libraries/index.md)).

This page describes how the Swagger UI is organised. To walk through executing your first request, see [Make your first request in Swagger](make-your-first-request.md).

## Swagger UI layout

The main view shows endpoint groups. At the top right, a definition selector lets you switch between different API surfaces: for example, `studyUser` for read-only study endpoints versus `studyCurator` for endpoints that also support modification.

Each endpoint entry shows the HTTP method, path, a summary description, and when expanded: parameters, request body requirements, example responses, and a **Try it out** button.

## Endpoint groups

Endpoints are organised into four access tiers:

**Query/retrieve data**, User endpoints. Available to all users, including those not in the Curator group as well as Curator group members.

**Import/curate data**, Curator endpoints. Available only to members of the Curator group.

**Data sources**, Mixed access. Some endpoints are curator-only; others are accessible to all users.

**Manage organisation**, Restricted to users with the "Organisation Administrator" role.

Some operations are gated by a platform role or by study ownership rather than by their tier. In `manageData`, each operation has its own requirement: see [Delete data](../admin/delete-data.md), [Find detached objects](../admin/find-detached-objects.md), and [Recover study ownership](../admin/recover-study-ownership.md). In `processorsController`, creating, updating, and archiving configurations requires the "Transformation Configuration Administrator" role. For all platform roles, see [Roles](../../overview/access-control/roles.md).

## Available definitions

Use the top-right definition selector to navigate between API surfaces. Most definitions come in a `…User` / `…Curator` pair: the `User` surface is read-only, while the `Curator` surface also supports modification and requires Curator group membership. The full set of definitions is:

- `studyUser` / `studyCurator`, study metadata
- `sampleUser` / `sampleCurator`, sample metadata
- `libraryUser` / `libraryCurator`, library metadata
- `preparationUser` / `preparationCurator`, preparation metadata
- `cellUser` / `cellCurator`, cell metadata
- `expressionUser` / `expressionCurator`, expression data
- `variantUser` / `variantCurator`, variant data
- `flowCytometryUser` / `flowCytometryCurator`, flow cytometry data
- `fileUser` / `fileCurator`, attached files
- `integrationUser` / `integrationCurator`, cross-entity queries and linking
- `manageData`, data deletion, detached objects, and ownership recovery (each operation has its own ownership or role requirement)
- `referenceGenome`, reference genome upload and query
- `xrefsets`, cross-reference mapping sets built from reference data (for example, Ensembl and NCBI)
- `processorsController`, transformations: configurations, images, and jobs (see [About the Processors Controller](../contribute/transformations/about-processors-controller.md))
- `job`, asynchronous job status
- `tasks`, background task status
- `audit`, retrieval of audit event records
- `scimUsers`, SCIM 2.0 user provisioning (Organisation Administrator)
- `scimGroups`, SCIM 2.0 group provisioning (Organisation Administrator)
