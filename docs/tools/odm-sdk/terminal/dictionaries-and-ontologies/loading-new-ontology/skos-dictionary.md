# Dictionaries in SKOS namespace

ODM also supports dictionaries in [SKOS](https://www.w3.org/2009/08/skos-reference/skos.html) namespace. This feature is
useful to organize terms in a hierarchical structure, which enables more advanced search capabilities. Both RDF/XML and
TURTLE formats of dictionaries are supported. Predicates `skos:broader`, `skos:narrower` `skos:related`,
`skos:definition`, and `skos:exactMatch` are recognized and utilized by ODM.

## Example of SKOS dictionary

Here are the examples of an artificial short SKOS dictionary in TURTLE and in RDF/XML formats:

<details>
<summary>TURTLE format</summary>

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

</details>

<details>
<summary>RDF/XML format</summary>

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

</details>

This dictionary defines two concepts: `Brain` and `Cerebral cortex`. Uploading this dictionary to ODM not only will
allow you
to assign a template attribute to have values `Brain` and `Cerebral cortex` but also will rate the full-text search
results
according to these relationships: if a user searches for `Brain`, the search results will also include studies that have
`Cerebral cortex` as a value, and vice versa: a search for `Cerebral cortex` will also include studies that have `Brain`
value, but with a lower score.
