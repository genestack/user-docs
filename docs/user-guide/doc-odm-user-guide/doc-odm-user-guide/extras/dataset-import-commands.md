# Curated Public Datasets: Import Commands

The commands below load each curated single-cell dataset into an ODM instance using the `odm-import-data` CLI. Each command uploads study and sample/library metadata alongside the H5AD attachment, ready for transformation.

Replace `<HOST>`, `<TOKEN>`, and `<TEMPLATE>` with your ODM instance URL, API token, and template ID before running. Commands can be run independently and in any order.

> Two datasets — **GSE192740** and **GSE198623** — contain multiple species and upload two H5AD files (human and mouse, or human and pig) within a single command.

---

## HeartDiversityTucker10x

```bash
odm-import-data \
  --server <HOST> \
  --token <TOKEN> \
  --study https://bio-test-data.s3.us-east-1.amazonaws.com/New_demo/Non-Onco/sc/Cardiovascular/HeartDiversityTucker10x/study.tsv \
  --samples https://bio-test-data.s3.us-east-1.amazonaws.com/New_demo/Non-Onco/sc/Cardiovascular/HeartDiversityTucker10x/samples.tsv \
  --libraries https://bio-test-data.s3.us-east-1.amazonaws.com/New_demo/Non-Onco/sc/Cardiovascular/HeartDiversityTucker10x/libraries.tsv \
  -fl https://bio-test-data.s3.us-east-1.amazonaws.com/New_demo/Non-Onco/sc/Cardiovascular/HeartDiversityTucker10x/healthy_human_4chamber_map_unnormalized_V4.h5ad \
  -flm https://bio-test-data.s3.us-east-1.amazonaws.com/New_demo/Non-Onco/sc/Cardiovascular/HeartDiversityTucker10x/data.tsv \
  -dc 'Single-cell transcriptomics' \
  --template <TEMPLATE> \
  --allow-duplicates
```

---

## SCP1303

```bash
odm-import-data \
  --server <HOST> \
  --token <TOKEN> \
  --study https://bio-test-data.s3.us-east-1.amazonaws.com/New_demo/Non-Onco/sc/Cardiovascular/SCP1303/study.tsv \
  --samples https://bio-test-data.s3.us-east-1.amazonaws.com/New_demo/Non-Onco/sc/Cardiovascular/SCP1303/samples.tsv \
  --libraries https://bio-test-data.s3.us-east-1.amazonaws.com/New_demo/Non-Onco/sc/Cardiovascular/SCP1303/libraries.tsv \
  -fl https://bio-test-data.s3.us-east-1.amazonaws.com/New_demo/Non-Onco/sc/Cardiovascular/SCP1303/human_dcm_hcm_scportal_03.17.2022.h5ad \
  -flm https://bio-test-data.s3.us-east-1.amazonaws.com/New_demo/Non-Onco/sc/Cardiovascular/SCP1303/data.tsv \
  -dc 'Single-cell transcriptomics' \
  --template <TEMPLATE> \
  --allow-duplicates
```

---

## GSE156793

```bash
odm-import-data \
  --server <HOST> \
  --token <TOKEN> \
  --study https://bio-test-data.s3.us-east-1.amazonaws.com/New_demo/Non-Onco/sc/Healthy_cell_atlases/GSE156793/study.tsv \
  --samples https://bio-test-data.s3.us-east-1.amazonaws.com/New_demo/Non-Onco/sc/Healthy_cell_atlases/GSE156793/samples.tsv \
  --libraries https://bio-test-data.s3.us-east-1.amazonaws.com/New_demo/Non-Onco/sc/Healthy_cell_atlases/GSE156793/libraries.tsv \
  -fl https://bio-test-data.s3.us-east-1.amazonaws.com/New_demo/Non-Onco/sc/Healthy_cell_atlases/GSE156793/GSE156793_all_organs_annotated_with_genes.h5ad \
  -flm https://bio-test-data.s3.us-east-1.amazonaws.com/New_demo/Non-Onco/sc/Healthy_cell_atlases/GSE156793/data.tsv \
  -dc 'Single-cell transcriptomics' \
  --template <TEMPLATE> \
  --allow-duplicates
```

---

## FibroticLiverWatsonMERFISH

```bash
odm-import-data \
  --server <HOST> \
  --token <TOKEN> \
  --study https://bio-test-data.s3.us-east-1.amazonaws.com/New_demo/Non-Onco/sc/Inflammatory/FibroticLiverWatsonMERFISH/study.tsv \
  --samples https://bio-test-data.s3.us-east-1.amazonaws.com/New_demo/Non-Onco/sc/Inflammatory/FibroticLiverWatsonMERFISH/samples.tsv \
  --libraries https://bio-test-data.s3.us-east-1.amazonaws.com/New_demo/Non-Onco/sc/Inflammatory/FibroticLiverWatsonMERFISH/libraries.tsv \
  -fl https://bio-test-data.s3.us-east-1.amazonaws.com/New_demo/Non-Onco/sc/Inflammatory/FibroticLiverWatsonMERFISH/GSE210077_adata_healthy_diseased_nucseq_sparse.h5ad \
  -flm https://bio-test-data.s3.us-east-1.amazonaws.com/New_demo/Non-Onco/sc/Inflammatory/FibroticLiverWatsonMERFISH/data.tsv \
  -dc 'Single-cell transcriptomics' \
  --template <TEMPLATE> \
  --allow-duplicates
```

---

## GSE165045

```bash
odm-import-data \
  --server <HOST> \
  --token <TOKEN> \
  --study https://bio-test-data.s3.us-east-1.amazonaws.com/New_demo/Non-Onco/sc/Inflammatory/GSE165045/study.tsv \
  --samples https://bio-test-data.s3.us-east-1.amazonaws.com/New_demo/Non-Onco/sc/Inflammatory/GSE165045/samples.tsv \
  --libraries https://bio-test-data.s3.us-east-1.amazonaws.com/New_demo/Non-Onco/sc/Inflammatory/GSE165045/libraries.tsv \
  -fl https://bio-test-data.s3.us-east-1.amazonaws.com/New_demo/Non-Onco/sc/Inflammatory/GSE165045/GSE165045_merged_with_TCR.h5ad \
  -flm https://bio-test-data.s3.us-east-1.amazonaws.com/New_demo/Non-Onco/sc/Inflammatory/GSE165045/data.tsv \
  -dc 'Single-cell transcriptomics' \
  --template <TEMPLATE> \
  --allow-duplicates
```

---

## GSE148073

```bash
odm-import-data \
  --server <HOST> \
  --token <TOKEN> \
  --study https://bio-test-data.s3.us-east-1.amazonaws.com/New_demo/Non-Onco/sc/Metabolic/GSE148073/study.tsv \
  --samples https://bio-test-data.s3.us-east-1.amazonaws.com/New_demo/Non-Onco/sc/Metabolic/GSE148073/samples.tsv \
  --libraries https://bio-test-data.s3.us-east-1.amazonaws.com/New_demo/Non-Onco/sc/Metabolic/GSE148073/libraries.tsv \
  -fl https://bio-test-data.s3.us-east-1.amazonaws.com/New_demo/Non-Onco/sc/Metabolic/GSE148073/GSE148073_merged_data_new.h5ad \
  -flm https://bio-test-data.s3.us-east-1.amazonaws.com/New_demo/Non-Onco/sc/Metabolic/GSE148073/data.tsv \
  -dc 'Single-cell transcriptomics' \
  --template <TEMPLATE> \
  --allow-duplicates
```

---

## GSE192740 (human + mouse)

```bash
odm-import-data \
  --server <HOST> \
  --token <TOKEN> \
  --study https://bio-test-data.s3.us-east-1.amazonaws.com/New_demo/Non-Onco/sc/Metabolic/GSE192740/study.tsv \
  --samples https://bio-test-data.s3.us-east-1.amazonaws.com/New_demo/Non-Onco/sc/Metabolic/GSE192740/samples.tsv \
  --libraries https://bio-test-data.s3.us-east-1.amazonaws.com/New_demo/Non-Onco/sc/Metabolic/GSE192740/libraries.tsv \
  -fl https://bio-test-data.s3.us-east-1.amazonaws.com/New_demo/Non-Onco/sc/Metabolic/GSE192740/GSE192740_human_combined_sparse.h5ad \
  -flm https://bio-test-data.s3.us-east-1.amazonaws.com/New_demo/Non-Onco/sc/Metabolic/GSE192740/data_human.tsv \
  -dc 'Single-cell transcriptomics' \
  -fl https://bio-test-data.s3.us-east-1.amazonaws.com/New_demo/Non-Onco/sc/Metabolic/GSE192740/GSE192740_mouse_combined_sparse.h5ad \
  -flm https://bio-test-data.s3.us-east-1.amazonaws.com/New_demo/Non-Onco/sc/Metabolic/GSE192740/data_mouse.tsv \
  -dc 'Single-cell transcriptomics' \
  --template <TEMPLATE> \
  --allow-duplicates
```

---

## GSE198623 (human + pig)

```bash
odm-import-data \
  --server <HOST> \
  --token <TOKEN> \
  --study https://bio-test-data.s3.us-east-1.amazonaws.com/New_demo/Non-Onco/sc/Metabolic/GSE198623/study.tsv \
  --samples https://bio-test-data.s3.us-east-1.amazonaws.com/New_demo/Non-Onco/sc/Metabolic/GSE198623/samples.tsv \
  --libraries https://bio-test-data.s3.us-east-1.amazonaws.com/New_demo/Non-Onco/sc/Metabolic/GSE198623/libraries.tsv \
  -fl https://bio-test-data.s3.us-east-1.amazonaws.com/New_demo/Non-Onco/sc/Metabolic/GSE198623/GSE198623_human_processed.h5ad \
  -flm https://bio-test-data.s3.us-east-1.amazonaws.com/New_demo/Non-Onco/sc/Metabolic/GSE198623/data_human.tsv \
  -dc 'Single-cell transcriptomics' \
  -fl https://bio-test-data.s3.us-east-1.amazonaws.com/New_demo/Non-Onco/sc/Metabolic/GSE198623/GSE198623_pig_processed.h5ad \
  -flm https://bio-test-data.s3.us-east-1.amazonaws.com/New_demo/Non-Onco/sc/Metabolic/GSE198623/data_pig.tsv \
  -dc 'Single-cell transcriptomics' \
  --template <TEMPLATE> \
  --allow-duplicates
```

---

## GSE292928

```bash
odm-import-data \
  --server <HOST> \
  --token <TOKEN> \
  --study https://bio-test-data.s3.us-east-1.amazonaws.com/New_demo/Non-Onco/sc/Metabolic/GSE292928/study.tsv \
  --samples https://bio-test-data.s3.us-east-1.amazonaws.com/New_demo/Non-Onco/sc/Metabolic/GSE292928/samples.tsv \
  --libraries https://bio-test-data.s3.us-east-1.amazonaws.com/New_demo/Non-Onco/sc/Metabolic/GSE292928/libraries.tsv \
  -fl https://bio-test-data.s3.us-east-1.amazonaws.com/New_demo/Non-Onco/sc/Metabolic/GSE292928/GSE292928_GEX_only_cellbender_sparse.h5ad \
  -flm https://bio-test-data.s3.us-east-1.amazonaws.com/New_demo/Non-Onco/sc/Metabolic/GSE292928/data.tsv \
  -dc 'Single-cell transcriptomics' \
  --template <TEMPLATE> \
  --allow-duplicates
```

---

## GSE148434

```bash
odm-import-data \
  --server <HOST> \
  --token <TOKEN> \
  --study https://bio-test-data.s3.us-east-1.amazonaws.com/New_demo/Non-Onco/sc/Neurodegenerative/GSE148434/study.tsv \
  --samples https://bio-test-data.s3.us-east-1.amazonaws.com/New_demo/Non-Onco/sc/Neurodegenerative/GSE148434/samples.tsv \
  --libraries https://bio-test-data.s3.us-east-1.amazonaws.com/New_demo/Non-Onco/sc/Neurodegenerative/GSE148434/libraries.tsv \
  -fl https://bio-test-data.s3.us-east-1.amazonaws.com/New_demo/Non-Onco/sc/Neurodegenerative/GSE148434/GSE148434_merged_data.h5ad \
  -flm https://bio-test-data.s3.us-east-1.amazonaws.com/New_demo/Non-Onco/sc/Neurodegenerative/GSE148434/data.tsv \
  -dc 'Single-cell transcriptomics' \
  --template <TEMPLATE> \
  --allow-duplicates
```
