# Attribute mapping reference

During metadata curation, the transformation automatically maps commonly used attribute names found in source HDF5 files to the canonical ODM API names.

Mapping is applied separately to cell metadata and feature metadata. When an attribute in the source file matches one of the known alternative names listed below, it is renamed to the corresponding ODM API display name. Attributes that do not match any known name are converted to camelCase.

## Cell metadata attributes

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
| cellCycle | `phase`, `cell_cycle_phase`, `cc_phase`, `cycle_stage` |
| ambientFraction | `ambient_fraction`, `decontX_score`, `rho`, `contamination_fraction`, `ambient_rna_percent`, `soup_fraction`, `soup_frac` |

## Feature metadata attributes

| ODM API display name | Alternative names |
|---|---|
| geneId | `gene_id` (index), `gene_ids`, `ensembl_id`, `feature_id`, `stable_id`, `ENSEMBL` |
| gene | `symbol`, `symbols`, `gene_symbol`, `gene_symbols`, `feature_name`, `display_name`, `name`, `gene_name` |
| totalCounts | `total_counts`, `gene_total`, `sum_counts`, `count_sum`, `total_umis` |
| nCellsByCounts | `n_cells_by_counts`, `n_cells`, `num_cells`, `n_obs`, `num_cells_expressed` |
| meanCounts | `mean_counts`, `avg_exp`, `obs_mean`, `means` |
| pctDropoutByCounts | `pct_dropout_by_counts`, `pct_dropout`, `percent_dropout`, `dropout_rate` |

## Gene ID to name mapping {#gene-id-to-name-mapping}

When feature metadata contains a `geneId` column but no gene name column, the transformation can automatically resolve gene names from a built-in reference. This is controlled by the `map_gene_ids_to_names` parameter in the `feature_metadata` configuration block, which is enabled by default. Set it to `false` for proteomics or other non-gene-ID data where this behaviour is not appropriate.

The mapping uses Ensembl and NCBI reference data. Both Ensembl gene IDs (for example, `ENSG...`) and NCBI gene IDs are supported. The following organisms are supported in `hdf5-cells`:

| Organism | Genome version | Ensembl release | NCBI release |
|----------|----------------|-----------------|--------------|
| *Homo sapiens* | GRCh38.p14 | 115 | GCF_000001405.40-RS_2025_08 |
| *Mus musculus* | GRCm39 | 115 | GCF_000001635.27-RS_2024_02 |
| *Rattus norvegicus* | GRCr8 | 115 | GCF_036323735.1-RS_2024_02 |
| *Sus scrofa* | Sscrofa11.1 | 115 | 106 |

> The gene ID column must be named `geneId` for mapping to be performed. If the column has a different name in the source file, ensure it is covered by the feature metadata attribute mapping above so that it is renamed to `geneId` before this step runs.
