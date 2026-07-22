---
diataxis: how-to
tab: odm-api
---

# How to query cross-reference mappings

This guide explains how to query ODM's cross-reference mappings to look up gene–transcript relationships, retrieve mappings for a study, or check which mappings are available for an expression data file.

## Prerequisites

- An API token. See [Authentication and tokens](../../getting-started/authentication-and-tokens.md).
- Any user can query mappings. Mappings are shared across all members of an organisation.

## Find genes or transcripts across all mapping files

To return entries across all mapping files, supply gene IDs or transcript IDs of interest to:

```
GET /xrefsets/entries
```

Pass your identifiers as repeated query parameters: `geneId=ENSG00000230368&geneId=ENSG00000188976` or `transcriptId=ENST00000230368&transcriptId=ENST00000188976`.

## Find within a specific mapping file

To return entries within a particular mapping file, supply the mapping accession as the path parameter and the gene or transcript IDs as query parameters:

```
GET /xrefsets/{id}/entries
```

## Retrieve the mapping for genes in a study

To look up transcript IDs for given genes in a specific study, follow these three steps.

**Step 1: Get the expression group accession for the study.**

Supply the study accession as the `studyQuery` parameter:

```
GET /omics/expression/group?studyQuery=<studyAccession>
```

**Step 2: Get the mapping file linked to that expression group.**

Submit a `GET` request to `/links` with `firstId` set to the expression group accession and `secondType` set to `geneTranscriptMapping`:

```
GET /links?firstId=<expressionGroupAccession>&secondType=geneTranscriptMapping
```

The endpoint returns an array of mapping accessions. If more than one is returned, inspect each via `GET /xrefsets/{id}/metadata` and choose the mapping of interest.

**Step 3: Query the mapping for the genes of interest.**

Submit a `GET` request to the entries endpoint for the chosen mapping, supplying the gene IDs:

```
GET /xrefsets/{id}/entries?geneId=ENSG00000230368&geneId=ENSG00000188976
```

## Perform OMICS queries using gene or transcript IDs

Gene and transcript IDs can be passed directly to OMICS expression queries via the `exQuery` parameter:

```
GET /omics/expression/data?exQuery=feature%3DENST00000230368%2CENST00000188976
```

Decoded, this is `feature=ENST00000230368,ENST00000188976`. ODM resolves the transcript IDs through the linked mapping and returns matching expression data.

## Check which mappings are linked to an expression file

Submit a `GET` request to `/links` with `firstId` set to the expression group accession and `secondType` set to `geneTranscriptMapping`. This returns the accessions of all mapping files linked to that expression group. Inspect a specific mapping via:

```
GET /xrefsets/{id}/metadata
```

It is also possible to record the mapping file URL in metadata templates so that it appears in the ODM user interface.

## Check which expression files are linked to a given mapping

Submit a `GET` request to `/links` with `firstId` set to the accession of the mapping file. This returns the accessions of all expression groups linked to that mapping, which is useful when you need to know which links to clean up before deleting the mapping.

## Related

- [About cross-reference mapping](about-cross-reference-mapping.md)
- [Import a mapping](import-a-mapping.md)
- [Search imported data](../../explore/search-imported-data.md)
