---
diataxis: how-to
tab: api-libraries
---

# Curate metadata with the curation script

The `odm-curate-study` script automates curation of study metadata by transforming raw metadata values into curated ones. It uses a rules file you provide, optionally validated against controlled vocabularies (dictionaries), and can match values using synonyms.

## Prerequisites

- Configured ODM SDK. See [Configure the ODM SDK](../configure.md).
- Membership in the Curator group and an API token or alias. See [Authentication and tokens](../../../odm-api/getting-started/authentication-and-tokens.md).
- A `rules.json` file describing the mappings you want to apply. See [Curation rules reference](curation-rules-reference.md) for the schema and examples.
- The accessions of the studies you want to curate.

## Basic usage

```bash
odm-curate-study --rules <rules.json> <study accession> -H GENESTACK_ENDPOINT_ADDR
```

Where `GENESTACK_ENDPOINT_ADDR` is the URL of your ODM instance.

To curate multiple studies in one run, separate accessions with spaces:

```bash
odm-curate-study --rules rules.json GSF000100 GSF000200 -H GENESTACK_ENDPOINT_ADDR
```

## Dry run

Test your rules without applying any changes. The script connects to the server and reports matches in the task output log, but does not modify any data:

```bash
odm-curate-study --rules <rules.json> --dry-run <study accession> -H GENESTACK_ENDPOINT_ADDR
```

## Overwriting existing values

By default, if a target key already contains a value, the script skips it and logs a warning. Use `--overwrite` to force the replacement:

```bash
odm-curate-study --rules <rules.json> --overwrite <study accession> -H GENESTACK_ENDPOINT_ADDR
```

The `--overwrite` flag does not apply to attributes marked as read-only in the template; those cannot be curated regardless. A warning is logged for any read-only attribute the script encounters.

## Tracking progress

You can monitor the curation job in the Genestack Task Manager. Detailed mapping results (which values were matched, remapped, or skipped) appear in the output logs.

## Explore script options

```bash
odm-curate-study -h
```

## Related

- [Curation rules reference](curation-rules-reference.md), rules.json schema, mapper variants, reassignment cases, and edge cases.
