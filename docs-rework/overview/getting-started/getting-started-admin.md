---
diataxis: tutorial
tab: overview
---

# Getting started: administering users and groups

In this tutorial you will add a new user to ODM, configure their permissions, manage their account status and password, and organise users into groups. By the end, you will have completed a full administrative cycle, from onboarding a user to managing the groups they belong to.

## Before you begin

You need an account with the **Manage organisation** permission to manage users and their permissions. To work with groups, you also need the **Manage groups** permission. See [Permissions](../access-control/permissions.md) for a full description of what each permission enables.

## Step 1: Confirm your admin status

Click your profile icon at the top-right of the Dashboard. Your profile view shows the **Admin** label alongside your permissions list: the groups you belong to, your capabilities (admin, curator), and your active API tokens. If you see this label, you are ready to proceed.

<figure markdown="span">
![User Profile](../../assets/user-guide/quick-start/quick-start-images/3Profile.png)
<figcaption>The user profile panel shows your group memberships, capabilities, and active API tokens.</figcaption>
</figure>

## Step 2: Access Users and Permissions

Click the three-line menu at the top-left of the Dashboard and select **Users and permissions**. A window opens listing all users on your ODM instance. This section is also accessible directly from the main Dashboard if you have the relevant permissions.

<figure markdown="span">
![Users and Permissions menu](../../assets/user-guide/quick-start/quick-start-images/4Users.png)
<figcaption>Click the three-line menu at the top-left of the Dashboard to reach Users and Permissions.</figcaption>
</figure>

## Step 3: Add a new user

In the Users and Permissions view, click **+ New user**. A form opens where you enter the new user's details. The system automatically detects whether the email address already belongs to an existing account. When you are satisfied with the details, click **Add**. You will see the new user appear in the user list.

<figure markdown="span">
![Add new user form](../../assets/user-guide/quick-start/quick-start-images/6AddUsers.png){ width="400" }
<figcaption>Enter the new user's details and click Add. ODM will warn you if the email address is already registered.</figcaption>
</figure>

<figure markdown="span">
![New user confirmed](../../assets/user-guide/quick-start/quick-start-images/7ConfirmNewUSer.png)
<figcaption>The newly added user now appears in the Users and Permissions list.</figcaption>
</figure>

## Step 4: Grant or revoke permissions

From the Users and Permissions view, find the user you want to configure. Use the search bar if the list is long. Tick or untick the checkboxes for each permission: **Manage organisation**, **Manage groups**, **Set up templates**, **Access all data**, and **Configure facets**. Hover over any checkbox to read a brief description of what that permission enables. Changes take effect as soon as you toggle the checkbox.

<figure markdown="span">
![Permissions panel](../../assets/user-guide/quick-start/quick-start-images/9ViewUsers.png)
<figcaption>Tick the boxes to grant or revoke permissions. Use the search bar to locate a specific user quickly.</figcaption>
</figure>

See [Permissions](../access-control/permissions.md) for full descriptions of each permission and its scope.

## Step 5: Create a group

Click the three-line menu at the top-left of the Dashboard and select **Groups**. In the Groups view, click **+ New Group**, enter a name, and click **Create**. The group is created and you are automatically assigned as Group Admin. Each group requires at least one admin at all times.

<figure markdown="span">
![Groups menu](../../assets/user-guide/quick-start/quick-start-images/13Groups.png)
<figcaption>Click the three-line menu to reach the Groups section.</figcaption>
</figure>

<figure markdown="span">
![Create a new group](../../assets/user-guide/quick-start/quick-start-images/14CreateNewGroup.png)
<figcaption>Click + New Group, enter a name, and click Create. You are assigned as Group Admin automatically.</figcaption>
</figure>

## Step 6: Add the user to the group

Open the group you just created, then click **New members**. Search for the user you added in Step 3, select them, and click **Add member**. The user appears in the group immediately.

<figure markdown="span">
![Add members to a group](../../assets/user-guide/quick-start/quick-start-images/15AddMembers.png)
<figcaption>Search for the user by name, then click Add member to confirm.</figcaption>
</figure>

<figure markdown="span">
![Members confirmed](../../assets/user-guide/quick-start/quick-start-images/17ConfirmMembers.png)
<figcaption>The group now shows the newly added member.</figcaption>
</figure>

## What you accomplished

You have completed the core administrative workflow in ODM: confirmed your admin status, added a new user, configured their permissions, created a group, and added that user to it. For account management tasks such as changing passwords, activating or deactivating users, managing group roles, and deleting groups, see the how-to guides in the [Admin](../../admin/index.md) tab.
