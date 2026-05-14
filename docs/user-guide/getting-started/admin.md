# Getting Started: Administrator

An Administrator can manage users and groups, assign and revoke permissions, deactivate accounts, and delete data in the Open Data Manager. Administrators have all the capabilities of Data Contributors and Consumers, plus organization-level access granted by the **Manage organization** permission. Working with groups also requires the separate **Manage groups** permission.

## Where to start

Work through [Your First Session](../tutorials/your-first-session.md) to get familiar with the ODM interface. Then return here to learn about your administrative capabilities.

## Common tasks

- [Manage users](../how-to/users-access/manage-users.md) — add new users, edit their details, change passwords, and activate or deactivate accounts
- [Manage groups](../how-to/users-access/manage-groups.md) — create groups, add or remove members, change member roles, and delete groups
- [Manage your profile](../how-to/users-access/manage-your-profile.md) — view your own permissions, generate API tokens, and update your settings

## Using the interface

Admin tasks are accessed from the **Users and permissions** and **Groups** sections, available from the three-line menu at the top left of the dashboard (or directly from the dashboard if your permissions allow).

**Managing users:**

- Navigate to **Users and permissions** to see all users in the ODM instance.
- Click **+ New user** to add a user; fill in their details and click **Add**.
- Use the permissions table to grant or revoke capabilities: **Manage organization**, **Manage groups**, **Set up templates**, **Access all data**, and **Configure facets**. Hover over any permission name to see a brief description.
- To deactivate or reactivate a user, click the three dots next to their name and select **Deactivate** or **Activate**.
- To change a user's password, click the three dots next to their name, select **Change Password**, authenticate as an admin, and enter the new password.

**Managing groups:**

- Navigate to **Groups** from the three-line menu.
- Click **+ New Group**, enter a name, and click **Create**. The creator is automatically assigned as Group Admin.
- To add members, open the group and click **New members**; search for users and click **Add member**.
- To remove a member, click the three dots next to their name and select **Remove member**. Each group must retain at least one admin — reassign admin status before removing the current admin.
- To change a member's role (member ↔ admin), click their current role label in the group view.
- To delete a group, click the three dots on the right of the group row and select **Delete group**. Deletion is permanent.

## Using the API

Administrators have access to the **Manage organisation** endpoint group in Swagger, in addition to all Consumer and Contributor endpoints. The Swagger interface is available from the dashboard under **API Documentation**.

**Key admin API use cases:**

- **Find detached data**: use `GET /api/v1/manage-data/detached-objects` to list data objects that are not linked to any study. Filter by type (`STUDY`, `SAMPLE_GROUP`, `LIBRARY_GROUP`, `PREPARATION_GROUP`, `TABULAR_DATA`, `GENE_VARIANT`, `FLOW_CYTOMETRY`) and use the `cursor` field in the response to paginate through results. Requires **Manage organization** and **Access all data** permissions.
- **Delete data**: use `DELETE /api/v1/manage-data/data` to permanently remove a data object or group by accession number. This action is irreversible. Requires **Manage organization** and **Access all data** permissions.

For detailed API instructions, see:

- [Manage users (API sections)](../how-to/users-access/manage-users.md)
- [Manage groups (API sections)](../how-to/users-access/manage-groups.md)
- [Generate an API token](../how-to/users-access/generate-api-token.md)

> **For full API capabilities, see the API how-to guides.**

## Go deeper

- [Roles & Permissions](../reference/roles-permissions.md) — full breakdown of all permissions and what they allow
- [Key Concepts](../explanation/data-model.md) — data model and ODM architecture overview
