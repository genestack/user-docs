# How to delete a study

## Requirements

- Configured odm-sdk. See [Configured odm-sdk](../../configuration.md)
- The user should have the "Manage organisation" permission and have Bearer Token or API token. See [Getting a Genestack API token](https://odm-user-guide.readthedocs.io/en/latest/doc-odm-user-guide/getting-a-genestack-api-token.html#token-label)

## Instructions

To explore the full list of supported arguments use the following command:

```bash
odm-delete-study -h
```

!!!warning Warning

    1. Only users with the “Manage organisation” permission can delete studies.
    2. The script doesn’t check that the file with the provided accession actually exists so if nothing is deleted but the script runs correctly it will still output 'Success'.
    3. The script doesn’t check the type of the file so if a template’s accession is provided instead of a study’s accession the template will be deleted. However, for deletion of templates please use the script from How to delete a template

Run the script and follow its login instructions, replacing the host name with the name of the instance the script will apply to. The script will print “Success” or an error stacktrace if there’s an error.

```shell
odm-delete-study --accession GSF244344 -H HOSTNAME
```
