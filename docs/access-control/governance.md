# Data Governance

The Open Data Manager (ODM) platform indexes both data and metadata to support efficient
search and exploration.

## Metadata

* A structured representation of metadata is stored in ODM’s internal MySQL database.
* This acts as a partial copy of metadata, ensuring fast performance for:

    * Search
    * Filtering
    * Data exploration

## Raw Data

* Raw files (e.g., images, BAM files) are not copied into ODM.
Instead, ODM stores pointers to the files in their existing storage locations.

## Processed and Indexed Data

* Processed data is stored in a columnar database, enabling it to be indexed and
searchable within ODM.

## Attachments

* When data files are imported via the GUI or attached to a study (e.g., supplementary
documents), they must be uploaded into the platform’s S3 bucket.
* This creates a copy of the file in ODM, ensuring accessibility through the user interface.

## Current Limitation

* ODM currently supports a single S3 bucket for attachments.

| Type          | Example                                                                                                       | Details                                                                                          | Copy                                                  | Configurability                                                |
|---------------|---------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------|-------------------------------------------------------|----------------------------------------------------------------|
| Attachments   | .pdf, .ppt, .h5 – can be anything                                                                             | ODM indexes basic file metadata (name, date, type, file contents for archives like .zip and .h5) | Copy is always stored in ODM. We use ODM’s S3 bucket. | Can configure to use the customer’s S3 bucket.                 |
| Metadata      | E.g. .tsv metadata files (e.g. <https://s3.amazonaws.com/bio-test-data/odm/Test_1000g/Test_1000g.samples.tsv>). | ODM captures and indexes study, sample, library/prep and other metadata.                         | Copy is always stored in ODM’s databases.             | No region separation made, use permissions to control access.  |
| Raw Data      | E.g. .fastq, .bam., images, and so on – if it’s not an attachment and not indexed data.                       | ODM stores and indexes the pointer to the file and nothing else.                                 | No copy is made anywhere.                             |                                                                |
| Indexed Data  | E.g., tabular data, VCFs, etc.                                                                                | ODM indexes most of the data by storing a compressed partial copy of the data columns.           | Copy is made.                                         | No configurability.                                            |
