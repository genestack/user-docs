# Users and Groups

## Accessing Your Profile and Permissions

Explore and customize your account by accessing the profile section.

1. Log into the ODM:
    - Navigate to the ODM homepage.
    - Click on your profile (top right of the main page)
2. Explore Permissions:
    - Click on Profile to access information regarding your user permissions.
3. A new window will display indicating if you are an admin and the groups you are part of. 
This window also allows you to change your password and edit details.
4. View Existing Tokens and **Create a New Token**. In the new window, you will see any previously created tokens that 
you can rename or delete if needed. Click on **Create a New Token** to create a new one. Refer to the 
section [Getting a Genestack API token](../doc-odm-user-guide/getting-a-genestack-api-token.md) for more information.

![User Profile](../doc-odm-user-guide/doc-odm-user-guide/gifs/user-profile.gif)

## Create/Deactivate users

TBD

## Users and permissions

Understanding the roles, capabilities, and permissions within ODM is crucial for effective data management and 
collaboration. Each permission defines specific actions users can perform, such as creating, editing, or deleting 
groups, and managing templates. Users must have the appropriate permissions to carry out these actions, ensuring a 
secure and well-organized data environment.

### Available Permissions

There are five permissions available in the system. Descriptions of the permissions are displayed when you 
hover over the mouse.

1. **Manage organization**: Create and deactivate users, change their passwords, and grant permissions.
2. **Manage groups**: Access and manage all existing groups, even if you are neither an admin nor a member of the group. 
This permission is particularly recommended for integration purposes, where centralized management of group 
permissions across systems is required
3. **Set up templates**: Create and modify templates.
4. **Access all data**: Access all studies in the system. This permission is recommended for integration purposes, 
enabling comprehensive data access for system-wide operations and integrations.
5. **Configure facets**: Set the desired list and order of filtering facets in the Study Browser for all users 
on the instance.

### **Setting and Managing User Permissions**

To set or change user permissions, you need to have the **Manage organization** permission:

1. **Accessing the Permissions Menu:**
    * On the main dashboard, click on the three-line menu button at the top left. 

    !!! warning "Permissions required"
        If you have the **Manage organization**
        permission, this menu will display the option **Users and Permissions**. If you do not have this permission,
        the option will not be available.

2. **Managing Permissions:**
    * If you have access, click on **Users and Permissions**. This option will open a new window where you can see all 
the users within your organization. You can grant or revoke permissions by ticking the corresponding boxes for 
options such as **Manage groups**, **Set up templates**, **Access all data**, and **Configure facets**.
    * Use the search bar to find users you want to grant or revoke permissions to. 
    * Hover over the permissions to view a brief description of the permissions capabilities.

![Set permissions](../doc-odm-user-guide/doc-odm-user-guide/gifs/set-permissions.gif)
     
## Groups

User Groups in ODM facilitate collaboration and data sharing, representing departments, project teams, or any other
preferred structure.

To view the list of available Groups in your instance, click on the three-line menu at the top left of the dashboard. 
A menu will appear; select <strong>Groups</strong> This option is available to all users, regardless of their permissions.

The new window will display a list of available groups in your instance. Click on each group to view its members. This
window also shows the primary roles within each group: the **Group Administrator**, who can add members, assign roles, 
and share data with the group, and **Group Members**, who can share data with the group.

You can also add new members to groups or create new groups. See the instructions below for more details.
