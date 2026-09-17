---
diataxis: how-to
tab: odm-api
---

# How to link entities after import

When you import data into ODM, each entity arrives as an independent object. A study, a group of samples, an expression matrix: at import time none of them know about the others. Linking is the step that assembles those separate objects into a single, navigable study, following the structure of the ODM data model. This guide walks you through it in the order the model requires, from samples all the way up to omics data.

The endpoints follow predictable patterns, which this guide lays out relationship by relationship. For the full specification of any one of them, the [Swagger UI](/swagger/helper/) is the source of truth.

## Prerequisites

All entities you intend to link must already be imported, and you need their `groupAccession` values from each import job's output. See [About the import workflow](about-the-import-workflow.md) for the entity import sequence.

## Link in the right order

Linking follows the ODM data model hierarchy, and the order matters: each link attaches a child to a parent that must already be in place. Work down this list, and every entity lands with something to hold onto:

1. Samples to the study
2. Libraries to samples
3. Preparations to samples
4. Cell metadata to samples, libraries, or preparations
5. Omics data (expression, variant, flow cytometry) to samples, libraries, preparations, or cell metadata
6. Attached files to the study (this one happens automatically at import; there is no separate link call)

The rest of this guide follows that order.

## Start with samples and the study

The first link is the foundation: it attaches your sample group to the study that will hold it. Send:

```bash
curl -X 'POST' \
  'https://<HOST>/api/v1/as-curator/integration/link/sample/group/GSF1283530/to/study/GSF1283528' \
  -H 'accept: */*' \
  -H 'Genestack-API-Token: <TOKEN>' \
  -d ''
```

You will see it take effect right away: in the Study Browser, the sample count next to the study changes from `-` to the number of linked samples.

## Attach libraries and preparations to samples

With samples in place, connect any libraries and preparations to them. Both link to the sample group and follow the same shape:

- Libraries to samples: `POST /api/v1/as-curator/integration/link/library/group/{sourceId}/to/sample/group/{targetId}`
- Preparations to samples: `POST /api/v1/as-curator/integration/link/preparation/group/{sourceId}/to/sample/group/{targetId}`

## Bring in cell metadata

Cell metadata can attach to samples, libraries, or preparations, depending on where it belongs in your study:

- To samples: `POST /api/v1/as-curator/integration/link/cell/group/{sourceId}/to/sample/group/{targetId}`
- To libraries: `POST /api/v1/as-curator/integration/link/cells/group/{sourceId}/to/library/group/{targetId}`
- To preparations: `POST /api/v1/as-curator/integration/link/cells/group/{sourceId}/to/preparation/group/{targetId}`

Cell metadata links by matching values, not by accession alone: the link succeeds when the `batch` values in the cell metadata match the `Sample Source ID` (for samples), `Library ID` (for libraries), or `Preparation ID` (for preparations) in the target group. The response reports how many links it created.

If a link comes back empty, one of two things is usually the cause:

- the target metadata group has no Sample Source ID, Library ID, or Preparation ID, or
- none of the `batch` values in the cell metadata match the IDs in the target group.

## Link your omics data

Omics data is the last layer: it attaches to the entities it measures.

Expression data is the most flexible, linking to samples, libraries, preparations, or cell metadata:

- To a sample group: `POST /api/v1/as-curator/integration/link/expression/group/{sourceId}/to/sample/group/{targetId}`
- To a library group: `POST /api/v1/as-curator/integration/link/expression/group/{sourceId}/to/library/group/{targetId}`
- To a preparation group: `POST /api/v1/as-curator/integration/link/expression/group/{sourceId}/to/preparation/group/{targetId}`
- To a cell metadata group: `POST /api/v1/as-curator/integration/link/expression/group/{sourceId}/to/cell/group/{targetId}`

When you link expression data to libraries, the default linking attribute is `Library ID`; for preparations, it is `Preparation ID`. Note that a Cell Expression Group can be linked to only one Cell Metadata Group.

Variant and flow cytometry data each link to their sample group:

- Variant to samples: `POST /api/v1/as-curator/integration/link/variant/group/{sourceId}/to/sample/group/{targetId}`
- Flow cytometry to samples: `POST /api/v1/as-curator/integration/link/flow-cytometry/group/{sourceId}/to/sample/group/{targetId}`

## Group-to-group or object-to-object?

Most of the endpoints above link one whole group to another. **Group-to-group linking** connects every object in the source group to every object in the target group, and it is the approach you will reach for most of the time.

When you need finer control, **object-to-object linking** connects one specific data object to one specific target:

`POST /api/v1/as-curator/integration/link/{sourceType}/{sourceId}/to/{targetType}/{targetId}`

## Choose your linking key

By default, sample-to-data relationships link on `Sample Source ID`. To match on a different template attribute instead, pass it through the `linkingAttribute` query parameter.

The defaults vary by target: libraries link on `Library ID`, preparations on `Preparation ID`, and cell metadata on the `batch` column.
