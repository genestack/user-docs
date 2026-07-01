# About the Processors Controller

A transformation takes an attached input file and turns its contents into ODM objects. Some transformations produce indexable metadata: for example, ODM cannot index a CSV file directly as a source of metadata, but the `metadata-basic` transformation converts it into TSV-based metadata objects that ODM can index. Others turn raw data into structured ODM objects: for example, the `hdf5-cells` transformation converts single-cell HDF5 (H5AD/H5) files into ODM Cell Groups and Expression Groups. Either way, a transformation bridges the gap between the file you have and the ODM objects you need.

Transformations are managed through the ODM Processors Controller API, which is built on three related components: configurations, images, and jobs.

These three map onto a simple idea: an image is *what processing to do*, a configuration is *how to tune it*, and a job is *doing it once, against specific files*. The same image and configuration can drive many independent jobs.

## Transformation configurations

Transformation configurations are JSON documents (a structured, text-based settings format) that define how an input file should be processed, including the input format, metadata extraction rules, and curation logic. Configurations are stored centrally and identified by an integer ID. The same configuration can be reused across multiple input files that share the same structure, and configurations can be created, retrieved, updated, and archived independently of any particular run. Configurations are versioned: updating a configuration does not overwrite it but saves the current state as a previous version and increments the active version. Earlier versions remain retrievable, so a job can always be audited or re-run with the exact parameters it used. Configurations are never deleted; instead they can be archived, which hides a configuration from the default listing and blocks further updates while keeping it retrievable and usable in jobs.

## Transformation images

Transformation images are versioned container images (self-contained, ready-to-run packages of the processing software) that run the processing logic. Available image versions can be queried through the API. Each image handles a specific input/output format pair: for example, `metadata-basic` converts CSV files to TSV-based metadata objects (samples, libraries, preparations, cell metadata, expression, or variants); `hdf5-cells` converts H5AD or H5 single-cell files into ODM Cell Groups, Expression Groups, and associated metadata. When starting a job you can specify either `latest` or a specific release tag.

## Transformation jobs

Transformation jobs are the execution records. A job combines an image and one or more input file accessions and a configuration, then runs the transformation and produces output plus a processing log. Jobs are independent: the same input file can be submitted again with a different configuration or image without affecting previous runs.

Job operations respect ODM's existing permissions: you can only act on a job if you have access to the studies its input attachments belong to, and creating or managing jobs requires the appropriate curation permissions. See the [API reference](#) <!-- TODO(swagger): repoint to OpenAPI/Swagger spec (was api-reference.md) --> for the exact rules.

A job is not where your results are stored. As it runs, the transformation writes its output into ODM as ordinary objects, so once the job finishes those results are part of your ODM data like anything else.

When a job finishes it stops running, and the resources that were processing it are released: nothing keeps running in the background. What stays behind is the job's record: its final status and full logs. These are kept indefinitely, with no expiry, and are never deleted. You retrieve them through the same API endpoints whether the job is still running or finished long ago, so from your side nothing about fetching a job's status or logs changes once it is done.

You can cancel a job while it is still running; it is then recorded in the terminal `CANCELLED` state, distinct from a failure. Its final status and logs remain available like any other job's.

## Dry-run mode

Transformations can be run in dry-run mode by setting `dry_run: true`. A dry run validates the configuration and input without writing any objects to ODM, which makes it the safest way to iterate on a configuration before committing results. For the steps to run a job in dry-run mode, see [How to run a transformation](how-to-run-a-transformation.md).

!!! warning "Editorial TODO: resolve before publishing"
    Confirm which transformation images actually implement dry-run (validate-without-write). The flag is accepted for all jobs, but honoring it is image-specific. If not universal, scope this wording (e.g. to single-cell).

## Transformation logs

Each job produces a log recording processing steps, warnings, errors, the source file name and accession, and the accessions of any ODM objects it created. Logs are retained permanently and are always retrievable through the API: the logs endpoint returns the live log while the job runs and the archived log once it has finished, transparently. A finished job's log is never unavailable. Separately, the log is also uploaded into ODM as an attachment on the owning study, so it sits alongside the job's other generated files; this attachment is an additional copy and is not what keeps the log available.
