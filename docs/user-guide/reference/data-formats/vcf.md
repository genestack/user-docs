# VCF (Variants)

VCF (Variant Call Format) is the standard tab-delimited format for storing genetic variation data. VCF files are typically produced as output from variant-calling pipelines and contain information about sequence variations including SNPs, insertions, deletions, and structural variants.

ODM imports VCF files as Variant objects, indexes their content, and links them to sample metadata for downstream analysis and cross-sample comparison.

**Example files:**

- [Test_1000g.vcf](https://s3.amazonaws.com/bio-test-data/odm/Test_1000g/Test_1000g.vcf) — VCF file with variant data from multiple sequencing runs
- [Test_1000g.vcf.tsv](https://s3.amazonaws.com/bio-test-data/odm/Test_1000g/Test_1000g.vcf.tsv) — companion TSV describing the variant dataset

---

## Supported file extensions

| Extension | Description |
|---|---|
| `.vcf` | Standard uncompressed VCF file |
| `.vcf.gz`, `.vcf.zip` | Compressed VCF file (available via API) |

---

## File structure

![VCF file structure](../../doc-odm-user-guide/doc-odm-user-guide/images/vcf-file.png)

A VCF file consists of three main sections:

### 1. Meta-information lines (`##`)

Lines beginning with `##` contain key=value pairs describing the file. It is strongly encouraged (though not required) to include `INFO`, `FILTER`, and `FORMAT` description lines in this section. If present, they must be completely well-formed.

Example entries:

```
##fileformat=VCFv4.3
##FILTER=<ID=LowQual,Description="Low quality">
##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
```

### 2. Header line (`#`)

A single tab-delimited line defining the 8 mandatory fixed columns, optionally followed by `FORMAT` and one column per sample:

| # | Column | Description |
|---|--------|-------------|
| 1 | `CHROM` | Chromosome identifier |
| 2 | `POS` | Genomic position (1-based) |
| 3 | `ID` | Variant identifier (e.g., dbSNP rs number); `.` if absent |
| 4 | `REF` | Reference allele(s) |
| 5 | `ALT` | Alternate allele(s), comma-separated |
| 6 | `QUAL` | Phred-scaled quality score |
| 7 | `FILTER` | Filter status: `PASS` or semicolon-separated list of failed filters |
| 8 | `INFO` | Additional annotations (semicolon-separated key=value pairs) |

If genotype data is present, a `FORMAT` column follows, then one column per sample. Duplicate sample IDs are not allowed.

### 3. Data lines

Each data line represents one variant. All fields are tab-delimited; missing values are indicated with `.`.

---

## Fixed field specifications

### CHROM
Chromosome identifier from the reference genome. Must not contain a colon (`:`). All records for the same `CHROM` must form a contiguous block. (String, no whitespace, required)

### POS
Reference position; 1-based, sorted numerically within each `CHROM`. Multiple records may share the same `POS`. Telomeres are represented by position 0 or N+1. (Integer, required)

### ID
Semicolon-separated list of unique identifiers. No identifier may appear in more than one data record. Use `.` for missing. (String, no whitespace or semicolons)

### REF
Reference base(s): A, C, G, T, or N (case-insensitive). For simple indels, the base before (or after at position 1) the event must be included. (String, required)

### ALT
Comma-separated list of alternate alleles. Bases A, C, G, T, N, `*` (case-insensitive), angle-bracketed symbolic IDs (`<ID>`), or breakend strings. Use `.` if no alternate allele. (String, no whitespace, commas, or angle-brackets in ID strings)

### QUAL
Phred-scaled quality score for the ALT assertion: −10 log10(P(call is wrong)). Use `.` if unknown. (Numeric)

### FILTER
`PASS` if all filters are passed; otherwise a semicolon-separated list of failed filter codes (e.g., `q10;s50`). Use `.` if filters have not been applied. (String, no whitespace or semicolons)

### INFO
Semicolon-separated key=value annotations. Reserved sub-fields include:

| Key | Description |
|-----|-------------|
| `AA` | Ancestral allele |
| `AC` | Allele count in genotypes for each ALT allele |
| `AF` | Allele frequency for each ALT allele (estimated from primary data) |
| `AN` | Total number of alleles in called genotypes |
| `BQ` | RMS base quality at this position |
| `CIGAR` | CIGAR string for aligning alternate to reference |
| `DB` | dbSNP membership |
| `DP` | Combined read depth across samples (e.g., `DP=154`) |
| `EFF` | Functional effect of the variant (see below) |
| `END` | End position for symbolic alleles |
| `H2` | HapMap2 membership |
| `H3` | HapMap3 membership |
| `MQ` | RMS mapping quality (e.g., `MQ=52`) |
| `MQ0` | Number of reads with MAPQ=0 |
| `NS` | Number of samples with data |
| `SB` | Strand bias |
| `SOMATIC` | Somatic mutation flag (cancer genomics) |
| `VALIDATED` | Validated by follow-up experiment |
| `1000G` | 1000 Genomes membership |

Keys without values indicate group membership (e.g., `H2` means the SNP is in HapMap 2).

#### EFF field format

The `EFF` INFO sub-field describes the functional effect of a variant. Components are pipe-separated (`|`); absent data is represented by `||`:

```
EFF=<Effect>(<Impact>|<FunctionalClass>|<CodonChange>|<AminoAcidChange>|<AALength>|<GeneName>|<TranscriptBioType>|<GeneCoding>|<TranscriptID>|<ExonRank>|<GenotypeNumber>)
```

| Component | Values |
|-----------|--------|
| Variant Effect | Alphanumeric descriptor (e.g., `INTRON`, `STOP_GAINED`) |
| Effect Impact | `HIGH`, `MODERATE`, `LOW`, or `MODIFIER` |
| Functional Class | `NONE`, `SILENT`, `MISSENSE`, or `NONSENSE` |
| Codon Change / Distance | Any characters except `|` |
| Amino Acid Change | Any characters except `|` |
| Amino Acid Length | Numeric |
| Gene Name | Gene identifier |
| Transcript BioType | Biotype of affected transcript |
| Gene Coding | `CODING` or `NON_CODING` |
| Transcript ID | Transcript identifier |
| Exon/Intron Rank | Numeric |
| Genotype Number | Numeric |

Examples:

```
EFF=INTRON(MODIFIER|||||HPS4|retained_intron|CODING|ENST00000485842|4|1)
EFF=STOP_GAINED(HIGH|NONSENSE|Cga/Tga|R241*|721|HPS4|protein_coding|CODING|ENST00000398141|8|1)
```

---

## Genotype fields

When genotype data is present, the `FORMAT` column specifies a colon-separated list of data types that applies to every sample column. The first sub-field must always be `GT` if genotype is included.

Common reserved genotype keywords:

| Key | Description |
|-----|-------------|
| `GT` | Genotype encoded as allele values separated by `/` (unphased) or `|` (phased). `0` = REF, `1` = first ALT, etc. Use `.` for missing alleles. |
| `DP` | Read depth at this position for this sample (Integer) |
| `FT` | Sample genotype filter: `PASS`, semicolon-separated failed filters, or `.` |
| `GL` | Comma-separated log10-scaled genotype likelihoods (Floats) |
| `GLE` | Genotype likelihoods for heterogeneous ploidy (String) |
| `PL` | Phred-scaled genotype likelihoods, rounded to integer |
| `GP` | Phred-scaled genotype posterior probabilities (Floats) |
| `GQ` | Conditional genotype quality, phred-scaled (Integer) |
| `HQ` | Haplotype qualities, two comma-separated phred values (Integers) |
| `PS` | Phase set identifier; conventionally the position of the first variant in the set |
| `PQ` | Phasing quality, phred-scaled (Integer) |
| `EC` | Expected alternate allele counts for each ALT allele (Integers) |
| `MQ` | RMS mapping quality for this sample (Integer) |

Trailing fields may be omitted, except `GT` which must be present if specified in `FORMAT`.

---

## How ODM uses VCF files

- VCF files are indexed on import, enabling search and filtering by chromosome, position, variant effect, and other INFO fields via `GET /api/v1/as-user/omics/variant/data`.
- Variant data can be integrated with sample metadata for cross-sample comparison and variant distribution analysis.
- Sample column identifiers in the VCF header are matched against `Sample Source ID` values in the linked Samples metadata file.

For a full reference to the VCF specification, see the [SAMtools/hts-specs documentation](https://samtools.github.io/hts-specs/).
