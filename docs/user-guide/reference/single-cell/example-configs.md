# Single-Cell Transformation: Example Configurations

This page provides annotated transformation configuration files for curated public single-cell datasets. Each configuration has been pre-validated against its dataset and can be used directly as a starting point when importing or transforming single-cell data in ODM.

---

## Configuration–dataset mapping

Each curated dataset is paired with a tested transformation configuration. Use the table below to identify which configuration to apply when running a transformation job.

> Because these configurations have been pre-validated against their respective datasets, the dry-run step can be skipped when transforming the curated catalogue.

| Configuration | Datasets |
|---|---|
| [`aggregated_config_1`](#aggregated_config_1) | HeartDiversityTucker10x, GSE292928, GSE192740_human, GSE192740_mouse, GSE148434, SCP1303 |
| [`aggregated_config_2`](#aggregated_config_2) | GSE198623_human, GSE198623_pig |
| [`aggregated_config_3`](#aggregated_config_3) | GSE148073, FibroticLiverWatsonMERFISH |
| [`GSE156793`](#gse156793) | GSE156793 |
| [`GSE165045`](#gse165045) | GSE165045 |

---

## Configuration files

### aggregated_config_1

**Applies to:** HeartDiversityTucker10x, GSE292928, GSE192740_human, GSE192740_mouse, GSE148434, SCP1303

**Download:** [aggregated_config_1.json](../../doc-odm-user-guide/doc-odm-user-guide/extras/aggregated_config_1.json)

This configuration covers a broad set of cardiovascular, metabolic, and neurodegenerative disease datasets captured with 10x Genomics chemistry. It handles the common AnnData structure shared across these studies and maps cell-type annotations, UMAP embeddings, and gene expression layers to their ODM equivalents.

---

### aggregated_config_2

**Applies to:** GSE198623_human, GSE198623_pig

**Download:** [aggregated_config_2.json](../../doc-odm-user-guide/doc-odm-user-guide/extras/aggregated_config_2.json)

This configuration handles the multi-species (human and pig) metabolic disease dataset GSE198623. Each species is uploaded as a separate H5AD file within a single study; the configuration normalises field names across both species-specific files.

---

### aggregated_config_3

**Applies to:** GSE148073, FibroticLiverWatsonMERFISH

**Download:** [aggregated_config_3.json](../../doc-odm-user-guide/doc-odm-user-guide/extras/aggregated_config_3.json)

This configuration targets metabolic disease and spatial transcriptomics (MERFISH) datasets. It accommodates the distinct obs/var layout used in the FibroticLiverWatsonMERFISH AnnData file alongside the conventional single-cell structure of GSE148073.

---

### GSE156793

**Applies to:** GSE156793 (healthy cell atlas, multi-organ)

**Download:** [GSE156793.json](../../doc-odm-user-guide/doc-odm-user-guide/extras/GSE156793.json)

Dataset-specific configuration for the GSE156793 all-organ annotated single-cell atlas. This config is tailored to the annotation schema and embedding keys used in `GSE156793_all_organs_annotated_with_genes.h5ad`.

---

### GSE165045

**Applies to:** GSE165045 (inflammatory disease, TCR)

**Download:** [GSE165045.json](../../doc-odm-user-guide/doc-odm-user-guide/extras/GSE165045.json)

Dataset-specific configuration for GSE165045, a merged single-cell dataset with T-cell receptor (TCR) data. Handles the combined cell and TCR annotation fields present in `GSE165045_merged_with_TCR.h5ad`.

---

## Import commands

The commands below load each curated single-cell dataset into an ODM instance using the `odm-import-data` CLI. Each command uploads study and sample/library metadata alongside the H5AD attachment, ready for transformation.

Replace `<HOST>`, `<TOKEN>`, and `<TEMPLATE>` with your ODM instance URL, API token, and template ID before running. Commands can be run independently and in any order.

Recommended template: [Public dataset template](https://bio-test-data.s3.us-east-1.amazonaws.com/demo_materials/templates/public_studies_template_demo.json)

> Two datasets — **GSE192740** and **GSE198623** — contain multiple species and upload two H5AD files (human + mouse, or human + pig) within a single command.

### HeartDiversityTucker10x

```bash
odm-import-data \
  --server <HOST> \
  --token <TOKEN> \
  --study https://bio-test-data.s3.us-east-1.amazonaws.com/demo_materials/non_onco/single_cell/cardiovascular_diseases/HeartDiversityTucker10x/study.tsv \
  --samples https://bio-test-data.s3.us-east-1.amazonaws.com/demo_materials/non_onco/single_cell/cardiovascular_diseases/HeartDiversityTucker10x/samples.tsv \
  --libraries https://bio-test-data.s3.us-east-1.amazonaws.com/demo_materials/non_onco/single_cell/cardiovascular_diseases/HeartDiversityTucker10x/libraries.tsv \
  -fl https://bio-test-data.s3.us-east-1.amazonaws.com/demo_materials/non_onco/single_cell/cardiovascular_diseases/HeartDiversityTucker10x/healthy_human_4chamber_map_unnormalized_V4.h5ad \
  -flm https://bio-test-data.s3.us-east-1.amazonaws.com/demo_materials/non_onco/single_cell/cardiovascular_diseases/HeartDiversityTucker10x/data.tsv \
  -dc 'Single-cell transcriptomics' \
  --template <TEMPLATE> \
  --allow-duplicates
```

### SCP1303

```bash
odm-import-data \
  --server <HOST> \
  --token <TOKEN> \
  --study https://bio-test-data.s3.us-east-1.amazonaws.com/demo_materials/non_onco/single_cell/cardiovascular_diseases/SCP1303/study.tsv \
  --samples https://bio-test-data.s3.us-east-1.amazonaws.com/demo_materials/non_onco/single_cell/cardiovascular_diseases/SCP1303/samples.tsv \
  --libraries https://bio-test-data.s3.us-east-1.amazonaws.com/demo_materials/non_onco/single_cell/cardiovascular_diseases/SCP1303/libraries.tsv \
  -fl https://bio-test-data.s3.us-east-1.amazonaws.com/demo_materials/non_onco/single_cell/cardiovascular_diseases/SCP1303/human_dcm_hcm_scportal_03.17.2022.h5ad \
  -flm https://bio-test-data.s3.us-east-1.amazonaws.com/demo_materials/non_onco/single_cell/cardiovascular_diseases/SCP1303/data.tsv \
  -dc 'Single-cell transcriptomics' \
  --template <TEMPLATE> \
  --allow-duplicates
```

### GSE156793

```bash
odm-import-data \
  --server <HOST> \
  --token <TOKEN> \
  --study https://bio-test-data.s3.us-east-1.amazonaws.com/demo_materials/non_onco/single_cell/healthy_cell_atlases/GSE156793/study.tsv \
  --samples https://bio-test-data.s3.us-east-1.amazonaws.com/demo_materials/non_onco/single_cell/healthy_cell_atlases/GSE156793/samples.tsv \
  --libraries https://bio-test-data.s3.us-east-1.amazonaws.com/demo_materials/non_onco/single_cell/healthy_cell_atlases/GSE156793/libraries.tsv \
  -fl https://bio-test-data.s3.us-east-1.amazonaws.com/demo_materials/non_onco/single_cell/healthy_cell_atlases/GSE156793/GSE156793_all_organs_annotated_with_genes.h5ad \
  -flm https://bio-test-data.s3.us-east-1.amazonaws.com/demo_materials/non_onco/single_cell/healthy_cell_atlases/GSE156793/data.tsv \
  -dc 'Single-cell transcriptomics' \
  --template <TEMPLATE> \
  --allow-duplicates
```

### FibroticLiverWatsonMERFISH

```bash
odm-import-data \
  --server <HOST> \
  --token <TOKEN> \
  --study https://bio-test-data.s3.us-east-1.amazonaws.com/demo_materials/non_onco/single_cell/inflammatory_diseases/FibroticLiverWatsonMERFISH/study.tsv \
  --samples https://bio-test-data.s3.us-east-1.amazonaws.com/demo_materials/non_onco/single_cell/inflammatory_diseases/FibroticLiverWatsonMERFISH/samples.tsv \
  --libraries https://bio-test-data.s3.us-east-1.amazonaws.com/demo_materials/non_onco/single_cell/inflammatory_diseases/FibroticLiverWatsonMERFISH/libraries.tsv \
  -fl https://bio-test-data.s3.us-east-1.amazonaws.com/demo_materials/non_onco/single_cell/inflammatory_diseases/FibroticLiverWatsonMERFISH/GSE210077_adata_healthy_diseased_nucseq_sparse.h5ad \
  -flm https://bio-test-data.s3.us-east-1.amazonaws.com/demo_materials/non_onco/single_cell/inflammatory_diseases/FibroticLiverWatsonMERFISH/data.tsv \
  -dc 'Single-cell transcriptomics' \
  --template <TEMPLATE> \
  --allow-duplicates
```

### GSE165045

```bash
odm-import-data \
  --server <HOST> \
  --token <TOKEN> \
  --study https://bio-test-data.s3.us-east-1.amazonaws.com/demo_materials/non_onco/single_cell/inflammatory_diseases/GSE165045/study.tsv \
  --samples https://bio-test-data.s3.us-east-1.amazonaws.com/demo_materials/non_onco/single_cell/inflammatory_diseases/GSE165045/samples.tsv \
  --libraries https://bio-test-data.s3.us-east-1.amazonaws.com/demo_materials/non_onco/single_cell/inflammatory_diseases/GSE165045/libraries.tsv \
  -fl https://bio-test-data.s3.us-east-1.amazonaws.com/demo_materials/non_onco/single_cell/inflammatory_diseases/GSE165045/GSE165045_merged_with_TCR.h5ad \
  -flm https://bio-test-data.s3.us-east-1.amazonaws.com/demo_materials/non_onco/single_cell/inflammatory_diseases/GSE165045/data.tsv \
  -dc 'Single-cell transcriptomics' \
  --template <TEMPLATE> \
  --allow-duplicates
```

### GSE148073

```bash
odm-import-data \
  --server <HOST> \
  --token <TOKEN> \
  --study https://bio-test-data.s3.us-east-1.amazonaws.com/demo_materials/non_onco/single_cell/metabolic_diseases/GSE148073/study.tsv \
  --samples https://bio-test-data.s3.us-east-1.amazonaws.com/demo_materials/non_onco/single_cell/metabolic_diseases/GSE148073/samples.tsv \
  --libraries https://bio-test-data.s3.us-east-1.amazonaws.com/demo_materials/non_onco/single_cell/metabolic_diseases/GSE148073/libraries.tsv \
  -fl https://bio-test-data.s3.us-east-1.amazonaws.com/demo_materials/non_onco/single_cell/metabolic_diseases/GSE148073/GSE148073_merged_data_new.h5ad \
  -flm https://bio-test-data.s3.us-east-1.amazonaws.com/demo_materials/non_onco/single_cell/metabolic_diseases/GSE148073/data.tsv \
  -dc 'Single-cell transcriptomics' \
  --template <TEMPLATE> \
  --allow-duplicates
```

### GSE192740 (human + mouse)

```bash
odm-import-data \
  --server <HOST> \
  --token <TOKEN> \
  --study https://bio-test-data.s3.us-east-1.amazonaws.com/demo_materials/non_onco/single_cell/metabolic_diseases/GSE192740/study.tsv \
  --samples https://bio-test-data.s3.us-east-1.amazonaws.com/demo_materials/non_onco/single_cell/metabolic_diseases/GSE192740/samples.tsv \
  --libraries https://bio-test-data.s3.us-east-1.amazonaws.com/demo_materials/non_onco/single_cell/metabolic_diseases/GSE192740/libraries.tsv \
  -fl https://bio-test-data.s3.us-east-1.amazonaws.com/demo_materials/non_onco/single_cell/metabolic_diseases/GSE192740/GSE192740_human_combined_sparse.h5ad \
  -flm https://bio-test-data.s3.us-east-1.amazonaws.com/demo_materials/non_onco/single_cell/metabolic_diseases/GSE192740/data_human.tsv \
  -dc 'Single-cell transcriptomics' \
  -fl https://bio-test-data.s3.us-east-1.amazonaws.com/demo_materials/non_onco/single_cell/metabolic_diseases/GSE192740/GSE192740_mouse_combined_sparse.h5ad \
  -flm https://bio-test-data.s3.us-east-1.amazonaws.com/demo_materials/non_onco/single_cell/metabolic_diseases/GSE192740/data_mouse.tsv \
  -dc 'Single-cell transcriptomics' \
  --template <TEMPLATE> \
  --allow-duplicates
```

### GSE198623 (human + pig)

```bash
odm-import-data \
  --server <HOST> \
  --token <TOKEN> \
  --study https://bio-test-data.s3.us-east-1.amazonaws.com/demo_materials/non_onco/single_cell/metabolic_diseases/GSE198623/study.tsv \
  --samples https://bio-test-data.s3.us-east-1.amazonaws.com/demo_materials/non_onco/single_cell/metabolic_diseases/GSE198623/samples.tsv \
  --libraries https://bio-test-data.s3.us-east-1.amazonaws.com/demo_materials/non_onco/single_cell/metabolic_diseases/GSE198623/libraries.tsv \
  -fl https://bio-test-data.s3.us-east-1.amazonaws.com/demo_materials/non_onco/single_cell/metabolic_diseases/GSE198623/GSE198623_human_processed.h5ad \
  -flm https://bio-test-data.s3.us-east-1.amazonaws.com/demo_materials/non_onco/single_cell/metabolic_diseases/GSE198623/data_human.tsv \
  -dc 'Single-cell transcriptomics' \
  -fl https://bio-test-data.s3.us-east-1.amazonaws.com/demo_materials/non_onco/single_cell/metabolic_diseases/GSE198623/GSE198623_pig_processed.h5ad \
  -flm https://bio-test-data.s3.us-east-1.amazonaws.com/demo_materials/non_onco/single_cell/metabolic_diseases/GSE198623/data_pig.tsv \
  -dc 'Single-cell transcriptomics' \
  --template <TEMPLATE> \
  --allow-duplicates
```

### GSE292928

```bash
odm-import-data \
  --server <HOST> \
  --token <TOKEN> \
  --study https://bio-test-data.s3.us-east-1.amazonaws.com/demo_materials/non_onco/single_cell/metabolic_diseases/GSE292928/study.tsv \
  --samples https://bio-test-data.s3.us-east-1.amazonaws.com/demo_materials/non_onco/single_cell/metabolic_diseases/GSE292928/samples.tsv \
  --libraries https://bio-test-data.s3.us-east-1.amazonaws.com/demo_materials/non_onco/single_cell/metabolic_diseases/GSE292928/libraries.tsv \
  -fl https://bio-test-data.s3.us-east-1.amazonaws.com/demo_materials/non_onco/single_cell/metabolic_diseases/GSE292928/GSE292928_GEX_only_cellbender_sparse.h5ad \
  -flm https://bio-test-data.s3.us-east-1.amazonaws.com/demo_materials/non_onco/single_cell/metabolic_diseases/GSE292928/data.tsv \
  -dc 'Single-cell transcriptomics' \
  --template <TEMPLATE> \
  --allow-duplicates
```

### GSE148434

```bash
odm-import-data \
  --server <HOST> \
  --token <TOKEN> \
  --study https://bio-test-data.s3.us-east-1.amazonaws.com/demo_materials/non_onco/single_cell/neurodegenerative_diseases/GSE148434/study.tsv \
  --samples https://bio-test-data.s3.us-east-1.amazonaws.com/demo_materials/non_onco/single_cell/neurodegenerative_diseases/GSE148434/samples.tsv \
  --libraries https://bio-test-data.s3.us-east-1.amazonaws.com/demo_materials/non_onco/single_cell/neurodegenerative_diseases/GSE148434/libraries.tsv \
  -fl https://bio-test-data.s3.us-east-1.amazonaws.com/demo_materials/non_onco/single_cell/neurodegenerative_diseases/GSE148434/GSE148434_merged_data.h5ad \
  -flm https://bio-test-data.s3.us-east-1.amazonaws.com/demo_materials/non_onco/single_cell/neurodegenerative_diseases/GSE148434/data.tsv \
  -dc 'Single-cell transcriptomics' \
  --template <TEMPLATE> \
  --allow-duplicates
```
