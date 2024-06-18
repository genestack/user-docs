# Supported File Formats

## Study metadata file

- [Test_1000g.study.tsv](https://s3.amazonaws.com/bio-test-data/odm/Test_1000g/Test_1000g.study.tsv), a tab-delimited file of the study attributes.

Study metadata can be supplied in a TSV format file. There is a limit of 255 characters for attribute names.

## Samples metadata file

- [Test_1000g.samples.tsv](https://s3.amazonaws.com/bio-test-data/odm/Test_1000g/Test_1000g.samples.tsv), a tab-delimited file of sample attributes.

Samples metadata is supplied in TSV format file. There needs to be a **Sample Source** column with values filled in, and a **Sample Source ID** column whose values match the column headers for samples in the GCT/VCF etc. files. The remaining columns are for metadata attributes and the names of these cannot be duplicated. There is a limit of 255 characters for attribute names.

| Sample Source        | Sample Source ID   | Species      | Sex   | Population   |
|----------------------|--------------------|--------------|-------|--------------|
| 1000 Genomes Project | HG00119            | Homo sapiens | M     | British      |
| 1001 Genomes Project | HG00121            | Homo sapiens | F     | British      |
| 1002 Genomes Project | HG00183            | Homo sapiens | M     | Finnish      |
| 1003 Genomes Project | HG00176            | Homo sapiens | F     | Finnish      |
> <a id="format-label"></a>

## Tabular data

In ODM, you can upload any tabular data that is formatted in **TSV (tab-separated values)**. As long as your file represents a data frame, ODM can import and index it. A data frame is a data structure that organizes data into a 2-dimensional table of rows and columns, similar to a spreadsheet.

Below, we break down the basics of the data frames you should be familiar with.

A data frame contains two main elements, especially in the context of Life Sciences:

- **Features**: These are the entities measured in an experiment (e.g., genes, proteins, metabolites, pathways, sales regions, etc.).
- **Measurements (or values)**: These are the actual values captured for each feature under different conditions (e.g., gene expression values, protein abundance, pathway activity, sales volume, etc.).

The first example below demonstrates the simplest and most popular type of data frame. Here, the features are genes listed in the first column, while the rest of the table contains measurements of gene expression for a number of samples. Each column represents a list of corresponding gene expression values in different samples (each column name represents a sample).

![image](doc-odm-user-guide/images/data-frame1.png)

In the second example, we present a more complex version of the data frame. Here, features are represented by more than one column containing additional information. Such columns might represent gene names, protein names, peptide sequences, PTM sites, pathway names, countries, etc. There can also be more than one type of measurements or calculated values for each feature in each sample. For example, for each gene (feature), we might have its expression level, quality flag, sequencing depth, Fold Change of differential expression, p-value, q-value per sample.

![image](doc-odm-user-guide/images/data-frame2.png)

This format provides a wide range of data types that can be uploaded and indexed in ODM.

However, the current **BETA** version has some limitations on the file content. Please ensure your file adheres to the following requirements:

- All columns must have names.
- All feature columns must be consecutive on the left side of the file. You need to explicitly specify the number of feature columns during the uploading process.
- **Recommended**: for a file with more than one feature column; to enable faster search when the file is uploaded, we recommend put the most importnat feature (any sort of ID, e.g., Gene Name, Protein Name, etc.) as the first column.
- Missing values: If your file intentionally contains missing data/values, ensure such values are coded as one of the following: “ “ (as a space symbol), empty (no symbol between two tabs), “NaN”, “null”, “N/A”, “NA”, “NA”, “filtered”, “Inf”, “-Inf”.
- The system automatically identifies all feature columns as either string value or numeric value columns. If a column that should be numeric contains at least one value with a non-numeric character (except for the missing value coded as indicated above), it will be considered a string value column, disabling the ranged search capabilities.
- Columns with measurements must contain only either numeric values or missing values (as specified above).
- If your file contains more than one measurement per Sample (Library or Preparation), e.g., Fold Change and P-value, the system will automatically recognize it using the following criteria:

> - The column name contains a special symbol (or their combination) as a separator between the Sample (Library or Preparation) name and the measurement type. If the column name contains more than one measurement separator (e.g., Sample1.p.value contains two dots), the first one will be used for separation.
> - The separator must be explicitly specified on data upload request either through API or GUI.
> - All columns must contain the separator.
> - All samples (libraries or preparations) must have the same types of measurements in the file. For example, if you have three samples and measure Intensity and Quality Pass, then your file must have six columns named: Sample1.Intensity, Sample1.QualityPass, Sample2.Intensity, Sample2.QualityPass, Sample3.Intensity, Sample3.QualityPass.

## Expression data in GCT (transcriptomics)

- [Test_1000g.gct](https://s3.amazonaws.com/bio-test-data/odm/Test_1000g/Test_1000g.gct), an example GCT file

- [Test_1000g.gct.tsv](https://s3.amazonaws.com/bio-test-data/odm/Test_1000g/Test_1000g.gct.tsv), an example expression metadata file

**GCT (Gene Cluster Text, .gct, .gct.gz, .gct.zip)** data files are supported by ODM. Gz and Zip archived versions are also accepted. This is a tab-delimited text file describing a gene expression dataset (e.g. microarray, RNA-seq data). GCT files are automatically recognised as Expression files in ODM.

![image](doc-odm-user-guide/images/gct-file.png)

The first line contains the file version and for gct format is always: #1.2

The second line shows the number of rows (‘2’) and columns (‘4’) of the expression matrix, which correspond to the number of features (eg genes) and samples respectively (ie excluding the identifier and description columns).

The third line is the matrix header row. The first column must be labelled ‘Name’ (case insensitive) and the second ‘Description’ (case insensitive), the following columns correspond to sample identifiers eg: ‘Bladder’ which must all be unique and a single word with no whitespace.

Below the header row is the data matrix. The first column contains the unique identifier values (e.g. Ensembl gene ID), the second column has a text description, the remaining columns contain values for the assay that was carried out (for example intensity of a sample gene expression measured in a specific tissue);
In the data matrix there is a row for each gene, and a column for each sample. The number of rows and columns should agree with the rows and columns specified on row two of the file.

Names and descriptions may contain spaces, but may not contain nothing - NA or NULL text strings should be used.

Intensity values in the data matrix can be left empty if they are missing.
To learn more take a look at the GCT [specification](https://software.broadinstitute.org/software/igv/GCT).

**.gct.tsv, gct.tsv.gz, gct.tsv.zip** files are tab delimited files that contain text metadata that describes the expression data, e.g. normalisation method, genome version.  The first row contains the key names, the second row contains the values.

| Expression Source    | Normalization Method   | Genome Version   |
|----------------------|------------------------|------------------|
| 1000 Genomes Project | RPKM                   | GRCh38.91        |

## Variant data (genomics)

- [Test_1000g.vcf](https://s3.amazonaws.com/bio-test-data/odm/Test_1000g/Test_1000g.vcf), a VCF file of variant data from multiple sequencing runs

- [Test_1000g.vcf.tsv](https://s3.amazonaws.com/bio-test-data/odm/Test_1000g/Test_1000g.vcf.tsv), a tab-separated file that describes the variant data (.gz and .zip also accepted)

ODM accepts **VCF files(Variant Call Format, .vcf, .vcf.gz, .vcf.zip)** for variant Data. VCF files are tab-delimited text files containing information about the position of genetic variations in the genome, and are produced as output of variant calling analysis. Gz and Zip archived versions are also accepted.

![image](doc-odm-user-guide/images/vcf-file.png)

### Basic structure of a VCF file

A VCF file contains three main parts:

- *Meta-information lines* (marked with “##”) — includes VCF format version number (##fileformat=VCFv4.3);
- *FILTER lines* (filters applied to the data, e.g. ##FILTER=<ID=LowQual, Description=”Low quality”>” ), FORMAT and INFO lines (explanations for abbreviations in the FORMAT and INFO columns of data lines,  e.g. “##FORMAT=<ID=GT,Number=1,Type=String,Description=”Genotype”>”);
- A vcf *Header line* (marked with “#”) — includes eight mandatory columns, namely #CHROM (chromosome), POS (genomic position), ID (identifier), REF (reference allele), ALT (alternate allele(s)), QUAL (Phred-scaled quality score for ALT), FILTER (filter status, where “PASS” means that this position has passed all filters), INFO (additional information described in the header lines, e.g. “DP=100”);
- *Data lines* — provide information about a genomic position of a variation and genotype information on samples for each position; each line represents a single variant, represented in the header.

#### Meta-information lines

File meta-information is included after the ## string and must be key=value pairs. It is strongly encouraged that information lines describing the INFO, FILTER and FORMAT entries used in the body of the VCF file be included in the meta-information section. Although they are optional, if these lines are present then they must be completely well-formed.

#### Header line syntax

The header line names the 8 fixed, mandatory columns. These columns are as follows:

1. #CHROM
2. POS
3. ID
4. REF
5. ALT
6. QUAL
7. FILTER
8. INFO

If genotype data is present in the file, these are followed by a FORMAT column header, then an arbitrary number of sample IDs. Duplicate sample IDs are not allowed. The header line is tab-delimited.

#### Data lines

Fixed fields:

There are 8 fixed fields per record. All data lines are tab-delimited. In all cases, missing values are specified with a dot (‘.’).

Fixed fields are:

1. **CHROM** - chromosome: An identifier from the reference genome or an angle-bracketed ID String (“<ID>”) pointing to a contig in the assembly file (cf. the ##assembly line in the header). All entries for a specific CHROM should form a contiguous block within the VCF file. The colon symbol (:) must be absent from all chromosome names to avoid parsing errors when dealing with breakends. (String, no white-space permitted, Required).
2. **POS** - position: The reference position, with the 1st base having position 1. Positions are sorted numerically, in increasing order, within each reference sequence CHROM. It is permitted to have multiple records with the same POS. Telomeres are indicated by using positions 0 or N+1, where N is the length of the corresponding chromosome or contig. (Integer, Required)
3. **ID** - identifier: Semi-colon separated list of unique identifiers where available. If this is a dbSNP variant it is encouraged to use the rs number(s). No identifier should be present in more than one data record. If there is no identifier available, then the missing value should be used. (String, no white-space or semi-colons permitted)
4. **REF** - reference base(s): Each base must be one of A,C,G,T,N (case insensitive). Multiple bases are permitted. The value in the POS field refers to the position of the first base in the String. For simple insertions and deletions in which either the REF or one of the ALT alleles would otherwise be null/empty, the REF and ALT Strings must include the base before the event (which must be reflected in the POS field), unless the event occurs at position 1 on the contig in which case it must include the base after the event; this padding base is not required (although it is permitted) for e.g. complex substitutions or other events where all alleles have at least one base represented in their Strings. If any of the ALT alleles is a symbolic allele (an angle-bracketed ID String “<ID>”) then the padding base is required and POS denotes the coordinate of the base preceding the polymorphism. Tools processing VCF files are not required to preserve case in the allele Strings. (String, Required).
5. **ALT** - alternate base(s): Comma separated list of alternate non-reference alleles. These alleles do not have to be called in any of the samples. Options are base Strings made up of the bases A,C,G,T,N,\*, (case insensitive) or an angle-bracketed ID String (“<ID>”) or a breakend replacement string as described in the section on breakends. The ‘\*’ allele is reserved to indicate that the allele is missing due to a upstream deletion. If there are no alternative alleles, then the missing value should be used. Tools processing VCF files are not required to preserve case in the allele String, except for IDs, which are case sensitive. (String; no whitespace, commas, or angle-brackets are permitted in the ID String itself)
6. **QUAL** - quality: Phred-scaled quality score for the assertion made in ALT. i.e. −10log10 prob(call in ALT is wrong). If ALT is ‘.’ (no variant) then this is −10log10 prob(variant), and if ALT is not ‘.’ this is −10log10 prob(no variant). If unknown, the missing value should be specified. (Numeric)
7. **FILTER** - filter status: PASS if this position has passed all filters, i.e., a call is made at this position. Otherwise, if the site has not passed all filters, a semicolon-separated list of codes for filters that fail. e.g. “q10;s50” might indicate that at this site the quality is below 10 and the number of samples with data is below 50% of the total number of samples. ‘0’ is reserved and should not be used as a filter String. If filters have not been applied, then this field should be set to the missing value. (String, no white-space or semi-colons permitted)
8. **INFO** - additional information: (String, no white-space, semi-colons, or equals-signs permitted; commas are permitted only as delimiters for lists of values) INFO fields are encoded as a semicolon-separated series of short keys with optional values in the format: <key>=<data>[,data]. Arbitrary keys are permitted, although the following sub-fields are reserved (albeit optional):

- **AA** : ancestral allele
- **AC** : allele count in genotypes, for each ALT allele, in the same order as listed
- **AF** : allele frequency for each ALT allele in the same order as listed: use this when estimated from primary data, not called genotypes
- **AN** : total number of alleles in called genotypes
- **BQ** : RMS base quality at this position
- **CIGAR** : cigar string describing how to align an alternate allele to the reference allele
- **DB** : dbSNP membership
- **DP** : combined depth across samples, e.g. DP=154
- **EFF** : functional effect of the genomic variant. Note the exact requirements for this field below.
- **END** : end position of the variant described in this record (for use with symbolic alleles)
- **H2** : membership in hapmap2
- **H3** : membership in hapmap3
- **MQ** : RMS mapping quality, e.g. MQ=52
- **MQ0** : Number of MAPQ == 0 reads covering this record
- **NS** : Number of samples with data
- **SB** : strand bias at this position
- **SOMATIC** : indicates that the record is a somatic mutation, for cancer genomics
- **VALIDATED** : validated by follow-up experiment
- **1000G** : membership in 1000 Genomes

**EFF** filed format specification. Each piece of data within the EFF field is separated by a pipe symbol **|**. If one piece of data is missing, two pipe symbols mark the absent data **||**. Below are the components expected in the EFF field, listed in the order they should appear:

- Variant Effect: An alphanumeric descriptor indicating the type of the variant effect. The rest of the fields follow in brackets **()**.
- Effect Impact: Classifies the impact level of the variant, options include HIGH, MODERATE, LOW, or MODIFIER.
- Functional Class: Indicates the functional class of the variant, with potential values being NONE, SILENT, MISSENSE, or NONSENSE.
- Codon Change / Distance: Provides information on codon changes or the distance measure, accepts any character excluding the pipe symbol **|**.
- Amino Acid Change: Indicates the changes in the amino acid, formatted similarly to the Codon Change / Distance field.
- Amino Acid Length (numeric): Specifies the length of the amino acid sequence with a numeric value.
- Gene Name: Denotes the gene’s name affected by the variant.
- Transcript BioType: States the biotype of the affected transcript.
- Gene Coding: Identifies whether the gene is CODING or NON_CODING.
- Transcript ID: Provides the ID associated with the transcript affected by the variant.
- Exon/Intron Rank (numeric): Assigns a numeric rank to the affected exon or intron.
- Genotype Number (numeric): Indicates the genotype number with a numeric value.

Examples:

EFF=INTRON(MODIFIER|||||HPS4|retained_intron|CODING|ENST00000485842|4|1)
EFF=STOP_GAINED(HIGH|NONSENSE|Cga/Tga|R241\*|721|HPS4|protein_coding|CODING|ENST00000398141|8|1)
EFF=STOP_GAINED(HIGH|NONSENSE|Cag/Tag|Q236\*|749|NOC2L||CODING|NM_015658||)
EFF=STOP_GAINED(HIGH|NONSENSE|Cag/Tag|Q141\*|642|KLHL17||CODING|NM_198317||)

The exact format of each INFO sub-field should be specified in the meta-information (as described above). Example for an INFO field: DP=154;MQ=52;H2. Keys without corresponding values are allowed in order to indicate group membership (e.g. H2 indicates the SNP is found in HapMap 2). It is not necessary to list all the properties that a site does NOT have, by e.g. H2=0. See below for additional reserved INFO sub-fields used to encode structural variants.

Genotype fields:

If genotype information is present, then the same types of data must be present for all samples.
First a **FORMAT** field is given specifying the data types and order (colon-separated alphanumeric String).
This is followed by one field per sample, with the colon-separated data in this field corresponding to the types
specified in the format. The first sub-field must always be the genotype (GT) if it is present.
There are no required sub-fields.
As with the INFO field, there are several common, reserved keywords that are standards across the community:

- **GT** : genotype, encoded as allele values separated by either of / or |. The allele values are 0 for the reference
allele (what is in the REF field), 1 for the first allele listed in ALT, 2 for the second allele list in ALT and
so on.
For diploid calls examples could be 0/1, 1 | 0, or 1/2, etc.
For haploid calls, e.g. on Y, male nonpseudoautosomal X, or mitochondrion, only one allele value should be given;
a triploid call might look like 0/0/1. If a call cannot be made for a sample at a given locus, ‘.’ should be specified
for each missing allele in the GT field (for example ‘./.’ for a diploid genotype and ‘.’ for haploid genotype).

The meanings of the separators are as follows (see the PS field below for more details on incorporating phasing
information into the genotypes):

- **/** : genotype unphased
- **|** : genotype phased
- **DP** : read depth at this position for this sample (Integer)
- **FT** : sample genotype filter indicating if this genotype was “called” (similar in concept to the FILTER field). Again, use PASS to indicate that all filters have been passed, a semi-colon separated list of codes for filters that fail, or ‘.’ to indicate that filters have not been applied. These values should be described in the metainformation in the same way as FILTERs (String, no white-space or semi-colons permitted)
- **GL** : genotype likelihoods comprised of comma separated floating point log10-scaled likelihoods for all possible genotypes given the set of alleles defined in the REF and ALT fields. In presence of the GT field the same ploidy is expected and the canonical order is used; without GT field, diploidy is assumed. If A is the allele in REF and B,C,… are the alleles as ordered in ALT, the ordering of genotypes for the likelihoods is given by: F(j/k) = (k\*(k+1)/2)+j. In other words, for biallelic sites the ordering is: AA,AB,BB; for triallelic sites the ordering is: AA,AB,BB,AC,BC,CC, etc. For example: GT:GL 0/1:-323.03,-99.29,-802.53 (Floats)
- **GLE** : genotype likelihoods of heterogeneous ploidy, used in presence of uncertain copy number. For example: GLE=0:-75.22,1:-223.42,0/0:-323.03,1/0:-99.29,1/1:-802.53 (String)
- **PL** : the phred-scaled genotype likelihoods rounded to the closest integer (and otherwise defined precisely as the GL field) (Integers)
- **GP** : the phred-scaled genotype posterior probabilities (and otherwise defined precisely as the GL field); intended to store imputed genotype probabilities (Floats)
- **GQ** : conditional genotype quality, encoded as a phred quality −10log10 p(genotype call is wrong, conditioned on the site’s being variant) (Integer)
- **HQ** : haplotype qualities, two comma separated phred qualities (Integers)
- **PS** : phase set. A phase set is defined as a set of phased genotypes to which this genotype belongs. Phased genotypes for an individual that are on the same chromosome and have the same PS value are in the same phased set. A phase set specifies multi-marker haplotypes for the phased genotypes in the set. All phased genotypes that do not contain a PS subfield are assumed to belong to the same phased set. If the genotype in the GT field is unphased, the corresponding PS field is ignored. The recommended convention is to use the position of the first variant in the set as the PS identifier (although this is not required). (Non-negative 32-bit Integer)
- **PQ** : phasing quality, the phred-scaled probability that alleles are ordered incorrectly in a heterozygote (against all other members in the phase set). We note that we have not yet included the specific measure for precisely defining “phasing quality”; our intention for now is simply to reserve the PQ tag for future use as a measure of phasing quality. (Integer)
- **EC** : comma separated list of expected alternate allele counts for each alternate allele in the same order as listed in the ALT field (typically used in association analyses) (Integers)
- **MQ** : RMS mapping quality, similar to the version in the INFO field. (Integer)

If any of the fields is missing, it is replaced with the missing value. For example if the FORMAT is GT:GQ:DP:HQ then 0 | 0 : . : 23 : 23, 34 indicates that GQ is missing. Trailing fields can be dropped (with the exception of the GT field, which should always be present if specified in the FORMAT field).

To learn more take a look at the VCF [specification](https://software.broadinstitute.org/software/igv/GCT).

<!-- Flow cytometry data
------------------- -->
<!-- Flow cytometry data can be stored with data in a **FACS (.facs)** file and metadata in TXT file. -->
<!-- Data files
********** -->
<!-- A .facs tab-delimited file. The first columns describes features; subsequent columns correspond to samples, one per column. -->
<!-- .. image:: images/facs-signals.png
:scale: 75 %
:align: center -->
<!-- Each row in the file is one feature: -->
<!-- Cytokine MFI —  just one protein identifier. MFI = Mean/Median Fluorescence Intensity.
Cell counts — a combination of cell markers (=genes/proteins) and modifiers: positive (+), negative (-), high(hi), low(lo), intermediate(int).
MFI_CellMarker — like counts, but the intensity of one particular cell marker on a given cell subpopulation defines as for counts is measured.
Percentage — like counts, but the percentage of cells positive/negative for a particular cell marker relative to the parent population as defined like for cell counts is provided. -->
<!-- Cell populations can have nicknames, e.g. CD45+CD3+CD4+FOXP3+ (’MarkerCombination’) cells are also called Tregs. -->
<!-- Metadata file
************* -->
<!-- Metadata (annotation) about FACS data samples can be supplied as a tab-delimited table text file. Each row is one sample, each column is one property type (the first column contains unique identifiers of each sample). -->
<!-- .. image:: images/facs-annot.png
:scale: 55 %
:align: center -->

## Cross-reference mapping file

A cross-reference mapping file can be imported. This is a TSV file consisting of two columns. The first row must contain the headers TXNAME and GENEID, and the first column must be the transcript IDs which must be unique. The file needs to be hosted at an HTTPS location accessible to ODM.

| TXNAME            | GENEID            |
|-------------------|-------------------|
| ENST00000438176.2 | ENSG00000231103.2 |
| ENST00000445563.2 | ENSG00000226662.2 |

## Libraries file

- [Test_RM.libraries.tsv](https://bio-test-data.s3.amazonaws.com/Research_Model_BR-205/Test_RM.libraries.tsv), a a TSV file with information about sample preparations

Libraries metadata is a TSV file with information about how samples were prepared. It contains data related to the quality of samples, barcodes and library properties (single-end vs pair-end). Each sample can have more than 1 corresponding library. Multiple samples can be pooled into the same library, e.g. pooling female and male samples to remove gender-specific signals in the sequencing output (unrelated to multiplexing of libraries with barcodes). **Sample Source ID** and **Library ID** are required headings.

| Sample Source ID   |   Library ID | Library barcode   | Library pool   |
|--------------------|--------------|-------------------|----------------|
| 1                  |            1 | A                 |                |
| 2                  |            2 | B                 |                |
| 1|2                |            3 | A + B             | 1|2            |

## Preparations file

- [Test_RM.preparations.tsv](https://bio-test-data.s3.amazonaws.com/Research_Model_BR-205/Test_RM.preparations.tsv), a TSV file with information about sample preparations

Preparations metadata follows the same format as libraries above, but containing proteomics specific metadata. **Sample Source ID** and **Preparation ID** are required headings.
