---
diataxis: explanation
tab: overview
---

# Objects and groups

ODM distinguishes between two levels of data entity: objects and groups.

## Object

An object is an individual data entity within ODM: a single sample, a single study, a single library. Objects are the foundational units of the system. Management and query operations can target individual objects.

## Group

A group is a collection of related objects created during a single call.

!!! example
    All samples uploaded as part of one TSV file form a single sample group. If you later upload additional samples for the same study in a second file, those samples form a second, distinct sample group within the same study.

!!! warning "Limitation"
    ODM does not currently support merging groups. Uploading samples in two separate calls to the same study produces two separate sample groups in that study. Plan your uploads accordingly to keep related samples together.

The ODM APIs include endpoints that operate at both the group level (across a collection) and the object level (on individual entities).
