---
diataxis: how-to
tab: api-libraries
---

# Load a custom ontology

This guide explains how to load a custom dictionary or ontology into ODM using the `odm-update-dictionary` script.

> Uploading a dictionary with the same name as an existing dictionary creates a new version (new accession) of that dictionary. The system marks the previous version as obsolete, which appears highlighted in red in the Template Editor. Existing templates that reference the old version must be updated to use the new one.

## Prerequisites

- Configured ODM SDK. See [Configure the ODM SDK](../configure.md).
- An API token or alias. See [Authentication and tokens](../../../odm-api/getting-started/authentication-and-tokens.md).
- One or more dictionary files in CSV, JSON, OWL, OBO, or TTL format, hosted at an accessible FTP or HTTPS URL. For CSV format details, see [CSV dictionary format reference](csv-dictionary-format-reference.md). For SKOS-encoded vocabularies, see [SKOS dictionary reference](skos-dictionary-reference.md).
- A `dictionaries.json` file describing the dictionaries to load.

## Steps

1. Open your `dictionaries.json` file and set the `name`, `url`, and `description` for each dictionary. The `name` is what will appear in ODM; the `url` is the hosted location of the dictionary file:

    ```json
    [
        {
            "name": "NCI Thesaurus",
            "url": "http://purl.obolibrary.org/obo/ncit.owl",
            "description": "NCI Thesaurus (NCIt) is a reference terminology that includes broad coverage of the cancer domain, including cancer related diseases, findings and abnormalities."
        }
    ]
    ```

    To load multiple dictionaries, repeat the object in the array.

2. Explore script options:

    ```bash
    odm-update-dictionary -h
    ```

3. Run the import command, providing the alias you configured and the full path to your `dictionaries.json` file:

    ```shell
    odm-update-dictionary -u YOUR_ALIAS_FOR_USER \
      --file_with_dictionaries /FULL_PATH_TO_THE_DICTIONARIES_JSON_FILE/dictionaries.json
    ```

    If `dictionaries.json` is in your current working directory, you can omit the full path:

    ```shell
    odm-update-dictionary -u YOUR_ALIAS_FOR_USER --file_with_dictionaries dictionaries.json
    ```

    You can also use `-H [hostname]` instead of `-u` to specify the environment directly.

4. After loading, the dictionary is indexed automatically in the background. Indexing can take several minutes (approximately 25 minutes for a 600 MB ontology). You can monitor the indexing task in the ODM Task Manager logs.

## Related

- [About dictionaries and ontologies](about-dictionaries.md)
- [CSV dictionary format reference](csv-dictionary-format-reference.md)
- [SKOS dictionary reference](skos-dictionary-reference.md)
