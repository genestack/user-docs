---
diataxis: reference
tab: api-libraries
---

# SKOS dictionary reference

ODM supports dictionaries encoded in the [SKOS](https://www.w3.org/2009/08/skos-reference/skos.html) namespace. This feature organises terms in a hierarchical structure, enabling more advanced search capabilities within ODM.

Both RDF/XML and TURTLE serialisation formats are supported. The following predicates are recognised and used by ODM:

- `skos:broader`
- `skos:narrower`
- `skos:related`
- `skos:definition`
- `skos:exactMatch`

## Hierarchical search behaviour

When a SKOS dictionary is uploaded, ODM uses the hierarchical relationships to rank full-text search results. For example, if a dictionary defines `Brain` and `Cerebral cortex` with a `skos:broader`/`skos:narrower` relationship, searching for `Brain` will also surface studies that have `Cerebral cortex` as a value (with a lower score), and vice versa.

## Example dictionary formats

### TURTLE format

```ttl
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .

<http://vocabulary.boehringer-ingelheim.com/BodySystem/562>
 a skos:Concept ;
 skos:prefLabel "Cerebral cortex"@en .
 
<http://vocabulary.boehringer-ingelheim.com/BodySystem/104>
 a skos:Concept ;
 skos:narrower <http://vocabulary.boehringer-ingelheim.com/BodySystem/562> ;
 skos:prefLabel "Brain"@en .
 
<http://vocabulary.boehringer-ingelheim.com/BodySystem/562> skos:broader <http://vocabulary.boehringer-ingelheim.com/BodySystem/104> .
```

### RDF/XML format

```xml
<?xml version="1.0" encoding="utf-8" ?>
<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
         xmlns:skos="http://www.w3.org/2004/02/skos/core#">

    <skos:Concept rdf:about="http://vocabulary.boehringer-ingelheim.com/BodySystem/562">
        <skos:prefLabel xml:lang="en">Cerebral cortex</skos:prefLabel>
        <skos:broader>
            <skos:Concept rdf:about="http://vocabulary.boehringer-ingelheim.com/BodySystem/104">
                <skos:narrower rdf:resource="http://vocabulary.boehringer-ingelheim.com/BodySystem/562"/>
                <skos:prefLabel xml:lang="en">Brain</skos:prefLabel>
            </skos:Concept>
        </skos:broader>

    </skos:Concept>

</rdf:RDF>
```

Both examples define two concepts, `Brain` and `Cerebral cortex`, with a parent-child relationship.

## Related

- [About dictionaries and ontologies](about-dictionaries.md)
- [Load a custom ontology](load-a-custom-ontology.md)
