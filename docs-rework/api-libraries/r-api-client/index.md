---
diataxis: explanation
tab: api-libraries
---

# R API Client

The ODM R API Client (`odmApi`) is a generated R wrapper around the ODM REST API. It exposes ODM endpoints as R methods, making it straightforward to query and interact with ODM from R scripts and bioinformatics workflows.

## When to use the R API Client

Use the R API Client when you want programmatic access to ODM from R, for example, to pull sample metadata into an analysis pipeline, filter and retrieve expression data, or automate queries as part of a Bioconductor or base-R workflow.

## Pages in this section

<div class="grid cards gs-section-cards" markdown>

- __[Install](install.md)__

    ---

    How to install the package and its dependencies.

- __[Usage example](usage-example.md)__

    ---

    A worked example showing how to authenticate and query samples.

</div>

## Relationship to the REST API

Like the Python client, the R client is generated from the OpenAPI specification (Swagger) that describes the ODM REST API. See [Swagger orientation](../../odm-api/getting-started/swagger-orientation.md) for an overview of the underlying API structure.
