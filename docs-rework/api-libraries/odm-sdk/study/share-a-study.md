---
diataxis: how-to
tab: api-libraries
---

# Share a study

This guide explains how to share a study with one or more user groups using the `odm-share-study` script.

## Prerequisites

- Configured ODM SDK. See [Configure the ODM SDK](../configure.md).
- Membership in the Curator group and a Bearer token or API token. See [Authentication and tokens](../../../odm-api/getting-started/authentication-and-tokens.md).

> **Note:** There are two limitations to be aware of:
> 1. The script must be launched under the account of the study owner.
> 2. The script will fail if the target group name is used more than once among the groups you are a member of. Group names must be unique across the groups visible to you.

## Steps

1. Identify the accession of the study you want to share and the exact name of the group you want to share it with.

2. Explore script options:

   ```shell
   odm-share-study -h
   ```

3. Run the script, replacing the host name, study accession, and group name with your values. The script prints `Success` or an error stack trace:

   ```shell
   odm-share-study --study_accession GSF013340 --group_name GroupName -H HOST
   ```

   If the group name contains spaces, wrap it in single quotes:

   ```shell
   odm-share-study --study_accession GSF000745 --group_name 'Group name with space' -H HOST
   ```

## Related

- [Upload a study](upload-a-study.md)
