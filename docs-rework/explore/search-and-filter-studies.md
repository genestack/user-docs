---
diataxis: how-to
tab: explore
---

# Find specific studies

The Study Browser displays all studies visible to you. Use the search bar and facet filters together to narrow down the list to exactly the studies you need.

## Search by keyword or metadata

Type your term into the search bar at the top of the Study Browser to search by study name, accession number, sample or signal object, or any text in any metadata field across all studies visible to you. With no term entered, the Study Browser lists every accessible study by date, newest first.

As you type, ODM autocompletes your term against the dictionaries and ontologies loaded into the instance and matches synonyms automatically. Searching for "human" also returns studies annotated with "Homo sapiens", and the reverse holds too.

To narrow a search further, refine your term in any of these ways:

- **Wildcards**: `?` matches any single character, so `c?ncer` matches `cancer`; `*` matches any number of characters, so `*ale` matches both `male` and `female`.
- **Exact phrase**: wrap a term in quotation marks, as in `"single cell"`, to match the phrase exactly.
- **Operators**: join terms with `AND` to require both, or prefix a term with `NOT` to exclude it. Terms are combined with `OR` by default.
- **Extend query**: when your term matches an ontology term that has child terms, enable the **Extend query** toggle to include results for all of those child terms. This is available when the total number of terms, including synonyms, is fewer than 30,000.

## Narrow results by metadata attribute

The left panel displays facets (filters based on metadata fields such as Data Class and Organism). Click a facet value to restrict results to studies that have that value. You can combine multiple facet selections with a search term to narrow results further.

Which facets are available depends on your ODM instance's configuration. Administrators can add, remove, and reorder facets; see [Configure facets](../admin/configure-facets.md) for details.

**Metadata validity facet**: use this facet to filter for studies with fully valid metadata or for studies with invalid metadata, that is, metadata that does not conform to the applied template. See [About validation and curation](../contribute/curate-metadata/about-validation-and-curation.md) for what valid and invalid metadata means.

## Going further

- For orientation on the Study Browser interface: [Study Browser](../overview/navigating-the-ui/study-browser.md)
- To search and query studies via the API: [Search studies](../odm-api/explore/search-studies.md)
