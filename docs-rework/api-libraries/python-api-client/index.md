---
diataxis: explanation
tab: api-libraries
---

# Python API Client

The ODM Python API Client (`odm-api`) is a generated Python wrapper around the ODM REST API. It exposes ODM endpoints as Python methods, making it convenient to call the API from Python scripts and Jupyter notebooks without constructing raw HTTP requests.

## When to use the Python API Client

Use the Python API Client when you want programmatic access to ODM from Python, for example, to integrate ODM into a data pipeline, automate queries, or explore datasets interactively in a Jupyter notebook.

The Python API Client is distinct from the ODM SDK. The SDK is a higher-level package with pre-built workflows for common operations such as importing studies or managing templates. The Python API Client is a thinner, generated wrapper that maps directly to the REST API endpoints, giving you more control at the cost of more verbosity.

## Pages in this section

<div class="grid cards gs-section-cards" markdown>

- __[Install](install.md)__

    ---

    How to install the package.

- __[Usage example](usage-example.md)__

    ---

    A worked example showing how to authenticate and call an endpoint.

</div>

## Relationship to the REST API

The Python client is generated from the OpenAPI specification (Swagger) that describes the ODM REST API. If you are working with the client, it is useful to understand the underlying API structure. See [Swagger orientation](../../odm-api/getting-started/swagger-orientation.md).

The source distribution also includes auto-generated in-tree documentation. After installation, consult the package's own docs for a complete method reference.
