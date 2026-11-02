---
diataxis: how-to
tab: odm-api
---

# How to delete data

Deletion is how you permanently remove data from ODM, whether you are clearing out the detached debris of a failed import or retiring data you no longer need. A single call can take a lot with it, so it is worth knowing exactly what cascades before you run one.

> **Warning:** Deletion is irreversible. Deleted objects and their linked data cannot be recovered.

For the full endpoint specification, the [Swagger UI](/swagger/helper/) is the source of truth.

## Prerequisites

- The right to delete the objects you name, which depends on what they are. See [Who can delete what](#who-can-delete-what).

## Who can delete what

Each kind of object has exactly one route to deletion:

| Object | Who can delete it |
|---|---|
| A study and its child objects | The study owner |
| Detached objects | A user with the **Orphan Data Administrator** role |
| Templates | A user with the **Template Administrator** role |
| Reference genomes | A user with the **Reference Data Administrator** role |
| Dictionaries | A user with the **Reference Data Administrator** role |

To delete a child object of a study, such as a sample group or an attached file, you must own the study it belongs to. ODM checks every object in the request before it deletes anything, so if you do not own all of them, nothing is deleted. Owning a study does not let you delete detached objects, templates, reference genomes, or dictionaries, even ones you created; each of those needs its role. Neither the **Organisation Administrator** nor the **Access all data** role grants the right to delete data.

If you are not the study owner, the request returns `403`:

```json
{
  "error": {
    "status": 403,
    "message": "Only the study owner can delete a study and its child objects."
  }
}
```

For the full list of roles, see [Roles](../../overview/access-control/roles.md).

## Delete an object

To delete an object, call `DELETE /api/v1/manage-data/data` with the Genestack accession of the object or group in the request body. For example, to delete the study `GSF1147012`:

```json
{
  "accession": "GSF1147012"
}
```

A `202` response confirms the request was accepted. Deletion then runs asynchronously. To confirm it finished, check that the object no longer appears where you would normally find it: search for a study or its child objects in the Study Browser or via the API, and for a detached object, repeat the `GET /api/v1/manage-data/detached-objects` request.

## What a delete takes with it

Deletion cascades down the data model. Deleting a study removes everything linked to it: sample groups, library groups, preparation groups, tabular data, VCF data, flow cytometry data, and attached files. Deleting a signal group removes the group along with all of its associated data objects.

You can delete:

- Studies and all their linked entities.
- Sample groups, library groups, and preparation groups.
- Tabular data (expression), gene variant data, and flow cytometry data.
- Cell metadata groups and cell expression groups.
- Attached files (available since release 1.59).
- Templates (see [Delete a template](#delete-a-template)).
- Reference genomes (see [Delete a reference genome](#delete-a-reference-genome)).
- Dictionaries (see [Delete a dictionary](#delete-a-dictionary)).

## Delete a template

Only a user with the **Template Administrator** role can delete a template. Pass the template's accession in the request body, as for any other object. Without the role, the request returns `403` and names the role it requires:

```json
{
  "error": {
    "status": 403,
    "message": "The following object cannot be deleted: GSF244345. Required system role: 'Template Administrator'."
  }
}
```

To delete a template with the ODM SDK instead, see [Delete a template](../../api-libraries/odm-sdk/templates/delete-a-template.md).

## Delete a reference genome

Only a user with the **Reference Data Administrator** role can delete a reference genome.

If you delete a reference genome that is linked to any VCF groups, gene-name-based variant search (`variantFeature`) becomes unavailable for those VCF groups.

## Delete a dictionary

Only a user with the **Reference Data Administrator** role can delete a dictionary.

You can delete a dictionary only when no template uses it. If any template still refers to the dictionary, the request fails with an error that lists those templates. Update each listed template so it no longer uses the dictionary, then send the request again. To change a template, see [Create and edit a template](../../contribute/templates/create-and-edit-a-template.md).

## S3 cleanup

When you delete a data file that was imported from a local computer, ODM automatically removes the corresponding file from S3 (since release 1.60).

## Related

- [Find detached objects](find-detached-objects.md), identify orphaned objects before deletion.
- [Roles](../../overview/access-control/roles.md), the roles that grant deletion rights.
- [About dictionaries and ontologies](../../api-libraries/odm-sdk/dictionaries-and-ontologies/about-dictionaries.md)
- [Authentication and tokens](../getting-started/authentication-and-tokens.md)
