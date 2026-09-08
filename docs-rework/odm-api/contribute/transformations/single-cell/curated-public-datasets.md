---
diataxis: reference
tab: odm-api
---

# Curated public datasets: import commands and configurations

Each curated single-cell dataset below ships with a tested import command and a pre-validated transformation configuration. For a given dataset, use its import command to load it into ODM, then run a transformation job with the configuration listed in that dataset's section.

The import commands use the `odm-import-data` CLI and upload the study and sample/library metadata alongside the H5AD attachment, ready for transformation. Replace `<HOST>`, `<TOKEN>`, and `<TEMPLATE>` with your ODM instance URL, API token, and template ID before running. Commands can be run independently and in any order.

Recommended template: [Public dataset template](https://bio-test-data.s3.us-east-1.amazonaws.com/demo_materials/templates/public_studies_template_demo.json)

> Because these configurations have been pre-validated against their datasets, you can skip the dry-run step when transforming the curated catalogue.
>
> Two datasets (**GSE192740** and **GSE198623**) contain multiple species and upload two H5AD files (human and mouse, or human and pig) within a single command.

For what the configuration fields mean, see the [Configuration reference](configuration-reference.md).

---

## Configuration index

Several datasets share an aggregated configuration. Each dataset's own section repeats the configuration that applies to it.

| Configuration | Datasets |
|---|---|
| [`aggregated_config_1`](../../../../assets/user-guide/doc-odm-user-guide/doc-odm-user-guide/extras/aggregated_config_1.json) | HeartDiversityTucker10x · SCP1303 · GSE192740_human · GSE192740_mouse · GSE292928 · GSE148434 |
| [`aggregated_config_2`](../../../../assets/user-guide/doc-odm-user-guide/doc-odm-user-guide/extras/aggregated_config_2.json) | GSE198623_human · GSE198623_pig |
| [`aggregated_config_3`](../../../../assets/user-guide/doc-odm-user-guide/doc-odm-user-guide/extras/aggregated_config_3.json) | GSE148073 · FibroticLiverWatsonMERFISH |
| [`GSE156793`](../../../../assets/user-guide/doc-odm-user-guide/doc-odm-user-guide/extras/GSE156793.json) | GSE156793 |
| [`GSE165045`](../../../../assets/user-guide/doc-odm-user-guide/doc-odm-user-guide/extras/GSE165045.json) | GSE165045 |

---

## HeartDiversityTucker10x

**Configuration:** [`aggregated_config_1`](../../../../assets/user-guide/doc-odm-user-guide/doc-odm-user-guide/extras/aggregated_config_1.json)

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

---

## SCP1303

**Configuration:** [`aggregated_config_1`](../../../../assets/user-guide/doc-odm-user-guide/doc-odm-user-guide/extras/aggregated_config_1.json)

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

---

## GSE156793

**Configuration:** [`GSE156793`](../../../../assets/user-guide/doc-odm-user-guide/doc-odm-user-guide/extras/GSE156793.json)

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

---

## FibroticLiverWatsonMERFISH

**Configuration:** [`aggregated_config_3`](../../../../assets/user-guide/doc-odm-user-guide/doc-odm-user-guide/extras/aggregated_config_3.json)

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

---

## GSE165045

**Configuration:** [`GSE165045`](../../../../assets/user-guide/doc-odm-user-guide/doc-odm-user-guide/extras/GSE165045.json)

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

---

## GSE148073

**Configuration:** [`aggregated_config_3`](../../../../assets/user-guide/doc-odm-user-guide/doc-odm-user-guide/extras/aggregated_config_3.json)

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

---

## GSE192740 (human + mouse)

**Configuration:** [`aggregated_config_1`](../../../../assets/user-guide/doc-odm-user-guide/doc-odm-user-guide/extras/aggregated_config_1.json)

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

---

## GSE198623 (human + pig)

**Configuration:** [`aggregated_config_2`](../../../../assets/user-guide/doc-odm-user-guide/doc-odm-user-guide/extras/aggregated_config_2.json)

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

---

## GSE292928

**Configuration:** [`aggregated_config_1`](../../../../assets/user-guide/doc-odm-user-guide/doc-odm-user-guide/extras/aggregated_config_1.json)

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

---

## GSE148434

**Configuration:** [`aggregated_config_1`](../../../../assets/user-guide/doc-odm-user-guide/doc-odm-user-guide/extras/aggregated_config_1.json)

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
