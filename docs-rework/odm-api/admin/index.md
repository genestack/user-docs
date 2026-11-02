---
diataxis: explanation
tab: odm-api
---

# Administer via API

Administering ODM through the API is about keeping your instance clean and its people in order, tidying up after failed imports, removing data you no longer need, and managing user accounts, all from your scripts rather than the interface. This section gives you the workflow guidance for doing that safely. For the same operations through the ODM user interface, see [Admin](../../admin/index.md).

Most of the admin API surface is documented directly in Swagger, so this section focuses on the operations that take a sequence of calls to get right.

## Choose your task

<div class="grid cards gs-section-cards" markdown>

- __[Find detached objects](find-detached-objects.md)__

    ---

    Identify and remove orphaned studies, samples, and omics objects no longer linked to any parent.

- __[Delete data](delete-data.md)__

    ---

    Delete studies you own, detached objects, templates, and reference data via the API, and check which role each needs.

- __[Recover study ownership](recover-study-ownership.md)__

    ---

    Assign a new owner to studies whose owner has been deactivated.

- __[Manage user accounts via API](manage-user-accounts-via-api.md)__

    ---

    Create, update, and deactivate users programmatically.

- __[Audit logs](audit/about-audit-logs.md)__

    ---

    Retrieve the trail of user and system actions for investigation, compliance, and support.

</div>
