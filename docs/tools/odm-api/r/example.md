# Usage of generated R API Client

## Requirements

- Installed odm-api. See [Installation odm-sdk](./installation.md)

### Example of usage

Script to search through samples and display them in table format:

```R
library(odmApi)
api_instance <- SampleSPoTAsCuratorApi$new()
api_instance$api_client$api_keys["Genestack-API-Token"] <- 'ODM_TOKEN'
api_instance$api_client$base_path <- 'https://ODM_HOSTNAME'
query <- '"Disease"="Healthy" OR "Disease"="Alzheimer Disease"'
result <- api_instance$SearchSamplesAsCurator(filter=query, response_format="term_id", returned_metadata_fields="minimal_data")
result$content$data[1:5]
```

The output (shorten):

```text
  genestack:accession Sample Source ID Sample Name Organism     Sex
1           GSF136813          HG00096        None     None    Male
2           GSF136814          HG00097        None     None  Female
3           GSF136815          HG00099        None     None  Female
4           GSF136816          HG00100        None     None  Female
5           GSF136817          HG00101        None     None    Male
```
