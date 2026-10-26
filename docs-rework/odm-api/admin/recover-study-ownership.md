---
diataxis: how-to
tab: odm-api
---

# How to recover ownership of studies with a deactivated owner

When a study owner's account is deactivated, their studies stay in ODM with nobody able to transfer them: only a study owner can transfer ownership, and the owner can no longer sign in. Ownership recovery closes that gap. You list the studies whose owner is deactivated, then assign them to an active user who takes over responsibility for them.

For the complete endpoint specification, see the [Swagger UI](/swagger/helper/). Both endpoints are in the `manageData` definition.

## Prerequisites

- The **Ownership Recovery Administrator** role. The role covers every study in the organisation whose owner is deactivated, whether or not the study is shared with you.
- The email address of the active user who will become the new owner.

## Find the studies to recover

To list studies whose owner is deactivated:

```text
GET /api/v1/manage-data/ownership-recovery/studies
```

Called without parameters, the endpoint returns every study in the organisation whose owner is deactivated. To narrow the list to the studies of one former owner, pass that user's email address in `ownerEmail`:

```text
GET /api/v1/manage-data/ownership-recovery/studies?ownerEmail=john.doe@genestack.com
```

Each item gives the study's accession, title, creation date, and current owner. Results are sorted by accession in ascending order:

```json
{
  "cursor": "GSF015641",
  "data": [
    {
      "genestack:accession": "GSF015641",
      "studyTitle": "BLUEPRINT haematopoietic epigenomes",
      "createdAt": "2024-03-18 09:41:12",
      "ownerEmail": "john.doe@genestack.com"
    }
  ]
}
```

Use `limit` to cap the number of studies per response, up to a maximum of 2,000. To page through a longer list, pass the `cursor` value from one response to the next request.

## Assign a new owner

Send the accessions of the studies and the email address of the new owner:

```text
PATCH /api/v1/manage-data/ownership-recovery/studies
```

```json
{
  "accessions": ["GSF015641"],
  "newOwnerEmail": "jane.doe@genestack.com"
}
```

The new owner must be an existing, active user of the same organisation. ODM checks every accession before it changes anything: each study must exist, and its current owner must be deactivated. A study whose owner is still active cannot be reassigned through this endpoint, because only its owner can transfer it.

The response lists each reassigned study in the same shape as the `GET` items, with its new owner and, for confirmation, the previous one:

```json
[
  {
    "genestack:accession": "GSF015641",
    "studyTitle": "BLUEPRINT haematopoietic epigenomes",
    "createdAt": "2024-03-18 09:41:12",
    "ownerEmail": "jane.doe@genestack.com",
    "previousOwnerEmail": "john.doe@genestack.com"
  }
]
```

Each reassignment is recorded in the audit log as a `CHANGE_OWNER` event with source `API`, in which `ownershipChangerId` identifies you rather than the previous owner. See [Audit event types reference](audit/audit-event-types-reference.md#change_owner).

## Related

- [Sharing and ownership](../../overview/access-control/sharing-and-ownership.md), how study ownership works.
- [Transfer study ownership](../../contribute/sharing/transfer-study-ownership.md), the owner's own transfer workflow in the interface.
- [Activate and deactivate users](../../admin/manage-users/activate-and-deactivate-users.md)
- [Roles](../../overview/access-control/roles.md)
