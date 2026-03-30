# Attribute Mapping Reference

During metadata curation, the transformation automatically maps commonly used attribute names found in source HDF5 files to the canonical ODM API names. This makes it possible to ingest data from a wide variety of tools and workflows — such as Seurat, Scanpy, or Cell Ranger — without requiring manual renaming of attributes before import.

Mapping is applied separately to cell metadata and feature metadata. When an attribute in the source file matches one of the known alternative names listed below, it is renamed to the corresponding ODM API display name. Attributes that do not match any known name are converted to camelCase.

## Cell metadata attributes

The table below lists the canonical ODM API name for each attribute alongside the alternative source names that are automatically recognized.

| ODM API display name | Alternative names |
|---|---|
| cellID | — |
| barcode | — |
| batch | `sample_id`, `sample`, `run_id` |
| cellType | `cell_type`, `celltype`, `ident`, `labels` |
| cluster | `cluster_louvain`, `cluster_leiden`, `seurat_clusters` |
| nCounts | `n_counts`, `umi_count`, `nCount_RNA`, `total_umi`, `n_umi`, `n_reads`, `nUMI`, `UMI_count` |
| percentMito | `percent_mito`, `percent_mt`, `percent.mt`, `pct_mt`, `pct_mito`, `pct_counts_mito`, `percent.mito`, `percent.mito.raw`, `mito_ratio`, `pct_counts_mt` |
| umap | `X_umap`, `UMAP` |
| pca | `X_pca`, `PCA` |
| tsne | `X_tsne`, `tSNE` |
| pcaHarmony | `pca_harmony`, `X_harmony`, `harmony_embedding`, `X_pca_harmony` |
| nGenes | `n_genes`, `n_genes_by_counts`, `nGene`, `n_features`, `nFeature_RNA`, `genes_detected`, `detected_genes`, `gene_count`, `Total_Genes_Detected` |
| mitoCounts | `mito_counts`, `total_counts_mt`, `total_counts_mito`, `subsets_mt_sum`, `mt_sum`, `MT_sum` |
| riboCounts | `ribo_counts`, `total_counts_ribo`, `total_counts_rb`, `subsets_ribo_sum`, `rb_counts`, `rb_sum` |
| percentRibo | `percent_ribo`, `percent_rb`, `percent.rb`, `pct_counts_ribo`, `ribo_ratio`, `pct_ribo`, `pct_counts_rb`, `pct_counts_rrna` |
| percentHemoglobin | `percent_hb`, `pct_hb`, `hemoglobin_fraction`, `prop_hb`, `percent_hemoglobin` |
| doubletStatus | `doublet_status`, `is_doublet`, `predicted_doublet`, `multiplet_status` |
| doubletScore | `doublet_score`, `scrublet_score`, `doublet_probability`, `multiplet_score`, `doublet_stat` |
| sScore | `S_score`, `s.score`, `S.Score`, `s_phase_score`, `S_phase_probability` |
| g2mScore | `G2M_score`, `g2m.score`, `G2M.Score`, `g2m_phase_score`, `G2M_phase_probability` |
| CellCycle | `phase`, `cell_cycle_phase`, `cc_phase`, `cycle_stage` |
| ambientFraction | `ambient_fraction`, `decontX_score`, `rho`, `contamination_fraction`, `ambient_rna_percent`, `soup_fraction`, `soup_frac` |

## Feature metadata attributes

The table below lists the canonical ODM API name for each feature attribute alongside the alternative source names that are automatically recognized.

| ODM API display name | Alternative names |
|---|---|
| geneId | `gene_id` (index), `gene_ids`, `ensembl_id`, `feature_id`, `stable_id`, `ENSEMBL` |
| gene | `symbol`, `symbols`, `gene_symbol`, `gene_symbols`, `feature_name`, `display_name`, `name`, `gene_name` |
| totalCounts | `total_counts`, `gene_total`, `sum_counts`, `count_sum`, `total_umis` |
| nCellsByCounts | `n_cells_by_counts`, `n_cells`, `num_cells`, `n_obs`, `num_cells_expressed` |
| meanCounts | `mean_counts`, `avg_exp`, `obs_mean`, `means` |
| pctDropoutByCounts | `pct_dropout_by_counts`, `pct_dropout`, `percent_dropout`, `dropout_rate` |
