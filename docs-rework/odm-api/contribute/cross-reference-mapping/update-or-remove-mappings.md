---
diataxis: how-to
tab: odm-api
---

# How to update or remove a mapping

Cross-reference mappings are shared across your organisation and outlive the individual studies and expression files they connect to. Because of that, ODM never cleans them up on your behalf: removing a mapping, along with the links that point to it, is always a deliberate step. This guide walks you through replacing a mapping and deleting one cleanly.

For the full specification of any endpoint below, the [Swagger UI](/swagger/helper/) is the source of truth.

## Prerequisites

- An API token. See [Authentication and tokens](../../getting-started/authentication-and-tokens.md).
- To delete a mapping: you must be the original uploader of the file.
- To delete links: Curator group membership is required.

## Updating a mapping

There is no way to edit a mapping file in place. When a mapping needs to change, the pattern is to delete the existing file and import a fresh one in its place. The [Import a mapping](import-a-mapping.md) guide covers the upload and linking steps; the rest of this page covers the delete side.

## Delete the mapping file

To remove a mapping, send a `DELETE` request to:

```
DELETE /xrefsets/{id}
```

You can do this whether or not the mapping is currently linked to any expression data files. Deleting the file is only half the job, though: the links that pointed to it are left behind, so clear those up too.

## Clear up the links

Deleting a mapping file does not remove its links to expression data. Remove those separately with a `DELETE` request to:

```
DELETE /links
```

Supply the link details (both accessions and their type labels) in the request body. If you are not sure which expression files a mapping is linked to, query `GET /links?firstId=<mappingAccession>` first to list them. See [Query mappings](query-mappings.md).

## What happens when you delete a study

Deleting a study does not remove the mapping files linked to its expression data. Those mappings stay in ODM, available to the rest of your organisation, and it is up to you to delete them separately once they are no longer needed.

## Who can do what

- Upload mapping files and create or delete links: Curator group only.
- Query mappings: any user.
- Delete a mapping file: only the original uploader of that file.

## Related

- [About cross-reference mapping](about-cross-reference-mapping.md)
- [Import a mapping](import-a-mapping.md)
- [Query mappings](query-mappings.md)
