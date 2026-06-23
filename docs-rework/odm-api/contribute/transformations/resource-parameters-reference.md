---
sources:
  - path: docs/user-guide/doc-odm-user-guide/api-reference.md
    lines: [162, 184]
  - path: docs/user-guide/doc-odm-user-guide/how-to-sc-hdf5-transformations.md
    lines: [93, 95]
  - path: docs/user-guide/doc-odm-user-guide/how-to-sc-hdf5-transformations.md
    lines: [345, 345]
diataxis: reference
tab: odm-api
---

# Job resource parameters reference

This reference covers the parameters you set at job submission time that affect how the processing environment is provisioned. These are distinct from the transformation configuration, which controls what the pipeline does with your data. Resource parameters are set in the request body of `POST /api/v1/transformations/jobs`. For the full job submission schema, see [Processors Controller API reference](api-reference.md).

---

## `volume_size`

| Property | Value |
|---|---|
| Type | string (Kubernetes quantity, e.g. `30Gi`) |
| Required | No |
| Default | the image's `default-volume-size` label, or `30Gi` if the image declares none |
| Example | `30Gi` |

Scratch volume allocated for the duration of the job. The volume stores the input file, intermediate processing files, and output files before they are uploaded to ODM. If the volume is too small for the data being processed, the job will fail.

**Sizing guidelines:**

| Input format | Recommended minimum |
|---|---|
| H5AD | ≥ 1.4 × size of the original attachment (GB) |
| 10x H5 | ≥ 4 × size of the original attachment (GB) |

10x H5 files require significantly more scratch space because the transformation converts them to H5AD internally before processing begins. For example, a 5 GB H5 file requires `volume_size` of at least `20Gi`.

---

## `memory_size`

| Property | Value |
|---|---|
| Type | string (Kubernetes quantity, e.g. `512Mi`) |
| Required | No |
| Default | the image's `default-memory-size` label, or `512Mi` if the image declares none |
| Example | `512Mi` |

Memory allocated to the transformation Pod. It is applied as both the Pod's memory request and limit, so it acts as a hard cap: a job that exceeds it is terminated and reported as `FAILED` with status reason `OOMKilled`. If that happens, increase `memory_size` or adjust the transformation configuration. The value must be a valid Kubernetes quantity greater than zero, otherwise the request is rejected with HTTP 422.
