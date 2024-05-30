# How to load custom dictionaries (ontologies)

This article explains how to load custom dictionaries (ontologies) in ODM.

> Uploading a dictionary with the same name as a previous dictionary will create a new version (new accession) of the dictionary and the system will mark the old version as obsolete, which will highlight it red in the template editor. Templates will need to be updated to use the new dictionary.

## Requirements

- Configured odm-sdk. See [Configured odm-sdk](../../configuration.md)
- User should have Bearer Token or API token. See [Getting a Genestack API token](https://odm-user-guide.readthedocs.io/en/latest/doc-odm-user-guide/getting-a-genestack-api-token.html#token-label)
- A file describing dictionaries, e.g.: [dictionaries.json](loading-new-ontology/dictionaries.json)
- One or more dictionaries in CSV, JSON, OWL, OBO or TTL formats, hosted at FTP or HTTP web addresses, see [dictionary example](http://purl.obolibrary.org/obo/go.owl)

## Setting up dictionary name/location

Open the `dictionaries.json` file and replace the `name`, `url` and `description` sections with the desired dictionary name as it will appear in ODM, dictionary location, and dictionary description.

```text
[
    {
        "name": "NCI Thesaurus",
        "url": "http://purl.obolibrary.org/obo/ncit.owl",
        "description": "NCI Thesaurus (NCIt) is a reference terminology that includes broad coverage of the cancer domain, including cancer related diseases, findings and abnormalities. The NCIt OBO Edition aims to increase integration of the NCIt with OBO Library ontologies"
    }
]
```

Multiple dictionaries can be supplied by repeating the section in curly brackets.

## Running the command to import dictionaries

To explore the full list of supported arguments use the following command:

```bash
odm-update-dictionary -h
```

Run the following command from your terminal:

```shell
odm-update-dictionary -u YOUR_ALIAS_FOR_USER --file_with_dictionaries /FULL_PATH_TO_THE_DICTIONARIES_JSON_FILE/dictionaries.json
```

`-u` [optional] parameter should contain the alias for the user you set up with the Genestack python client previously.<br/>
`-H [hostname]` [optional] hostname for the environment being used; you can use either `-u` or `-H`.<br/>
`--file_with_dictionaries` parameter should contain full path to the `dictionaries.json` file - replace `FULL_PATH_TO_THE_DICTIONARIES_JSON_FILE` with this path.<br/>
or run

```shell
odm-update-dictionary -u YOUR_ALIAS_FOR_USER --file_with_dictionaries dictionaries.json
```

if `dictionaries.json` is presented in the current working directory.

Once loaded the dictionary needs to be indexed. This will occur automatically in the background but can take several minutes (~25 minutes for a 600MB ontology). The indexing task can be monitored in the tasks log.
