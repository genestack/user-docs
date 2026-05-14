# How data is organised in ODM

ODM structures experimental data as a hierarchy of related entities. This hierarchy is not arbitrary — it reflects the real-world flow from a research question down to raw measurements, and it is what makes cross-study discovery possible.

## The Study → Sample → Library → Data hierarchy

At the top sits the **Study**, which defines the context of an experiment: its aim, statistical design, and provenance. Everything else in ODM belongs to a study.

Below the study, **Samples metadata** captures the biological attributes of the specimens involved — tissue type, disease status, treatment conditions, organism, and so on. This is the metadata that researchers typically want to filter on when searching across studies.

**Libraries and Preparations** are optional intermediaries that describe sample preparation steps and sequencing libraries. Not all experiment types require this level of detail, but when it matters — for example in single-cell or multi-omic studies — it allows the experimental protocol to be represented faithfully.

**Data metadata** describes how the data itself was processed: normalization techniques, instrumentation, and the type of processed data produced (TSV, VCF, and so on). Keeping this separate from sample metadata means that the same biological sample can be associated with multiple data processing pipelines without duplicating biological information.

Finally, **Data** is the actual omics measurements: expression matrices, variant calls, flow cytometry readouts, and similar.

**Cross-references** sit outside the main hierarchy but are linked to data files. They provide mappings between identifier namespaces — for example, mapping transcript IDs to gene IDs — so that the same data can be queried at different levels of biological resolution.

This layered design means that a query can start at any level. You can search for all studies from a given tissue, or all expression datasets that used a particular normalization method, without needing to know in advance which studies are relevant.

## Objects vs. Groups

### Objects

An **Object** is an individual data entity within ODM: a single sample, a single study, a single library. Objects are the foundational units of data. They can be queried, updated, and managed individually through the ODM API.

### Groups

A **Group** is a collection of related objects that were created together in a single API call — for example, all the samples uploaded from one metadata table file. Groups exist because batch operations are the norm in large-scale data management: importing 500 samples one at a time would be impractical.

!!! example
    **Samples uploaded as part of one table file** constitute a group. If you upload an initial set of samples and then upload additional samples in a separate file to the same study, these will form two distinct sample groups within that study.

!!! warning "Limitation"
    ODM does not currently support merging groups. If you upload 10 samples from one file and later upload another 5 samples to the same study, the study will contain two separate sample groups. Plan your uploads accordingly — split imports create permanent structural divisions.

The distinction between objects and groups surfaces in the ODM API: some endpoints operate on an entire group (returning or updating all objects within it at once), while others operate on individual objects. Understanding which level an endpoint targets is important when writing integrations or automation against the API.

## See also

- [`../reference/data-formats/`](../reference/data-formats/) — format-specific details for each data type ODM accepts
- [`../how-to/studies-import/create-a-study.md`](../how-to/studies-import/create-a-study.md) — step-by-step instructions for creating a study in ODM
