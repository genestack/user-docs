---
diataxis: explanation
tab: odm-api
---

# About the Processors Controller

The Processors Controller is the ODM API for running file transformations: it lets you discover what transformation images are available, configure how they process your data, and execute and monitor transformation jobs. Its purpose is to remove preprocessing as a barrier to ingestion - you attach the file you have and ODM transforms it into queryable objects. Transformations cover both metadata and data: `metadata-basic` converts a CSV into indexable sample objects, while `hdf5-cells` extracts cell-type annotations, dimensional-reduction results, and processed expression values from an H5AD or H5 file into ODM Cell Groups and Expression Groups.

Transformations are managed through the ODM Processors Controller API, which is built on three related components: images, configurations, and jobs.

These three map onto a simple idea: an image is *what processing to do*, a configuration is *how to tune it*, and a job is *doing it once, against specific files*. The same image and configuration can drive many independent jobs.

## Transformation images

Transformation images are versioned container images (self-contained, ready-to-run packages of the processing software) that run the processing logic. The transformation itself is defined in the image. Available image versions can be queried through the API. Each image handles a specific input/output format pair: for example, `metadata-basic` converts CSV files to TSV-based Sample metadata objects; `hdf5-cells` converts H5AD or H5 single-cell files into ODM Cell Groups, Expression Groups, and associated metadata. When starting a job you can specify either `latest` or a specific release tag. You cannot change what an image does (its processing logic is fixed in code), but you can adjust its behaviour, within the scope the image supports, through a configuration.

## Transformation configurations

Transformation configurations are optional: a configuration is a reusable handle for tuning how an image processes your input, within the scope the image's code already allows. Configurations are JSON documents (a structured, text-based settings format) that define how an input file should be processed, including the input format, metadata extraction rules, and curation logic. Configurations are stored centrally and identified by an integer ID. The same configuration can be reused across multiple input files that share the same structure, and configurations can be created, retrieved, updated, and archived independently of any particular run. Configurations are versioned: updating a configuration does not overwrite it but saves the current state as a previous version and increments the active version. Earlier versions remain retrievable, so a job can always be audited or re-run with the exact parameters it used. Configurations are never deleted; instead they can be archived, which hides a configuration from the default listing and blocks further updates while keeping it retrievable and usable in jobs.

## Transformation jobs

Transformation jobs are the execution records. A job combines an image and one or more input file accessions and a configuration, then runs the transformation and produces output plus a processing log. Jobs are independent: the same input file can be submitted again with a different configuration or image without affecting previous runs.

Job operations respect ODM's existing permissions: you can only act on a job if you have access to the studies its input attachments belong to, and creating or managing jobs requires the appropriate curation permissions.

A job is not where your results are stored. As it runs, the transformation writes its output into ODM as ordinary objects, so once the job finishes those results are part of your ODM data like anything else.

When a job finishes, the transformation is complete and its processing container is released. A finished job does not mean ODM is idle, though: once the import completes, ODM begins indexing the imported data, and for large single-cell files this can take considerable time and load ODM heavily. The data may not be available through the API until indexing finishes, so avoid queuing many large jobs back-to-back on the assumption that a completed job has freed the system. The job's record, including its final status and full logs, is retained in line with ODM's standard log retention policy and stays retrievable through the same API endpoints, whether the job is still running or long finished.

You can cancel a job while it is still running; it is then recorded in the terminal `CANCELLED` state, distinct from a failure. Its final status and logs remain available like any other job's.

## Dry-run mode

Transformations can be run in dry-run mode by setting `dry_run: true`. A dry run validates the configuration and input without writing any objects to ODM, which makes it the safest way to iterate on a configuration before committing results. For the steps to run a job in dry-run mode, see [How to run a transformation](how-to-run-a-transformation.md).

Dry-run is currently implemented only by the `hdf5-cells` image. The `dry_run` flag is accepted on any job, but only `hdf5-cells` acts on it; for other images the flag currently has no effect.

## Transformation logs

Each job produces a log recording processing steps, warnings, errors, the source file name and accession, and the accessions of any ODM objects it created. Logs are retained in line with ODM's standard log retention policy and are retrievable through the API: the logs endpoint returns the live log while the job runs and the archived log once it has finished, transparently.
