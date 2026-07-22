---
diataxis: how-to
tab: api-libraries
---

# Usage example

ODM APIs let you perform large-scale, cross-study, and cross-omics analysis programmatically. The ODM OpenAPI Specification is available at `ODM_HOSTNAME/swagger/helper/`, where `ODM_HOSTNAME` is the URL of your ODM instance.

## Requirements

- `odm-api` installed. See [Install](install.md).
- An API token. See [Authentication and tokens](../../odm-api/getting-started/authentication-and-tokens.md).

## Example: search samples and display results as a table

The following script queries samples matching a disease filter and prints the first five results as a pandas DataFrame:

```python
import pandas as pd
import odm_api

configuration = odm_api.Configuration(
    host="ODM_HOSTNAME",
    api_key={'Genestack-API-Token': 'ODM_TOKEN'}
)

api = odm_api.SampleSPoTAsCuratorApi(
    api_client=odm_api.ApiClient(configuration=configuration)
)

query = '"Disease"="Healthy" OR "Disease"="Alzheimer Disease"'
samples = api.search_samples_as_curator(filter=query, page_offset=0)
print(pd.DataFrame.from_dict(samples.data[:5]))
```

Replace `ODM_HOSTNAME` with your ODM URL and `ODM_TOKEN` with your API token.

Example output:

```text
  genestack:accession Sample Source ID Sample Name Organism     Sex  Disease   Age Age Unit Tissue Cell Type  ... Family.ID Donor Treatment/Treatment Name Specimen Type Tissue or Cell Type Sample Source Continental Group Code Sample Type Population Code Sample ID Continental Group
0           GSF136813          HG00096        None     None    Male  Healthy  None     None   None      None  ...   HG00096                    Not treated           LCL               Blood         NHGRI                    EUR         DNA             GBR   HG00096       "European "
1           GSF136814          HG00097        None     None  Female  Healthy  None     None   None      None  ...   HG00097                    Not treated           LCL               Blood         NHGRI                    EUR         DNA             GBR   HG00097       "European "
2           GSF136815          HG00099        None     None  Female  Healthy  None     None   None      None  ...   HG00099                    Not treated           LCL               Blood         NHGRI                    EUR         DNA             GBR   HG00099       "European "
3           GSF136816          HG00100        None     None  Female  Healthy  None     None   None      None  ...   HG00100                    Not treated           LCL               Blood         NHGRI                    EUR         DNA             GBR   HG00100       "European "
4           GSF136817          HG00101        None     None    Male  Healthy  None     None   None      None  ...   HG00101                    Not treated           LCL               Blood         NHGRI                    EUR         DNA             GBR   HG00101       "European "
```
