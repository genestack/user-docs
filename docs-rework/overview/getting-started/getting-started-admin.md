---
diataxis: tutorial
tab: overview
---

# Getting started: administering users and groups

In this tutorial you will add a new user to ODM, configure their roles, manage their account status and password, and organise users into groups. By the end, you will have completed a full administrative cycle, from onboarding a user to managing the groups they belong to.

## Before you begin

You need an account with the **Organisation Administrator** role to manage users and their roles. To work with groups, you also need the **Group Administrator** role. See [Roles](../access-control/roles.md) for a full description of what each role enables.

Every action in this tutorial is performed through the ODM UI, but that interface is not the only way to administer users. You can manage accounts programmatically through the [user management endpoints](../../odm-api/admin/manage-user-accounts-via-api.md), which suits automation scripts and system integrations. You can also hand user and group provisioning to your identity provider through [SCIM integration](../../admin/scim-integration.md), which is the recommended approach whenever your identity provider supports SCIM 2.0.

## Step 1: Confirm your admin status

Click your profile icon at the top-right of the Dashboard. Your profile view shows the **Admin** label, the groups you belong to, your capabilities (admin, curator), and your active API tokens. If you see this label, you are ready to proceed.

<figure markdown="span">
![User Profile](../../assets/user-guide/quick-start/quick-start-images/admin1.gif)
</figure>

## Step 2: Access Users and Roles

Click the three-line menu at the top-left of the Dashboard and select **Users and Roles**. A window opens listing all users on your ODM instance. This section is also accessible directly from the main Dashboard if you have the relevant role.

<figure markdown="span">
![Users and Roles menu](../../assets/user-guide/quick-start/quick-start-images/usersandroles.gif)
</figure>

## Step 3: Add a new user

In the Users and Roles view, click **+ New user**. A form opens where you enter the new user's details. The system automatically detects whether the email address already belongs to an existing account. When you are satisfied with the details, click **Add**. You will see the new user appear in the user list.

<figure markdown="span">
![Add new user form](../../assets/user-guide/quick-start/quick-start-images/adduser.gif)
</figure>

## Step 4: Assign or remove roles

From the Users and Roles view, find the user you want to configure. Use the search bar if the list is long. Tick or untick the checkboxes for each role: **Organisation Administrator**, **Group Administrator**, **Template Administrator**, **Access all data**, **Catalogue Administrator**, **Ownership Recovery Administrator**, **Orphan Data Administrator**, **Transformation Configuration Administrator**, **Reference Data Administrator**, and **Audit Log Administrator**. Hover over any checkbox to read a brief description of what that role enables. Changes take effect as soon as you toggle the checkbox.

<figure markdown="span">
![Roles panel](../../assets/user-guide/quick-start/quick-start-images/addrole.gif)
</figure>

See [Roles](../access-control/roles.md) for full descriptions of each role and its scope.

## Step 5: Create a group

Click the three-line menu at the top-left of the Dashboard and select **Groups**. In the Groups view, click **+ New Group**, enter a name, and click **Create**. The group is created and you are automatically assigned as Group admin. Each group requires at least one admin at all times.

<figure markdown="span">
![Groups menu](../../assets/user-guide/quick-start/quick-start-images/creategroup.gif)
</figure>

## Step 6: Add the user to the group

Open the group you just created, then click **New members**. Search for the user you added in Step 3, select them, and click **Add member**. The user appears in the group immediately.

<figure markdown="span">
![Add members to a group](../../assets/user-guide/quick-start/quick-start-images/addusergroup.gif)
</figure>

## What you accomplished

You have completed the core administrative workflow in ODM: confirmed your admin status, added a new user, configured their roles, created a group, and added that user to it. For account management tasks such as changing passwords, activating or deactivating users, managing group roles, and deleting groups, see the how-to guides in the [Admin](../../admin/index.md) tab.
