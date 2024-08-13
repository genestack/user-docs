# Key Concepts

## How data is organized in ODM

The data in ODM is structured in an efficient way, ensuring comprehensive documentation 
and seamless integration from study design to data analysis.


<div class="grid cards" markdown>

- :octicons-book-16:  __Study__

    ---
    This is the starting point, where you define the context of your experiment, 
    including the aim and statistical design.

-  :octicons-note-16:  __Samples metadata__

    ---
    Here, you document the biological attributes of your samples, such as tissue type, disease status, and treatment conditions.

- :material-test-tube:  __Libraries/Preparations (Optional)__

    ---
    If applicable, detail the sample preparation methods and libraries used.

- :octicons-database-16:  __Data metadata__

    ---
    Describe how your data was processed, including normalization techniques, 
    the instrumentation used, and the types of processed data (e.g., TSV, VCF).

- :octicons-number-16:  __Data__

    ---
    This section encompasses the actual omics data generated from your study.

- :octicons-arrow-switch-16:  __Cross-reference__

    ---
    Ensure your data is easily interpretable by mapping data points to standardized 
    identifiers, like converting transcript information to gene IDs.

</div>

## Objects vs. Groups

### Object

Object is an individual data entity within ODM, such as a single sample, study, or library. 
Objects serve as the foundational units of data within the system and are amenable to management 
and querying operations.

### Group

A Group in ODM is a collection of related data entities or objects, created during a single API call. 

!!! example
    **Samples uploaded as part of one table file** constitutes a group. 
    If you upload an initial set of samples and then upload additional samples in a separate file to the same study, 
    these will form distinct sample groups within the study.

!!! warning "Limitation"
    Currently, ODM does not support merging groups. 
    Therefore, if you upload 10 samples from one file to a study and later upload another 5 samples 
    to the same study, the study will contain two separate sample groups. Understanding this limitation is 
    crucial for effective data organization and management within ODM.

The ODM APIs include endpoints that operate on both group and object levels. Group-level endpoints facilitate
operations on collections of related objects, while object-level endpoints focus on individual data entities.

## Templates

A **Template** controls the metadata attributes associated with various data objects, 
such as **Study**, **Sample**, **Experimental Data**, such as **Gene Expression**, 
**Variant** and **Flow cytometry**. Templates ensure that terms and values are harmonized 
and validated across the platform. Each template can include several metadata options:

* **Name**: The name of the metadata field (e.g., "Accession", "Organism"). 
* **Required**: Indicates whether the metadata field is mandatory. 
If marked as required and left blank or incorrectly filled, the field is highlighted in red.
* **Metainfo Type**: Specifies the type of metadata, such as text, integer, decimal, date, yes/no, and external link. 
* **Read-only**: Represents permissions for editing; "yes" means the metadata cannot be edited. 
* **Dictionary**: Specifies a dictionary providing standardized and unified terms for data curation and validation. 
* **Description**: A description of the attribute shown during curation as a hint.

!!! tip "For detailed instruction on how to work with templates, please refer to [Template Editor](../doc-odm-user-guide/template-editor.md){:target="_blank"} article"

## Validation

In the context of data curation, **validation** refers to the process of ensuring that metadata 
fields conform to predefined rules and standards set by a specific template. 
This process is essential for maintaining the integrity, consistency, and reliability of the data within the ODM.

### Importance of Validation

Validation is a critical aspect of data curation within the Open Data Manager, offering several key benefits:

* **Ensuring Data Quality**: Validation enforces metadata standards, ensuring that data entries are accurate,
complete, and consistent. This process helps maintain high data quality across studies and datasets.
* **Facilitating Data Harmonization**: By using custom dictionaries and standardized terms within templates, 
validation aids in harmonizing metadata. This harmonization makes it easier to integrate and compare data 
from different sources, enhancing the usability and interoperability of the data.
* **Streamlining Data Management**: Automated error detection and clear indications of invalid fields simplify 
the data curation process. This reduces the likelihood of manual errors and saves time, making data 
management more efficient and reliable.

Templates facilitate the consistent and accurate import and validation of data within ODM. 
They can be created, customized, and updated using the Template Editor application.

## API Token

**API Token**: An API token is a unique identifier used to authenticate requests made to the ODM API. 
It ensures that only authorized users can access and interact with the data and functionalities provided by the ODM. 
API tokens are essential for maintaining the security and integrity of the data management system.

### Importance of API Tokens

* **Security**: API tokens provide a secure method for authenticating users, ensuring that only those with 
valid credentials can access sensitive data and perform operations. 
* **Access Control**: They help in managing and controlling access to different parts of the ODM, 
allowing administrators to specify which users or applications can interact with specific data or functionalities. 
* **Auditability**: Using API tokens allows for detailed logging of API interactions, which is crucial for 
auditing purposes and for tracking who accessed or modified data. 
* **Efficiency**: They enable seamless and efficient interaction with the ODM API, as they eliminate the need 
for repetitive manual authentication, streamlining automated workflows and integrations.

By understanding and utilizing API tokens, you can enhance the security, control, and efficiency of your 
interactions with the Open Data Manager API.

By familiarizing yourself with these key concepts, you can navigate and utilize the Open Data Manager more 
effectively, ensuring that your data is well-organized, validated, and integrated for seamless data management 
and analysis.
