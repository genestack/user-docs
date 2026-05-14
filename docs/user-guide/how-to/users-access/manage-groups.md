# Manage Groups

**Role:** Administrator.

User Groups in ODM facilitate collaboration and data sharing, representing departments, project teams, or any other preferred structure.

To view the list of available Groups in your instance, click on the three-line menu at the top left of the dashboard.
A menu will appear.

The new window will display a list of available groups in your instance. Click on each group to view its members. This
window also shows the primary roles within each group: the **Group Administrator**, who can add members, assign roles,
and share data with the group, and **Group Members**, who can share data with the group.

You can also add new members to groups or create new groups. See the instructions below for more details.

## Permission Limitations

!!! warning "Permissions required"
    To manage groups (create, edit, or delete), you must have the **Manage Groups** permission.

The Groups page in ODM provides a list of all groups to which a user belongs. However, user capabilities are restricted
based on their assigned permissions. Below are the key limitations depending on user permissions:

1. **Access to Groups:**
    * With Manage Groups permission: Users can access all groups within the system, irrespective of their membership status.
    * Without permission: Users can only access groups of which they are members.
2. **Creating a New Group:** Any user can create a new group through the user interface.
3. **Adding or Removing Members from a Group:**
    * With Manage Groups permission: Users can add or remove members from any group.
    * Without permission: Group Admin can add or remove members and edit roles only within groups they belong to.
4. **Deleting a Group:**
    * With Manage Groups permission: Any user can delete any group through the interface.
    * Without permission: Group Admin can only delete groups they are a part of.

## Creating a Group

To create a new group manually, follow these steps:

1. **Access the Groups Section**
    * Click on the three-line menu button at the top left of the dashboard to access the `Groups` section.

2. **Create a New Group:**
    * In the Groups window, click on the **\+New Group** button at the top of the window.
    * Enter a name for the new group in the new window that appears.
    * Click "Create" to finalize the creation of the group.
    * A new window will be displayed showing the new group has been created. By default, the user who creates the new
group is assigned as the **Group Admin**. It is important to notice that each group requires at least one group admin.

![Create Group](../../doc-odm-user-guide/doc-odm-user-guide/gifs/group-creation.gif)

## Managing Groups

Once you have created groups, you can edit details such as members, members' roles (group admin or group members),
and delete groups.

To manage groups in the interface, navigate to the section Groups (instructions described above) and select the group
you want to manage.

### Add New Members via Interface

* Click on the **\+New members** button to add members to the group.
* In the new window, you can select members from the list or use the search bar to find specific users.

**Confirm New Members:**

* After selecting the members, click **Add member** to confirm. The group will now display the recently added members.

### Edit Group Details

* You can edit the roles of group members by clicking on their role descriptions. You can change members to
administrators or vice versa. Note that each group must have at least one administrator.
* To remove a member, click on the three dots next to their username.

![Modify Group](../../doc-odm-user-guide/doc-odm-user-guide/gifs/modify-group.gif)

## Curator Group

The Curator group is a special group granting edit permissions to its members. Curators can import new studies and
edit any study shared with them.

Only Administrators can add or remove members to the Curator Group. To add new members, simply follow the instructions
described in previous sections and select the user to add.

1. Briefly, navigate to the Groups section. Select the group **Curator**.
2. Click on **+New member** and select the member to add.
3. Confirm the changes.
4. Once the user is added, the title will be displayed on their profile.

Curators can explore, edit, and curate data. However, some limitations are set based on their permissions:

* **Curators with Manage Groups permissions**: Members of the Curator group with full edit permissions.
Users can add or remove members of the Curator Group.

!!! danger "It is not advisable to delete the **Curator Group**, since Users need to be aware of potential changes"

## See also

- [Manage Users](manage-users.md)
- [Share a Study](../../how-to/sharing-permissions/share-a-study.md) — groups are used to share studies with other users.
