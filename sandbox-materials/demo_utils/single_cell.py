"""Single-cell analysis and visualisation helpers."""

import json
import textwrap
import uuid
from collections import Counter

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import anndata as ad
import scanpy as sc
from IPython.display import HTML, display
from matplotlib.patches import Patch
from scipy.cluster.hierarchy import leaves_list, linkage
from scipy.spatial.distance import pdist
from scipy import sparse
from scipy.sparse import coo_matrix

from demo_utils._util import (
    _enable_umap_axis_ticks,
    _shared_vmin_vmax,
    _short_label,
)
from demo_utils.theme import GS_LINE


def create_full_matrix(
    cells: pd.DataFrame,
    expression: pd.DataFrame,
    genes: list[str] | None = None,
) -> sparse.csr_matrix:
    """
    Build a genes × cells sparse expression matrix from long-form API tables.
    
    Parameters:
    - cells: Cell table indexed by barcode / runSourceId.
    - expression: Long-form expression with runSourceId and gene.
    - genes: Optional gene order; default = genes present in expression.
    
    Returns:
    - genes × cells expression matrix aligned to
      the chosen gene list and cells.index.
    """
    # filter expression data to only include cells in provided barcodes
    valid_cells = cells.index
    ex_df_filt = expression[expression['runSourceId'].isin(valid_cells)].copy()

    # get unique genes and cells
    genes_unique = list(genes) if genes is not None else ex_df_filt['gene'].unique()
    cells_unique = cells.index

    # create mapping gene / cell - matrix index
    gene_to_idx = {gene: i for i, gene in enumerate(genes_unique)}
    cell_to_idx = {cell: i for i, cell in enumerate(cells_unique)}

    # map expression data to matrix indices; drop rows that don't map cleanly
    row_idx = ex_df_filt['gene'].map(gene_to_idx)
    col_idx = ex_df_filt['runSourceId'].map(cell_to_idx)
    valid = row_idx.notna() & col_idx.notna()
    row_idx = row_idx[valid].astype(int).values
    col_idx = col_idx[valid].astype(int).values
    data = ex_df_filt.loc[valid, 'value'].values

    # build sparse matrix (genes x cells)
    counts_matrix = coo_matrix(
    (data, (row_idx, col_idx)),
    shape=(len(genes_unique), len(cells_unique))
    )

    counts_matrix = counts_matrix.tocsr()
    return counts_matrix


def create_anndata_object(
    cell_metadata: pd.DataFrame,
    feature_metadata: pd.DataFrame | None = None,
    counts_matrix: pd.DataFrame | None = None,
) -> ad.AnnData:
    """
    Create an AnnData object from cell metadata, optional features, and counts.
    
    Parameters:
    - cell_metadata: Cell metadata (rows = cells; e.g. indexed by barcode).
    - feature_metadata: Optional feature / gene metadata for ``var``.
    - counts_matrix: Optional features × cells counts; stored transposed as ``X``.
    
    Returns:
    - AnnData with obs/var/X set; UMAP coords moved to ``obsm['X_umap']`` when present.
    """
    adata = ad.AnnData(
        X=counts_matrix.T if counts_matrix is not None else None,
        obs=cell_metadata.loc[cell_metadata.index].copy(),
        var=feature_metadata if feature_metadata is not None else None
    )

    if 'umap' in adata.obs.columns:
        adata.obsm["X_umap"] = np.stack(adata.obs["umap"].values)

    return adata


def plot_cell_type_proportions(
    df: pd.DataFrame,
    row_height: float = 0.38,
    min_height: float = 4,
    rarity_threshold: float = 0.01,
    bar_color: str = '#0470BE',
    rare_color: str = '#B7EAFF',
) -> None:
    """
    Horizontal bar chart of cell-type abundance in one cohort.
    
    Bar length = total_prop; rare types below rarity_threshold are greyed.
    
    Parameters:
    - df: Columns cell_type, total_count, total_prop.
    - row_height: Inches per row.
    - min_height: Minimum figure height.
    - rarity_threshold: Proportion below which bars use rare_color.
    - bar_color: Colour for common types.
    - rare_color: Colour for rare types.
    
    Returns:
    - Displays a matplotlib bar chart.
    """
    plot_df = df.copy()
    plot_df['total_prop'] = plot_df['total_count'] / plot_df['total_count'].sum()

    plot_df = plot_df[plot_df['total_count'] > 0].sort_values('total_prop', ascending=True)

    if plot_df.empty:
        print("No cell types with counts > 0.")
        return

    n = len(plot_df)
    fig_h = max(min_height, row_height * n)
    fig, ax = plt.subplots(figsize=(8, fig_h))

    colors = [bar_color if p >= rarity_threshold else rare_color
              for p in plot_df['total_prop']]

    bars = ax.barh(plot_df['cell_type'], plot_df['total_prop'],
                   color=colors, edgecolor='white', linewidth=0.5, height=0.7)

    x_max = plot_df['total_prop'].max()
    for bar, (_, row) in zip(bars, plot_df.iterrows()):
        w = bar.get_width()
        ax.text(
            w + x_max * 0.01, bar.get_y() + bar.get_height() / 2,
            f"{row['total_count']:,}  ({w*100:.2f}%)",
            va='center', ha='left', fontsize=8, color='#444'
        )

    ax.axvline(rarity_threshold, color='#888', linewidth=1.2,
               linestyle='--', zorder=3)
    ax.text(rarity_threshold + x_max * 0.005,
            ax.get_ylim()[0] + 0.3,
            f'Rarity\n({rarity_threshold*100:.0f}%)',
            color='#888', fontsize=8, va='bottom')

    ax.set_xlabel('Proportion of total cells', fontsize=9)
    ax.set_ylabel('')
    ax.set_xlim(0, x_max * 1.35)
    ax.spines[['top', 'right']].set_visible(False)
    ax.tick_params(axis='y', labelsize=9)
    ax.tick_params(axis='x', labelsize=8)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x*100:.0f}%'))
    ax.grid(axis='x', linestyle='--', linewidth=0.4, alpha=0.4, zorder=0)
    ax.set_facecolor('white')

    ax.legend(
        handles=[Patch(color=bar_color,  label=f'≥{rarity_threshold*100:.0f}% (present)'),
                 Patch(color=rare_color, label=f'<{rarity_threshold*100:.0f}% (rare)')],
        fontsize=8, frameon=False, loc='lower right'
    )

    plt.tight_layout()
    plt.show()


def plot_cell_type_proportions_comparison(
    case_df: pd.DataFrame,
    ctrl_df: pd.DataFrame,
    case_label: str = 'Case',
    ctrl_label: str = 'Control',
    row_height: float = 0.55,
    min_height: float = 4,
    rarity_threshold: float = 0.01,
    case_color: str = '#0470BE',
    ctrl_color: str = '#93D8B8',
    top_n: int | None = None,
    title: str | None = None,
    legend_loc: str = 'lower right',
) -> None:
    """
    Paired horizontal bars comparing cell-type proportions (case vs control).
    
    Highlights composition shifts (e.g. case vs control) for the top_n types.
    
    Parameters:
    - case_df: Case proportions (cell_type, total_count, total_prop).
    - ctrl_df: Control proportions (same columns).
    - case_label: Legend / axis label for case.
    - ctrl_label: Legend / axis label for control.
    - row_height: Inches per row.
    - min_height: Minimum figure height.
    - rarity_threshold: Types below this in both groups are de-emphasised.
    - case_color: Case bar colour.
    - ctrl_color: Control bar colour.
    - top_n: Max cell types to show.
    - title: Plot title.
    - legend_loc: Matplotlib legend location.
    
    Returns:
    - Displays a matplotlib comparison chart.
    """
    case = case_df.copy()
    ctrl = ctrl_df.copy()
    case['prop'] = case['total_count'] / case['total_count'].sum()
    ctrl['prop'] = ctrl['total_count'] / ctrl['total_count'].sum()

    merged = case[['cell_type', 'prop', 'total_count']].merge(
        ctrl[['cell_type', 'prop', 'total_count']],
        on='cell_type', suffixes=('_case', '_ctrl')
    )
    merged = merged[(merged['prop_case'] > 0) | (merged['prop_ctrl'] > 0)]
    if top_n:
        merged = merged.sort_values('prop_case', ascending=False).head(top_n)
    merged = merged.sort_values('prop_case', ascending=True).reset_index(drop=True)

    n = len(merged)
    fig_h = max(min_height, row_height * n)
    fig, ax = plt.subplots(figsize=(9, fig_h), constrained_layout=True)

    bar_h = 0.35
    y = np.arange(n)
    x_max = max(merged['prop_case'].max(), merged['prop_ctrl'].max()) * 1.4

    for offset, prop_col, count_col, color in [
        (+bar_h/2, 'prop_case', 'total_count_case', case_color),
        (-bar_h/2, 'prop_ctrl', 'total_count_ctrl', ctrl_color),
    ]:
        props  = merged[prop_col].values
        counts = merged[count_col].values
        alphas = [1.0 if p >= rarity_threshold else 0.35 for p in props]
        for i, (p, cnt, a) in enumerate(zip(props, counts, alphas)):
            ax.barh(y[i] + offset, p, height=bar_h,
                    color=color, alpha=a, edgecolor='white', linewidth=0.4)
            ax.text(p + x_max * 0.01, y[i] + offset,
                    f"{cnt:,}  ({p*100:.2f}%)",
                    va='center', ha='left', fontsize=7.5, color='#444')

    ax.axvline(rarity_threshold, color='#888', linewidth=1.0, linestyle='--', zorder=3)
    ax.text(rarity_threshold + x_max * 0.005, 0.97,
            f'Rarity ({rarity_threshold*100:.0f}%)',
            transform=ax.get_xaxis_transform(),
            color='#888', fontsize=7.5, va='top')

    ax.set_yticks(y)
    ax.set_ylim(-0.5, n - 0.5)
    ax.set_yticklabels(merged['cell_type'], fontsize=9)
    ax.set_xlim(0, x_max)
    ax.set_xlabel('Proportion of total cells', fontsize=9)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x*100:.0f}%'))
    ax.spines[['top', 'right']].set_visible(False)
    ax.tick_params(axis='x', labelsize=8)
    ax.grid(axis='x', linestyle='--', linewidth=0.4, alpha=0.4, zorder=0)
    ax.set_facecolor('white')
    _legend_kwargs = dict(handles=[
        Patch(color=case_color, label=case_label),
        Patch(color=ctrl_color, label=ctrl_label),
    ], fontsize=9, frameon=False)
    if legend_loc == 'top':
        _legend_kwargs.update(loc='lower center', bbox_to_anchor=(0.5, 1.01),
                              ncol=2, borderaxespad=0)
    else:
        _legend_kwargs.update(loc=legend_loc)
    ax.legend(**_legend_kwargs)

    if title:
        ax.set_title('\n'.join(textwrap.wrap(title, 70)), fontsize=10,
                     color='#1b2a4a', pad=28 if legend_loc == 'top' else 10)

    plt.show()


def plot_umap_panel(
    adata_dict: dict[str, ad.AnnData],
    color: str = 'cellType',
    figsize_per_col: float = 6,
    point_size: float = 25,
    show_umap_coords: bool = False,
) -> None:
    """
    Show a side-by-side panel of UMAP plots coloured by cell type.
    
    Parameters:
    - adata_dict: Mapping of panel title → AnnData (must have ``obsm['X_umap']``).
    - color: Cell type attribute to color by.
    - figsize_per_col: Figure width contribution per column.
    - point_size: size of points on the UMAP
    - show_umap_coords: If True, show UMAP axis ticks and labels.
    
    Returns:
    - Displays a matplotlib UMAP panel.
    """
    n_cols = len(adata_dict)
    fig, axes = plt.subplots(1, n_cols, figsize=(figsize_per_col * n_cols, 5))
    axes = np.atleast_1d(axes)

    for i, (name, adata) in enumerate(adata_dict.items()):
        sc.pl.umap(
            adata,
            color=color,
            ax=axes[i],
            size=point_size,
            legend_loc='on data',
            title=name,
            show=False,
        )

        if show_umap_coords:
            _enable_umap_axis_ticks(axes[i])

    plt.tight_layout()
    plt.show()


def compare_gene_expression_with_umap(
    adata_dict: dict[str, ad.AnnData],
    genes: list[str],
    figsize_per_col: float = 6,
    figsize_per_row: float = 5,
    point_size: float = 25,
    show_umap_coords: bool = False,
) -> None:
    """
    Compare gene expression on UMAP across multiple groups (plot columns).
    
    One row per gene, one column per AnnData; colour scales are shared
    across columns for each gene.
    
    Parameters:
    - adata_dict: Mapping of panel title → AnnData (must have ``obsm['X_umap']``).
    - genes: Genes to plot (one row per gene).
    - figsize_per_col: Figure width contribution per column.
    - figsize_per_row: Figure height contribution per row.
    - point_size: size of points on the UMAP
    - show_umap_coords: If True, show UMAP axis ticks and labels.
    
    Returns:
    - Displays a matplotlib UMAP expression panel.
    """
    if len(adata_dict) < 1:
        raise ValueError("Need at least one AnnData object")

    titles = list(adata_dict.keys())
    adatas = list(adata_dict.values())
    n_genes = len(genes)
    n_cols = len(adatas)

    _, axes = plt.subplots(
        n_genes, n_cols,
        figsize=(figsize_per_col * n_cols, figsize_per_row * n_genes),
        squeeze=False,  # axes is always 2D
    )

    for i, gene in enumerate(genes):
        # skip genes missing from any object
        if not all(gene in a.var_names for a in adatas):
            print(f"Skipping {gene}: not in all groups")
            continue

        vmin, vmax = _shared_vmin_vmax(adatas, gene)

        for j, (title, adata) in enumerate(zip(titles, adatas)):
            sc.pl.umap(
                adata,
                color=gene,
                ax=axes[i, j],
                vmin=vmin,
                vmax=vmax,
                size=point_size,
                cmap="viridis",
                frameon=True,
                colorbar_loc="right" if j == n_cols - 1 else None,
                title=f"{gene}: {title}",
                show=False,
            )

            if show_umap_coords:
                _enable_umap_axis_ticks(axes[i, j])

    plt.tight_layout()
    plt.show()


def annotate_cells_by_marker_panel(
    adata_dict: dict[str, ad.AnnData],
    marker_genes: list[str],
    weights: dict[str, float],
    score_percentile: float = 99,
    cell_original_key: str = 'cellType',
    cell_score_key: str = 'marker_panel_score',
    cell_call_key: str = 'marker_panel_cells',
    figsize_per_col: float = 6.0,
    figsize_per_row: float = 5.0,
    point_size: float = 25,
    show_umap_coords: bool = False,
    copy: bool = False,
) -> dict[str, ad.AnnData] | None:
    """
    Score cells in each AnnData with a weighted marker panel, call positives with one threshold 
    from the pooled score distribution (ignoring cells with no panel signal), and plot a 2-row
    faceted UMAP (original annotation / marker panel call × adata_dict columns).

    Parameters:
    - adata_dict: title → AnnData (must have obsm['X_umap'])
    - marker_genes: panel gene symbols / IDs
    - weights: gene → weight (e.g. cell_spec_score); keys = gene IDs
    - score_percentile: percentile of score distribution to use as the threshold for calling cells
    - cell_original_key: obs column used for the top-row categorical UMAP
    - cell_score_key, cell_call_key: obs columns written on each AnnData
    - figsize_per_col, figsize_per_row: width and height of one column and row
    - point_size: size of points on the UMAP
    - show_umap_coords: whether to show UMAP axis ticks
    - copy: if False (default), mutate objects in adata_dict in place; 
            if True, copy each AnnData and return a new title → AnnData dict

    Returns:
    - None if copy is False; a new dict of copied AnnData objects if copy is True.
      Displays a matplotlib UMAP panel in either case.
    """
    if len(adata_dict) < 1:
        raise ValueError('Need at least one AnnData object')

    titles = list(adata_dict.keys())
    adatas = list(adata_dict.values())
    n_cols = len(adatas)

    for adata in adatas:
        if cell_original_key not in adata.obs:
            raise KeyError(f"cell_original_key={cell_original_key!r} missing from one AnnData.obs")

    if copy:
        adatas = [adata.copy() for adata in adatas]

    # genes present in every object and in weights
    genes = [
        g for g in marker_genes
        if g in weights and all(g in a.var_names for a in adatas)
    ]
    if not genes:
        raise ValueError('No marker genes shared by all AnnData objects and weights')

    w = np.array([weights[g] for g in genes]) 

    # pooled expression → shared z-score parameters
    Xs = []
    for adata in adatas:
        X = adata[:, genes].X
        if sparse.issparse(X):
            X = X.toarray()
        Xs.append(np.asarray(X, dtype=float))

    X_all = np.vstack(Xs)
    gene_mean = X_all.mean(axis=0)
    gene_std = X_all.std(axis=0) + 1e-8

    # score each object with the same mean/std
    ws_all = []
    for adata, X in zip(adatas, Xs):
        Xz = (X - gene_mean) / gene_std
        ws_all.append(Xz @ w)
    for adata, ws in zip(adatas, ws_all):
        adata.obs[cell_score_key] = ws

    # shared threshold from pooled scores
    pooled = np.concatenate([a.obs[cell_score_key].to_numpy() for a in adatas])
    nonzero = pooled[pooled > np.min(pooled)]
    score_threshold = np.percentile(nonzero, score_percentile)

    for adata in adatas:
        adata.obs[cell_call_key] = pd.Categorical(
            (adata.obs[cell_score_key] >= score_threshold).astype(str),
            categories=['False', 'True'],  # keep both, even if unused
        )

    # shared category order for cell_original_key across columns
    all_cats = sorted({
        str(v)
        for adata in adatas
        for v in adata.obs[cell_original_key].astype(str).unique()
    })
    for adata in adatas:
        adata.obs[cell_original_key] = pd.Categorical(
            adata.obs[cell_original_key].astype(str),
            categories=all_cats,
        )

    # faceted UMAP: annotation / call
    n_rows = 2
    _, axes = plt.subplots(
        n_rows, n_cols,
        figsize=(figsize_per_col * n_cols, figsize_per_row * n_rows),
        squeeze=False,
    )

    for j, (title, adata) in enumerate(zip(titles, adatas)):
        pos = (adata.obs[cell_call_key] == 'True').to_numpy()
        n_pos = int(pos.sum())
        n_total = adata.n_obs

        # plot original annotation
        sc.pl.umap(
            adata,
            color=cell_original_key,
            ax=axes[0, j],
            size=point_size,
            frameon=True,
            legend_loc='on data',
            legend_fontsize=8,
            legend_fontoutline=2,
            title=f'{title}\n{cell_original_key}',
            show=False,
        )

        # plot marker panel call
        sc.pl.umap(
            adata,
            color=cell_call_key,
            ax=axes[1, j],
            size=point_size,
            palette={'True': '#0470BE', 'False': '#D0D5DD'},
            frameon=True,
            legend_loc='right margin' if j == n_cols - 1 else None,
            title=f'{title}\nmarker-panel⁺ cells (n={n_pos}/{n_total})',
            show=False,
        )

        # re-draw positive calls last so they are never hidden by points overplotting        
        axes[1, j].scatter(
            adata.obsm['X_umap'][pos, 0],
            adata.obsm['X_umap'][pos, 1],
            s=point_size/4,
            c='#0470BE',
        )

        if show_umap_coords:
            from demo_utils._util import _enable_umap_axis_ticks
            for i in range(n_rows):
                _enable_umap_axis_ticks(axes[i, j])

    plt.tight_layout()
    plt.show()

    if copy:
        return {k: v for k, v in zip(titles, adatas)}
    return None


def plot_cell_composition(
    all_study_counts: dict,
    case_label: str,
    ctrl_label: str,
) -> None:
    """
    Multi-study view of cell-type mix in case vs control cohorts.
    
    One subplot per study showing how cell-type composition differs between
    the case and control conditions.
    
    Parameters:
    - all_study_counts: study → {'case': counts, 'ctrl': counts} structures.
    - case_label: Label for the case condition.
    - ctrl_label: Label for the control condition.
    
    Returns:
    - Displays a matplotlib multi-panel composition figure.
    """
    if not all_study_counts:
        print("No data to plot.")
        return

    all_cell_types = sorted(set(
        ct for data in all_study_counts.values() for ct in data['cell_types']
    ))
    cmap   = plt.colormaps.get_cmap('tab20').resampled(max(len(all_cell_types), 1))
    colors = {ct: cmap(i) for i, ct in enumerate(all_cell_types)}

    n_studies = len(all_study_counts)
    fig, axes = plt.subplots(1, n_studies, figsize=(4 * n_studies, 7))
    if n_studies == 1:
        axes = [axes]

    x_labels = [case_label, ctrl_label]

    for ax, (acc, data) in zip(axes, all_study_counts.items()):
        counts_case = data['case'].set_index('cell_type')['total_count']
        counts_ctrl = data['ctrl'].set_index('cell_type')['total_count']
        prop_case = (counts_case / counts_case.sum()).reindex(data['cell_types'], fill_value=0)
        prop_ctrl = (counts_ctrl / counts_ctrl.sum()).reindex(data['cell_types'], fill_value=0)

        bottom_case = bottom_ctrl = 0
        for ct in data['cell_types']:
            v_case = prop_case.get(ct, 0)
            v_ctrl = prop_ctrl.get(ct, 0)
            ax.bar(0, v_case, bottom=bottom_case, color=colors[ct], width=0.5)
            ax.bar(1, v_ctrl, bottom=bottom_ctrl, color=colors[ct], width=0.5)
            bottom_case += v_case
            bottom_ctrl += v_ctrl

        ax.set_xticks([0, 1])
        ax.set_xticklabels(x_labels, fontsize=14, rotation=0, ha='center')
        ax.set_ylim(0, 1)
        ax.set_ylabel('Proportion', fontsize=14)
        ax.set_title(acc, fontsize=14, pad=10)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

    n_cols = min(5, len(all_cell_types))
    handles = [mpatches.Patch(color=colors[ct], label=ct) for ct in all_cell_types]
    fig.legend(handles=handles, title='Cell Types',
               loc='upper center', bbox_to_anchor=(0.5, 0),
               ncol=n_cols, fontsize=15, title_fontsize=17, frameon=True)
    fig.suptitle(f'Cell Composition — {case_label} vs {ctrl_label}', fontsize=20, y=1.02)
    plt.tight_layout()
    n_legend_rows = -(-len(all_cell_types) // n_cols)
    plt.subplots_adjust(bottom=0.03 + n_legend_rows * 0.02)
    plt.show()


def plot_sc_dotplot(
    summary_df: pd.DataFrame,
    genes_order: list[str] | None = None,
    title: str = 'Single-cell expression · gene × cell type',
    cluster_genes: bool = True,
    cluster_cell_types: bool = True,
) -> None:
    """
    Classic gene × cell-type dot plot: size = % expressing, colour = mean.
    
    Parameters:
    - summary_df: Columns gene_id, cell_type, cell_prop, mean.
    - genes_order: Optional gene row order / subset.
    - title: Plot title.
    - cluster_genes: Cluster gene rows when genes_order is not set.
    - cluster_cell_types: Cluster cell-type columns.
    
    Returns:
    - Displays a matplotlib dot plot.
    """
    df = summary_df.copy()
    if genes_order:
        df = df[df['gene_id'].isin(genes_order)]

    size_df  = df.pivot_table(index='gene_id', columns='cell_type', values='cell_prop', aggfunc='first').fillna(0)
    color_df = df.pivot_table(index='gene_id', columns='cell_type', values='mean', aggfunc='first').fillna(0)

    if genes_order:
        idx = [g for g in genes_order if g in size_df.index]
        size_df  = size_df.reindex(idx)
        color_df = color_df.reindex(idx)
    elif cluster_genes and len(color_df) > 1:
        row_ord = leaves_list(linkage(pdist(color_df.values, metric='euclidean'), method='ward'))
        size_df  = size_df.iloc[row_ord]
        color_df = color_df.iloc[row_ord]

    if cluster_cell_types and len(color_df.columns) > 1:
        col_ord = leaves_list(linkage(pdist(color_df.values.T, metric='euclidean'), method='ward'))
        size_df  = size_df.iloc[:, col_ord]
        color_df = color_df.iloc[:, col_ord]

    n_genes, n_cts = len(size_df), len(size_df.columns)
    fig, ax = plt.subplots(figsize=(max(8, n_cts * 0.75), max(5, n_genes * 0.45)))

    vmin, vmax = color_df.values.min(), color_df.values.max()
    max_dot = 400

    for i, gene in enumerate(size_df.index):
        for j, ct in enumerate(size_df.columns):
            pct  = size_df.loc[gene, ct]
            mean = color_df.loc[gene, ct]
            norm_c = (mean - vmin) / (vmax - vmin + 1e-9)
            ax.scatter(j, i, s=pct * max_dot,
                       c=[[plt.cm.YlOrRd(0.2 + 0.8 * norm_c)]],
                       edgecolors='#aaa', linewidths=0.3, zorder=2)

    ax.set_xticks(range(n_cts))
    ax.set_xticklabels(size_df.columns, rotation=45, ha='right', fontsize=11)
    ax.set_yticks(range(n_genes))
    ax.set_yticklabels(size_df.index, fontsize=12)
    ax.invert_yaxis()
    ax.set_title(title, fontsize=16)
    ax.grid(True, color='#f0f0f0', linewidth=0.5, zorder=0)
    ax.set_facecolor('white')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    for s in [0.05, 0.25, 0.5, 1.0]:
        ax.scatter([], [], s=s * max_dot, c='#bbb', label=f'{int(s*100)}%',
                   edgecolors='#aaa', linewidths=0.3)
    ax.legend(title='% expressing', bbox_to_anchor=(1.02, 1), loc='upper left',
              fontsize=13, title_fontsize=14, framealpha=0.9)

    sm = plt.cm.ScalarMappable(cmap='YlOrRd', norm=plt.Normalize(vmin=vmin, vmax=vmax))
    sm.set_array([])

    # vertical colorbar directly below the legend — axes-fraction coords [x0, y0, width, height]
    cax = ax.inset_axes([1.02, 0.05, 0.03, 0.35])
    cbar = fig.colorbar(sm, cax=cax, orientation='vertical')
    cbar.set_label('Mean expression', fontsize=13)
    cbar.ax.tick_params(labelsize=11)

    fig.subplots_adjust(right=0.78)
    plt.show()


def plot_sc_heatmap(
    summary_df: pd.DataFrame,
    genes_order: list[str] | None = None,
    value_col: str = 'log2_fold_change',
    title: str = 'Expression specificity · gene × cell type (log2FC vs rest)',
    cluster_genes: bool = True,
    cluster_cell_types: bool = True,
) -> None:
    """
    Heatmap of a gene × cell-type summary value (default: mean expression).
    
    Parameters:
    - summary_df: Columns gene_id, cell_type, and value_col.
    - genes_order: Optional gene row order / subset.
    - value_col: Column to pivot into heatmap colours.
    - title: Plot title.
    - cluster_genes: Cluster gene rows when genes_order is not set.
    - cluster_cell_types: Cluster cell-type columns.
    
    Returns:
    - Displays a matplotlib heatmap.
    """
    df = summary_df.copy()
    if genes_order:
        df = df[df['gene_id'].isin(genes_order)]

    pivot = df.pivot_table(index='gene_id', columns='cell_type',
                           values=value_col, aggfunc='first').fillna(0)
    mean_pivot = df.pivot_table(index='gene_id', columns='cell_type',
                                values='mean', aggfunc='first').fillna(0)

    # cluster on mean expression — same basis as dotplot
    if genes_order:
        pivot      = pivot.reindex([g for g in genes_order if g in pivot.index])
        mean_pivot = mean_pivot.reindex(pivot.index)
    elif cluster_genes and len(mean_pivot) > 1:
        row_ord = leaves_list(linkage(pdist(mean_pivot.values, metric='euclidean'), method='ward'))
        pivot = pivot.iloc[row_ord]

    if cluster_cell_types and len(mean_pivot.columns) > 1:
        col_ord = leaves_list(linkage(pdist(mean_pivot.values.T, metric='euclidean'), method='ward'))
        pivot = pivot.iloc[:, col_ord]

    n_genes, n_cts = len(pivot), len(pivot.columns)
    fig, ax = plt.subplots(figsize=(max(8, n_cts * 0.75), max(5, n_genes * 0.4)))

    vmax = np.percentile(np.abs(pivot.values), 95)
    im = ax.imshow(pivot.values, cmap='RdBu_r', vmin=-vmax, vmax=vmax, aspect='auto')

    ax.set_xticks(range(n_cts))
    ax.set_xticklabels(pivot.columns, rotation=45, ha='right', fontsize=8)
    ax.set_yticks(range(n_genes))
    ax.set_yticklabels(pivot.index, fontsize=9)
    ax.set_title(title, fontsize=12)

    for i in range(n_genes):
        for j in range(n_cts):
            v = pivot.values[i, j]
            if abs(v) > vmax * 0.5:
                ax.text(j, i, f'{v:.1f}', ha='center', va='center',
                        fontsize=6, color='white' if abs(v) > vmax * 0.7 else '#333')

    fig.colorbar(im, ax=ax, shrink=0.4, label='log2FC vs rest')
    plt.tight_layout()
    plt.show()


def score_cell_specificity(
    df: pd.DataFrame,
    gene_col: str = "gene_id",
    mean_col: str = "mean",
    count_col: str = "cell_count",
    total_col: str = "total_count",
    E: float = 1e-9,
) -> pd.DataFrame:
    """
    Score how selectively each gene is expressed in each cell type vs the rest.
    
    Adds cell-specificity and log2 fold-change for ranking "which cell type owns this gene" views. 
    Cell specificity score is calculated as the product of log2 fold-change and cell proportion 
    difference, but only for genes with the same sign of log2 fold-change and cell proportion 
    difference, otherwise it is set to 0.
    
    Parameters:
    - df: Per gene × cell type summary rows.
    - gene_col: Gene ID column.
    - mean_col: Mean expression column.
    - count_col: Expressing-cell count column.
    - total_col: Total cells in that type column.
    - E: Pseudocount to avoid log(0).
    
    Returns:
    - Input copy plus specificity / lfc-vs-rest style columns
      (e.g. cell_spec_score, log2_fold_change).
    """
    out = df.copy()

    # cell counts
    total_n = out.groupby(gene_col)[count_col].transform("sum") # cells with expression
    totals_n = out.groupby(gene_col)[total_col].transform("sum") # all cells

    # log2 fold change
    wx = out[mean_col] * out[count_col]
    total_w = wx.groupby(out[gene_col]).transform("sum")
    mean_rest = (total_w - wx) / (total_n - out[count_col])
    out["mean_rest"] = mean_rest
    out["log2_fold_change"] = np.log2((out[mean_col] + E) / (mean_rest + E))

    # cell proportion difference
    out["cell_prop"] = out[count_col] / out[total_col]
    rest_total_n = total_n - out[count_col]
    rest_totals_n = totals_n - out[total_col]
    out["cell_prop_rest"] = rest_total_n / rest_totals_n
    diff = out["cell_prop"] - out["cell_prop_rest"]
    out["cell_prop_diff"] = diff

    # cell-specificity score
    lfc = out["log2_fold_change"]
    diff = out["cell_prop_diff"]
    magnitude = lfc.abs() * diff.abs()
    same_sign = (np.sign(lfc) == np.sign(diff))
    concordant = same_sign & (lfc != 0) & (diff != 0)
    out["cell_spec_score"] = np.where(concordant, np.sign(lfc) * magnitude, 0.0)

    return out


def get_top_cell_types(gene_cell_summary_df, gene, n_top=10, cell_count_threshold=5):
    """
    Get the top cell types for a given gene, ranked by specificity score and then 
    by proportion of expressing cells. Include only the ones with specificity score > 0.

    Parameters:
    - gene_cell_summary_df (pd.DataFrame): The dataframe containing the gene cell summary.
        Must contain the columns 'gene_id', 'cell_spec_score', 'cell_prop', and 'cell_count'.
    - gene (str): The gene to get the top cell types for.
    - n_top (int): The number of top cell types to return.
    - cell_count_threshold (int): The minimum cell count threshold.

    Returns:
    - pd.DataFrame: The top cell types for the given gene.
    """
    g = (
        gene_cell_summary_df[
            (gene_cell_summary_df['gene_id'] == gene)
            & (gene_cell_summary_df['cell_count'] >= cell_count_threshold)
            & (gene_cell_summary_df['cell_spec_score'] > 0)
        ]
        .sort_values(['cell_spec_score', 'cell_prop'], ascending=False)
        .head(n_top)
    )
    return g.reset_index(drop=True)


def display_gene_cell_type_shortlist(
    gene_cell_summary_df: pd.DataFrame,
    genes: list[str] | None = None,
    n_top: int = 10,
    cell_count_threshold: int = 5,
    title: str | None = None,
) -> None:
    """
    HTML table of top-specificity cell types for each gene.
    Inverse of cell_type_shortlist: one row per gene, cell-type chips from
    get_top_cell_types. The bar is that gene's best spec score, normalised
    across the genes shown.
    Parameters:
    - gene_cell_summary_df: Gene × cell-type summary (same columns as
      get_top_cell_types).
    - genes: Gene order / subset. Default = unique gene_id values.
    - n_top: Cell types to show per gene (passed to get_top_cell_types).
    - cell_count_threshold: Minimum expressing-cell count per type.
    - title: Optional card heading.
    Returns:
    - Displays the HTML shortlist table.
    """
    gene_order = (
        list(dict.fromkeys(genes))
        if genes is not None
        else list(dict.fromkeys(gene_cell_summary_df['gene_id'].tolist()))
    )
    per_gene = {
        gene: get_top_cell_types(
            gene_cell_summary_df, gene,
            n_top=n_top,
            cell_count_threshold=cell_count_threshold,
        )
        for gene in gene_order
    }
    gene_order = [g for g in gene_order if not per_gene[g].empty]
    if not gene_order:
        print('No genes to display.')
        return
    max_spec = max(float(per_gene[g]['cell_spec_score'].max()) for g in gene_order) or 1.0
    rows_html = ''
    for gene in gene_order:
        g = per_gene[gene]
        types = g['cell_type'].tolist()
        scores = g['cell_spec_score'].tolist()
        best = float(scores[0]) if scores else 0.0
        bar_w = int(100 * best / max_spec) if max_spec else 0
        extra = [f'{s:.2f}' for s in scores]
        chips = ' '.join(
            f'<span class="gct-chip">{t} <span>{e}</span></span>'
            for t, e in zip(types, extra)
        )
        rows_html += f"""
        <tr>
        <td><span class="gct-gene">{gene}</span></td>
        <td>
            <span class="gct-bar-wrap">
            <span class="gct-bar-fill" style="width:{bar_w}%"></span>
            </span>
            <span class="gct-bar-val">{best:.2f}</span>
        </td>
        <td>{chips}</td>
        </tr>
        """
    heading = title or f'Top cell types per gene ({len(gene_order)} genes)'
    display(HTML(f"""
    <style>
    .gct-wrap {{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;max-width:1100px;
                margin:0 auto;background:#ffffff;color:#1a1a2e;padding:4px 0}}
    .gct-hdr  {{border-bottom:2px solid #e5e7eb;padding-bottom:10px;margin-bottom:12px}}
    .gct-title{{font-size:17px;font-weight:700;color:#1a1a2e;margin:0}}
    .gct-sub  {{font-size:12px;color:#6b7280;margin:3px 0 0}}
    .gct-table{{width:100%;border-collapse:collapse;font-size:13px;background:#ffffff}}
    .gct-table th{{background:#f8f9fb;color:#374151;font-size:11px;font-weight:600;
                text-transform:uppercase;letter-spacing:.05em;
                padding:7px 10px;border-bottom:2px solid #e5e7eb;white-space:nowrap}}
    .gct-table td{{padding:6px 10px;border-bottom:1px solid #f0f0f0;vertical-align:middle;
                background:#ffffff;color:#1a1a2e}}
    .gct-table tr:nth-child(even) td{{background:#f9fafb}}
    .gct-table tr:hover td{{background:#f3f4f6}}
    .gct-gene{{font-weight:700;color:#1a1a2e;font-size:13px}}
    .gct-bar-wrap{{background:#f0f0f0;border-radius:3px;height:6px;width:70px;
                display:inline-block;vertical-align:middle}}
    .gct-bar-fill{{display:block;height:100%;border-radius:3px;background:#22c55e}}
    .gct-bar-val{{font-size:11px;color:#4b5563;margin-left:6px;vertical-align:middle}}
    .gct-chip{{display:inline-flex;align-items:center;gap:3px;padding:1px 7px;border-radius:10px;
            font-size:10px;font-weight:500;background:#f0f0ff;color:#3730a3;border:1px solid #c7d2fe;
            margin:1px}}
    .gct-chip span{{opacity:.7}}
    </style>
    <div style="overflow-x:auto;border:1px solid {GS_LINE};border-radius:8px;background:#ffffff">
    <div class="gct-wrap">
    <div class="gct-hdr">
        <p class="gct-title">{heading}</p>
        <p class="gct-sub">ranked by cell-specificity score</p>
    </div>
    <table class="gct-table">
        <thead>
        <tr>
            <th>Gene</th>
            <th>Best spec score</th>
            <th>Top cell types</th>
        </tr>
        </thead>
        <tbody>{rows_html}</tbody>
    </table>
    </div>
    </div>
    """))


def plot_sc_dotplot_and_cell_summary(
    df: pd.DataFrame,
    x_col: str = "mean",
    type_col: str = "cell_type",
    prop_col: str = "cell_prop",
    spec_score_col: str = "cell_spec_score",
    gene_col: str = "gene_id",
    plot_title: str = "",
    log1p_x: bool = True,
    size_range: tuple[float, float] = (20, 250),
    size_vmax: float = 0.5,
    color_vmax: float = 0.5,
    cmap: str = "YlOrRd",
) -> None:
    """
    Faceted gene×cell-type dot plots with size = % expressing, colour = specificity.
    
    One panel per gene; used to show where panel genes live among cell types.
    
    Parameters:
    - df: Gene × cell type summary with mean / prop / specificity.
    - x_col: Column for x-axis expression values.
    - type_col: Cell-type column.
    - prop_col: Fraction expressing (dot size).
    - spec_score_col: Specificity score (dot colour).
    - gene_col: Gene ID column.
    - plot_title: Figure title.
    - log1p_x: Apply log1p to x values.
    - size_range: Dot size range.
    - size_vmax: Cap for size scaling.
    - color_vmax: Cap for colour scale.
    - cmap: Matplotlib colormap name.
    
    Returns:
    - Displays a faceted matplotlib figure.
    """
    color_label, size_label = "Cell-specificity", "Cell proportion"

    plot_df = df.copy()
    genes_to_plot = plot_df[gene_col].unique().tolist()
    plot_df["_x"] = np.log1p(plot_df[x_col]) if log1p_x else plot_df[x_col]
    x_label = "log1p(Expression)" if log1p_x else "Expression"
    plot_df = plot_df.rename(columns={spec_score_col: color_label, prop_col: size_label})
    # specificity is NaN when a gene has no background to compare against -> keep marker
    plot_df[[color_label, size_label]] = plot_df[[color_label, size_label]].fillna(0.0)

    # shared scales, guarded so a single/constant value never collapses the range
    xmin, xmax = plot_df["_x"].min(), plot_df["_x"].max()
    xpad = (xmax - xmin) * 0.05 or abs(xmax) * 0.05 or 0.5
    xlim = (xmin - xpad, xmax + xpad)
    cmin = plot_df[color_label].min()
    cmax = max(plot_df[color_label].max(), color_vmax)
    smin = plot_df[size_label].min()
    smax = max(plot_df[size_label].max(), size_vmax)
    hue_norm = plt.Normalize(cmin, cmax if cmax > cmin else cmin + 1)
    size_norm = plt.Normalize(smin, smax if smax > smin else smin + 1)

    # layout in inches (converted to figure fractions only at the end)
    ROW_H, PAD_ROWS, PLOT_W = 0.25, 0.6, 5.5      # row pitch, dot padding, dots width
    TICK_FS, GENE_FS, SUP_FS, AXIS_FS, LEG_FS = 10, 12, 14, 11, 10
    LINE = 1.6 / 72                               # inches per font point, per line
    char = lambda fs: fs * 0.6 / 72               # rough character width in inches

    n = len(genes_to_plot)
    n_cats = {g: plot_df[plot_df[gene_col] == g][type_col].nunique() for g in genes_to_plot}
    axes_h = [(n_cats[g] + 2 * PAD_ROWS) * ROW_H for g in genes_to_plot]

    # left margin fits the longest cell-type label; right block holds the legend
    max_chars = max(len(str(c)) for c in plot_df["cell_type"].unique())
    left = min(max(max_chars * char(TICK_FS) + 0.2, 0.4), 4.0)
    has_legend = plot_df[color_label].nunique() > 1 or plot_df[size_label].nunique() > 1
    legend_w = 0.45 + len(color_label) * char(LEG_FS) + 0.2 if has_legend else 0.2
    fig_w = left + PLOT_W + legend_w

    # wrap the title to the figure width so it never clips
    title_lines = []
    if plot_title:
        max_line = max(int((fig_w - 0.2) / char(SUP_FS)), 8)
        cur = ""
        for w in plot_title.split():
            if cur and len(cur) + 1 + len(w) > max_line:
                title_lines.append(cur)
                cur = w
            else:
                cur = (cur + " " + w).strip()
        if cur:
            title_lines.append(cur)

    gene_title_h = GENE_FS * LINE + 0.06
    gap = gene_title_h + 0.12                     # gap separating two facets
    sup_h = len(title_lines) * SUP_FS * LINE + 0.18 if title_lines else 0.0
    top_block = sup_h + gene_title_h + 0.05       # suptitle + first facet title
    bottom_block = AXIS_FS * LINE + TICK_FS * LINE + 0.45   # x ticks + x label
    plot_region = sum(axes_h) + gap * (n - 1)

    # build the legend once from the full data so it spans the whole range
    handles = labels = None
    if has_legend:
        tmp = plt.figure()
        sns.scatterplot(
            data=plot_df, x="_x", y=type_col, hue=color_label, size=size_label,
            sizes=size_range, palette=cmap, hue_norm=hue_norm, size_norm=size_norm,
            legend="brief", edgecolor="0.3", linewidth=0.5, ax=tmp.add_subplot(111),
        )
        handles, labels = tmp.axes[0].get_legend_handles_labels()
        plt.close(tmp)
    legend_h = len(labels) * (LEG_FS * LINE + 0.075) + 0.1 if labels else 0.0

    # figure must be tall enough for BOTH facets+axis label AND the legend (which
    # sits below the title on the right) so the title and legend never overlap
    fig_h = top_block + max(plot_region + bottom_block, legend_h + 0.1)

    fig = plt.figure(figsize=(fig_w, fig_h))
    gs = fig.add_gridspec(
        n, 1, height_ratios=axes_h,
        left=left / fig_w, right=(left + PLOT_W) / fig_w,
        top=1 - top_block / fig_h,
        bottom=1 - (top_block + plot_region) / fig_h,
        hspace=gap / np.mean(axes_h),
    )
    axes = [fig.add_subplot(gs[i, 0]) for i in range(n)]

    for ax, gene in zip(axes, genes_to_plot):
        gdf = plot_df[plot_df[gene_col] == gene].copy()
        # preserve ranking order top-to-bottom on the y-axis
        gdf[type_col] = pd.Categorical(
            gdf[type_col], categories=gdf[type_col].tolist(), ordered=True
        )
        sns.scatterplot(
            data=gdf, x="_x", y=type_col, hue=color_label, size=size_label,
            sizes=size_range, size_norm=size_norm, hue_norm=hue_norm, palette=cmap,
            legend=False, edgecolor="0.3", linewidth=0.5, ax=ax,
        )
        ax.set_ylim(-0.5 - PAD_ROWS, n_cats[gene] - 0.5 + PAD_ROWS)
        ax.invert_yaxis()
        ax.set_xlim(xlim)
        ax.set_title(gene, fontsize=GENE_FS, fontweight="bold", loc="left", pad=4)
        ax.set_ylabel("")
        ax.set_xlabel("")
        ax.tick_params(axis="both", labelsize=TICK_FS)
        ax.grid(axis="x", linestyle="--", alpha=0.3)
        sns.despine(ax=ax, left=True)
        if ax is not axes[-1]:        # facets share the x scale
            ax.tick_params(labelbottom=False)
    axes[-1].set_xlabel(x_label, fontsize=AXIS_FS)

    # legend anchored to the top of the plotting area, just under the title
    if handles:
        leg = fig.legend(
            handles, labels, loc="upper left",
            bbox_to_anchor=((left + PLOT_W + 0.15) / fig_w, 1 - top_block / fig_h),
            frameon=False, labelspacing=0.6, fontsize=LEG_FS, borderaxespad=0.0,
        )
        for t in leg.get_texts():
            if t.get_text() in {color_label, size_label}:
                t.set_fontweight("bold")

    if title_lines:
        fig.suptitle(
            "\n".join(title_lines), fontsize=SUP_FS, fontweight="bold",
            x=0.12 / fig_w, ha="left", va="top", y=1 - 0.06 / fig_h,
        )

    plt.show()


def plot_sc_dotplot_and_cell_summary_source_comparison(
    combined_top_df: pd.DataFrame,
    per_study_top_dfs: list[pd.DataFrame],
    genes: list[str],
    log1p_x: bool = False,
    dot_size_scale: float = 350,
    cmap: str = 'YlOrRd',
) -> None:
    """
    Grid of gene×cell-type dots comparing combined cohort vs per-study slices.
    
    Rows = genes; columns = combined + each study. Used to show whether
    cell-type expression patterns replicate across datasets.
    
    Parameters:
    - combined_top_df: Combined-cohort top cell types per gene
      (gene_id, cell_type, mean, cell_prop, cell_spec_score).
    - per_study_top_dfs: Per-study DataFrames with the same columns.
    - genes: Genes (rows) to display.
    - log1p_x: Apply log1p to mean expression on the x-axis.
    - dot_size_scale: Multiplier for cell_prop → marker size.
    - cmap: Colormap for specificity colouring.
    
    Returns:
    - Displays a matplotlib grid figure.
    """
    sources = [('Combined', combined_top_df)] + per_study_top_dfs
    n_sources = len(sources)
    genes_present = [g for g in genes if combined_top_df['gene_id'].eq(g).any()]
    n_genes = len(genes_present)

    if not genes_present:
        print("No genes found in combined data.")
        return

    ct_orders = {
        gene: (
            combined_top_df[combined_top_df['gene_id'] == gene]
            .sort_values(['cell_spec_score', 'cell_prop'], ascending=False)
            ['cell_type'].tolist()
        )
        for gene in genes_present
    }

    _nonempty = [df for _, df in sources if not df.empty]
    all_scores = pd.concat(_nonempty)['cell_spec_score'].clip(lower=0)
    color_vmax = max(float(all_scores.quantile(0.95)), 1e-6)
    cmap_obj = plt.get_cmap(cmap)
    norm = plt.Normalize(0, color_vmax)

    row_heights = [max(len(ct_orders[g]) * 0.35 + 0.1, 0.5) for g in genes_present]
    col_w = 2.5
    left_margin = 2.2
    right_margin = 1.2
    fig_w = left_margin + n_sources * col_w + right_margin
    fig_h = sum(row_heights) + 1.0

    title_space = 0.3 / fig_h
    TOP = 1.0 - title_space

    fig, axes = plt.subplots(
        n_genes, n_sources,
        figsize=(fig_w, fig_h),
        dpi=150,
        gridspec_kw={'height_ratios': row_heights, 'hspace': 0.15, 'wspace': 0.05},
        sharex='row', sharey='row',
    )
    fig.subplots_adjust(
        left=left_margin/fig_w,
        right=(fig_w - right_margin)/fig_w,
        top=TOP, bottom=0.04
    )

    if n_genes == 1 and n_sources == 1:
        axes = np.array([[axes]])
    elif n_genes == 1:
        axes = axes[np.newaxis, :]
    elif n_sources == 1:
        axes = axes[:, np.newaxis]

    for row_i, gene in enumerate(genes_present):
        ct_order = ct_orders[gene]
        n_cts    = len(ct_order)
        ct_pos   = {ct: i for i, ct in enumerate(ct_order)}

        ax0 = axes[row_i, 0]
        ax0.set_yticks(range(n_cts))
        ax0.set_yticklabels(ct_order, fontsize=13)
        ax0.set_ylim(-0.5, n_cts - 0.5)
        ax0.invert_yaxis()
        ax0.set_ylabel(gene, fontsize=15, fontweight='bold', labelpad=6)

        all_x = []
        for _, df in sources:
            if df.empty:
                continue
            gdf = df[df['gene_id'] == gene]
            if len(gdf):
                vals = np.log1p(gdf['mean'].values) if log1p_x else gdf['mean'].values
                all_x.extend(vals.tolist())
        if all_x:
            xpad = (max(all_x) - min(all_x)) * 0.12 or 0.05
            ax0.set_xlim(min(all_x) - xpad, max(all_x) + xpad)

        for col_i, (label, df) in enumerate(sources):
            ax = axes[row_i, col_i]

            if col_i > 0:
                ax.tick_params(labelleft=False)
            if row_i == 0:
                ax.set_title(label, fontsize=14, fontweight='bold', pad=5)

            gdf = pd.DataFrame() if df.empty else df[df['gene_id'] == gene].copy()
            if gdf.empty:
                ax.text(0.5, 0.5, '—', ha='center', va='center',
                        transform=ax.transAxes, fontsize=18, color='#ccc')
            else:
                x_vals = np.log1p(gdf['mean'].values) if log1p_x else gdf['mean'].values
                y_vals = np.array([ct_pos.get(ct, np.nan) for ct in gdf['cell_type']])
                valid  = ~np.isnan(y_vals)
                ax.scatter(
                    x_vals[valid], y_vals[valid],
                    s=(gdf['cell_prop'].values[valid] * dot_size_scale).clip(min=15),
                    c=cmap_obj(norm(gdf['cell_spec_score'].clip(lower=0).values[valid])),
                    edgecolors='#444', linewidths=0.3, alpha=0.9, zorder=3,
                )

            ax.set_facecolor('white')
            ax.grid(axis='x', linestyle='--', linewidth=0.4, alpha=0.35, zorder=0)
            ax.spines[['top', 'right', 'left']].set_visible(False)
            ax.tick_params(axis='x', labelsize=12)
            if row_i < n_genes - 1:
                ax.tick_params(labelbottom=False)
            elif col_i == n_sources // 2:
                ax.set_xlabel('log1p(mean)' if log1p_x else 'Mean expression', fontsize=13)

    right_edge = (fig_w - right_margin) / fig_w
    cbar_x = right_edge + 0.10 / fig_w

    cbar_h = 2.2 / fig_h
    cbar_w = 0.15 / fig_w
    cbar_y = TOP - 0.05 / fig_h - cbar_h

    cbar_ax = fig.add_axes([cbar_x, cbar_y, cbar_w, cbar_h])
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(0, color_vmax))
    sm.set_array([])
    cb = fig.colorbar(sm, cax=cbar_ax)
    cb.set_label('Specificity\nscore', fontsize=13, labelpad=3)
    cb.ax.tick_params(labelsize=12)

    leg_h = 1.3 / fig_h
    leg_w = 0.8 / fig_w
    leg_y = cbar_y - 0.4 / fig_h - leg_h

    leg_ax = fig.add_axes([cbar_x - 0.02 / fig_w, leg_y, leg_w, leg_h])
    leg_ax.set_axis_off()
    for pct, txt in [(0.1, '10%'), (0.25, '25%'), (0.5, '50%')]:
        leg_ax.scatter([], [], s=pct * dot_size_scale, c='#bbb',
                      edgecolors='#555', linewidths=0.3, label=txt, alpha=0.9)
    leg_ax.legend(title='% cells\nexpr.', title_fontsize=13, fontsize=13,
                 frameon=False, loc='center left')

    plt.show()


def plot_sc_de_panel(
    de_results_dict: dict,
    genes: list[str],
    fdr_threshold: float = 0.05,
    log2fc_threshold: float = 0.25,
    cluster_genes: bool = True,
    cluster_cell_types: bool = True,
    title: str = 'Panel gene DE · SC (log2FC colour · dot size = −log10 FDR)',
) -> None:
    """
    Dot-style panel of SC DE across cell types for selected genes.
    
    Colour = log2FC; size / greying encodes significance (FDR and |log2FC|).
    
    Parameters:
    - de_results_dict: cell type → DE DataFrame (gene_id, log2_fc, fdr).
    - genes: Genes to show as rows.
    - fdr_threshold: FDR cutoff for calling significance.
    - log2fc_threshold: |log2FC| cutoff for calling significance.
    - cluster_genes: Cluster gene rows.
    - cluster_cell_types: Cluster cell-type columns.
    - title: Plot title.
    
    Returns:
    - Displays a matplotlib DE panel.
    """

    # build pivot tables: genes × cell types
    fc_data, fdr_data = {}, {}
    for ct, de in de_results_dict.items():
        sub = de[de['gene_id'].isin(genes)].set_index('gene_id')
        fc_data[ct]  = sub['log2_fc'].reindex(genes)
        fdr_data[ct] = sub['fdr'].reindex(genes)

    fc_df  = pd.DataFrame(fc_data,  index=genes).fillna(0)
    fdr_df = pd.DataFrame(fdr_data, index=genes).fillna(1.0)
    sig_df = (fdr_df < fdr_threshold) & (fc_df.abs() >= log2fc_threshold)

    # drop cell types with no significant hits
    keep_cts = sig_df.columns[sig_df.any(axis=0)]
    if keep_cts.empty:
        print(
            "No cell types with significant hits "
            f"(FDR < {fdr_threshold}, |log2FC| ≥ {log2fc_threshold})."
        )
        return
    fc_df  = fc_df[keep_cts]
    fdr_df = fdr_df[keep_cts]
    sig_df = sig_df[keep_cts]

    # cluster on significant log2FC only
    cluster_mat = fc_df.where(sig_df, 0)
    if cluster_cell_types and len(fc_df.columns) > 1:
        col_ord = leaves_list(linkage(pdist(cluster_mat.values.T, metric='euclidean'), method='ward'))
        fc_df  = fc_df.iloc[:, col_ord]
        fdr_df = fdr_df.iloc[:, col_ord]
        sig_df = sig_df.iloc[:, col_ord]
    if cluster_genes and len(fc_df) > 1:
        row_ord = leaves_list(linkage(pdist(cluster_mat.values, metric='euclidean'), method='ward'))
        fc_df  = fc_df.iloc[row_ord]
        fdr_df = fdr_df.iloc[row_ord]
        sig_df = sig_df.iloc[row_ord]

    n_genes, n_cts = len(fc_df), len(fc_df.columns)
    fig, ax = plt.subplots(figsize=(max(6, n_cts * 0.9), max(5, n_genes * 0.45)))

    neg_log_fdr = -np.log10(fdr_df.clip(lower=1e-4))
    s_max = neg_log_fdr.values.max() or 1
    max_dot = 400
    vmax = max(fc_df.values.max(), abs(fc_df.values.min()), 1.0)

    for i, gene in enumerate(fc_df.index):
        for j, ct in enumerate(fc_df.columns):
            fc   = fc_df.loc[gene, ct]
            s    = neg_log_fdr.loc[gene, ct] / s_max * max_dot
            sig  = sig_df.loc[gene, ct]
            norm_c = (fc + vmax) / (2 * vmax + 1e-9)
            color = plt.cm.RdBu_r(np.clip(norm_c, 0, 1)) if sig else '#dddddd'
            ec    = '#444' if sig else '#bbb'
            ax.scatter(j, i, s=max(s, 8),
                       c=[color], edgecolors=ec,
                       linewidths=0.5 if sig else 0.3,
                       alpha=0.9 if sig else 0.5, zorder=2)

    ax.set_xticks(range(n_cts))
    ax.set_xticklabels(fc_df.columns, rotation=40, ha='right', fontsize=9)
    ax.set_yticks(range(n_genes))
    ax.set_yticklabels(fc_df.index, fontsize=9)
    ax.invert_yaxis()
    ax.set_title(title, fontsize=11, pad=10)
    ax.grid(True, color='#f0f0f0', linewidth=0.5, zorder=0)
    ax.set_facecolor('white')
    ax.spines[['top', 'right']].set_visible(False)

    # size legend
    for fdr_val, lbl in [(0.05, 'FDR=0.05'), (0.01, 'FDR=0.01'), (0.001, 'FDR=0.001')]:
        s_leg = -np.log10(fdr_val) / s_max * max_dot
        ax.scatter([], [], s=s_leg, c='#999', edgecolors='#555',
                   linewidths=0.4, label=lbl)
    ax.legend(title='Significance', bbox_to_anchor=(1.02, 1), loc='upper left',
              fontsize=8, frameon=False)

    # colour bar
    sm = plt.cm.ScalarMappable(cmap='RdBu_r', norm=plt.Normalize(vmin=-vmax, vmax=vmax))
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax, shrink=0.4, pad=0.18)
    cbar.set_label('log2FC', fontsize=9)

    # note on grey dots
    ax.text(1.02, 0.02, '● grey = not significant', transform=ax.transAxes,
            fontsize=7.5, color='#999', va='bottom')

    plt.tight_layout()
    plt.show()


def plot_sc_de_panel_heatmap(
    de_results_dict: dict,
    genes: list[str],
    fdr_threshold: float = 0.05,
    log2fc_threshold: float = 0.25,
    cluster_genes: bool = True,
    cluster_cell_types: bool = True,
    title: str = 'Panel gene DE · SC log2FC (∗ FDR significant)',
) -> None:
    """
    Heatmap of SC log2FC across cell types for selected genes.
    
    Significant cells (FDR and |log2FC|) are emphasised; others muted.
    
    Parameters:
    - de_results_dict: cell type → DE DataFrame (gene_id, log2_fc, fdr).
    - genes: Genes to show as rows.
    - fdr_threshold: FDR cutoff.
    - log2fc_threshold: |log2FC| cutoff.
    - cluster_genes: Cluster gene rows.
    - cluster_cell_types: Cluster cell-type columns.
    - title: Plot title.
    
    Returns:
    - Displays a matplotlib heatmap.
    """
    fc_data, fdr_data = {}, {}
    for ct, de in de_results_dict.items():
        sub = de[de['gene_id'].isin(genes)].set_index('gene_id')
        fc_data[ct]  = sub['log2_fc'].reindex(genes)
        fdr_data[ct] = sub['fdr'].reindex(genes)

    fc_df  = pd.DataFrame(fc_data,  index=genes).fillna(0)
    fdr_df = pd.DataFrame(fdr_data, index=genes).fillna(1.0)
    sig_df = (fdr_df < fdr_threshold) & (fc_df.abs() >= log2fc_threshold)

    keep_cts = sig_df.columns[sig_df.any(axis=0)]
    if keep_cts.empty:
        print(
            "No cell types with significant hits "
            f"(FDR < {fdr_threshold}, |log2FC| ≥ {log2fc_threshold})."
        )
        return
    fc_df  = fc_df[keep_cts]
    fdr_df = fdr_df[keep_cts]
    sig_df = sig_df[keep_cts]

    cluster_mat = fc_df.where(sig_df, 0)
    if cluster_cell_types and len(fc_df.columns) > 1:
        col_ord = leaves_list(linkage(pdist(cluster_mat.values.T, metric='euclidean'), method='ward'))
        fc_df  = fc_df.iloc[:, col_ord]
        sig_df = sig_df.iloc[:, col_ord]
    if cluster_genes and len(fc_df) > 1:
        row_ord = leaves_list(linkage(pdist(cluster_mat.values, metric='euclidean'), method='ward'))
        fc_df  = fc_df.iloc[row_ord]
        sig_df = sig_df.iloc[row_ord]

    n_genes, n_cts = len(fc_df), len(fc_df.columns)
    fig, ax = plt.subplots(figsize=(max(6, n_cts * 0.9), max(5, n_genes * 0.45)))

    vmax = max(fc_df.values.max(), abs(fc_df.values.min()), 1.0)
    im = ax.imshow(fc_df.values, cmap='RdBu_r', vmin=-vmax, vmax=vmax, aspect='auto')

    for i in range(n_genes):
        for j in range(n_cts):
            if sig_df.values[i, j]:
                ax.text(j, i, '∗', ha='center', va='center',
                        fontsize=11, color='white', fontweight='bold')

    ax.set_xticks(range(n_cts))
    ax.set_xticklabels(fc_df.columns, rotation=40, ha='right', fontsize=9)
    ax.set_yticks(range(n_genes))
    ax.set_yticklabels(fc_df.index, fontsize=9)
    ax.set_title(title, fontsize=11, pad=10)

    cbar = fig.colorbar(im, ax=ax, shrink=0.4, pad=0.18)
    cbar.set_label('log2FC', fontsize=9)
    ax.text(1.02, 0.02, '∗ FDR < threshold', transform=ax.transAxes,
            fontsize=7.5, color='#666', va='bottom')

    plt.tight_layout()
    plt.show()


def plot_bulk_sc_de_comparison(
    bulk_de_results: dict,
    sc_de_results: dict,
    genes: list[str],
    fdr_threshold: float = 0.05,
    bulk_log2fc_threshold: float = 1.0,
    sc_log2fc_threshold: float = 0.25,
    cluster_genes: bool = True,
    cluster_cell_types: bool = True,
    title: str = 'Bulk vs Single-Cell DE · panel genes',
) -> None:
    """
    Side-by-side log2FC heatmaps: bulk studies vs single-cell cell types.
    
    Left panel = bulk DE across datasets; right panel = SC DE within cell types.
    Shared gene row order (optionally clustered from bulk); ∗ marks cells
    passing FDR and |log2FC| for that modality.
    
    Parameters:
    - bulk_de_results: study label → DE DataFrame (gene_id, log2_fc, fdr).
    - sc_de_results: cell type → DE DataFrame (gene_id, log2_fc, fdr).
    - genes: Gene panel to compare.
    - fdr_threshold: FDR cutoff for ∗ markers.
    - bulk_log2fc_threshold: |log2FC| cutoff on the bulk panel.
    - sc_log2fc_threshold: |log2FC| cutoff on the SC panel.
    - cluster_genes: Cluster gene rows from bulk signal.
    - cluster_cell_types: Cluster SC cell-type columns from significant log2FC.
    - title: Figure title.
    
    Returns:
    - Displays a two-panel matplotlib figure.
    """
    def _build_pivots(de_dict, log2fc_threshold):
        fc, fdr = {}, {}
        for label, de in de_dict.items():
            sub = de[de['gene_id'].isin(genes)].set_index('gene_id')
            fc[label]  = sub['log2_fc'].reindex(genes)
            fdr[label] = sub['fdr'].reindex(genes)
        fc_df  = pd.DataFrame(fc,  index=genes).fillna(0)
        fdr_df = pd.DataFrame(fdr, index=genes).fillna(1.0)
        sig_df = (fdr_df < fdr_threshold) & (fc_df.abs() >= log2fc_threshold)
        return fc_df, sig_df

    bulk_fc, bulk_sig = _build_pivots(bulk_de_results, bulk_log2fc_threshold)
    sc_fc,   sc_sig   = _build_pivots(sc_de_results,   sc_log2fc_threshold)

    keep_cts = sc_sig.columns[sc_sig.any(axis=0)]
    if keep_cts.empty:
        print(
            "No cell types with significant hits "
            f"(FDR < {fdr_threshold}, |log2FC| ≥ {sc_log2fc_threshold})."
        )
    sc_fc  = sc_fc[keep_cts]
    sc_sig = sc_sig[keep_cts]

    if cluster_cell_types and len(sc_fc.columns) > 1:
        cluster_mat = sc_fc.where(sc_sig, 0)
        col_ord = leaves_list(linkage(pdist(cluster_mat.values.T, metric='euclidean'), method='ward'))
        sc_fc  = sc_fc.iloc[:, col_ord[::-1]]
        sc_sig = sc_sig.iloc[:, col_ord[::-1]]

    if cluster_genes and len(bulk_fc) > 1:
        cluster_mat = bulk_fc.where(bulk_sig, 0)
        row_ord  = leaves_list(linkage(pdist(cluster_mat.values, metric='euclidean'), method='ward'))
        bulk_fc  = bulk_fc.iloc[row_ord]
        bulk_sig = bulk_sig.iloc[row_ord]
        sc_fc    = sc_fc.iloc[row_ord]
        sc_sig   = sc_sig.iloc[row_ord]

    n_genes = len(bulk_fc)
    n_bulk  = len(bulk_fc.columns)
    n_sc    = len(sc_fc.columns)
    bulk_w  = max(2.5, n_bulk * 1.1)
    sc_w    = max(4.0, n_sc   * 0.85)
    fig_h   = max(5, n_genes * 0.45)

    fig, (ax_bulk, ax_sc) = plt.subplots(
        1, 2, figsize=(bulk_w + sc_w + 1.5, fig_h),
        sharey=True,
        gridspec_kw={'width_ratios': [n_bulk, n_sc], 'wspace': 0.08},
        constrained_layout=True,
    )

    # separate scales per modality
    bulk_vmax = max(bulk_fc.values.max(), abs(bulk_fc.values.min()), bulk_log2fc_threshold)
    sc_vmax   = max(sc_fc.values.max(),   abs(sc_fc.values.min()),   sc_log2fc_threshold)
    cmap = 'RdBu_r'

    cbars = {}
    for ax, fc_df, sig_df, vmax, subtitle in [
        (ax_bulk, bulk_fc, bulk_sig, bulk_vmax, 'Bulk RNA-seq'),
        (ax_sc,   sc_fc,   sc_sig,   sc_vmax,   'Single-cell (per cell type)'),
    ]:
        norm = plt.Normalize(vmin=-vmax, vmax=vmax)
        im = ax.imshow(fc_df.values, cmap=cmap, norm=norm, aspect='auto')
        for i in range(len(fc_df)):
            for j in range(len(fc_df.columns)):
                if sig_df.values[i, j]:
                    ax.text(j, i, '∗', ha='center', va='center',
                            fontsize=15, color='white', fontweight='bold')
        ax.set_xticks(range(len(fc_df.columns)))
        ax.set_xticklabels(fc_df.columns, rotation=40, ha='right', fontsize=13)
        ax.set_yticks(range(n_genes))
        ax.set_yticklabels(fc_df.index, fontsize=13)
        ax.tick_params(axis='y', labelleft=True, left=True)
        ax.set_title(subtitle, fontsize=15, pad=8)
        ax.spines[['top', 'right', 'bottom', 'left']].set_visible(False)
        cbar = fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap),
                            ax=ax, shrink=0.5, pad=0.03)
        cbar.set_label('log2FC', fontsize=13)
        cbar.ax.tick_params(labelsize=12)
        cbars[subtitle] = cbar

    fig.canvas.draw()  # finalize constrained_layout so positions below are accurate
    bulk_cbar_x1 = cbars['Bulk RNA-seq'].ax.get_position().x1
    sc_ax_x0     = ax_sc.get_position().x0
    sep_x = (bulk_cbar_x1 + sc_ax_x0) / 2

    fig.add_artist(plt.Line2D(
        [sep_x, sep_x], [0.06, 0.95],
        transform=fig.transFigure, color='#888', linewidth=1.2, linestyle='--'
    ))

    ax_bulk.text(
        -0.3, -0.32,
        f'* |logFC| >= {bulk_log2fc_threshold}, FDR < {fdr_threshold}',
        transform=ax_bulk.transAxes, fontsize=12, color='#666',
    )
    ax_sc.text(
        0, -0.32,
        f'* |logFC| >= {sc_log2fc_threshold}, FDR < {fdr_threshold}',
        transform=ax_sc.transAxes, fontsize=12, color='#666',
    )

    fig.suptitle(title, fontsize=18)
    fig.get_layout_engine().set(h_pad=0.1)
    plt.show()


def display_bulk_sc_de_comparison_panel(
    genes_panel: list[str],
    de_results_bulk: dict,
    de_results_sc: dict,
    bulk_sig_genes: set | None = None,
    fdr_threshold: float = 0.05,
    log2fc_threshold: float = 0.5,
    sc_fdr_thresh: float = 0.05,
    sc_log2fc_thresh: float = 0.25,
    require_both_studies: bool = False,
    genes_from_panel: bool = False,
    title: str = 'Candidate Gene Panel',
    subtitle: str = 'Genes differentially expressed (Case vs Control)',
) -> None:
    """
    Interactive HTML panel reconciling bulk-significant genes with SC cell-type DE.
    
    Per-gene view of whether bulk hits appear in single-cell DE (and in which
    cell types), for the Step 4 "bulk vs SC" talking point.
    
    Parameters:
    - genes_panel: Gene panel order / membership.
    - de_results_bulk: study → bulk DE DataFrame.
    - de_results_sc: cell type → SC DE DataFrame.
    - bulk_sig_genes: Genes called significant in bulk.
    - fdr_threshold: Bulk FDR threshold.
    - log2fc_threshold: Bulk |log2FC| threshold.
    - sc_fdr_thresh: SC FDR threshold.
    - sc_log2fc_thresh: SC |log2FC| threshold.
    - require_both_studies: Require concordance across bulk studies.
    - genes_from_panel: Restrict listing to the gene panel.
    - title: Panel title.
    - subtitle: Panel subtitle.
    
    Returns:
    - Displays the interactive HTML comparison panel.
    """
    _uid = uuid.uuid4().hex[:8]

    panel_set  = set(genes_panel)
    study_keys = list(de_results_bulk.keys())

    study_labels = [_short_label(k) for k in study_keys]

    if bulk_sig_genes is None:
        study_sig = []
        for k, de in de_results_bulk.items():
            mask = (de['fdr'] < fdr_threshold) & (de['log2_fc'].abs() >= log2fc_threshold)
            study_sig.append(set(de[mask]['gene_id'].tolist()))
        if require_both_studies and len(study_sig) > 1:
            bulk_sig_genes = study_sig[0].intersection(*study_sig[1:])
        else:
            bulk_sig_genes = set().union(*study_sig) if study_sig else set()

    sc_lookup = {}
    for cell_type, de in de_results_sc.items():
        mask = (de['fdr'] < sc_fdr_thresh) & (de['log2_fc'].abs() >= sc_log2fc_thresh)
        for _, row in de[mask].iterrows():
            g = row['gene_id']
            sc_lookup.setdefault(g, []).append({
                'ct': cell_type,
                'lfc': round(float(row['log2_fc']), 3),
                'fdr': float(row['fdr'])
            })

    all_genes = panel_set if genes_from_panel else (panel_set | bulk_sig_genes)

    _source_order = ['Bulk + Single-cell', 'Panel + Bulk', 'Single-cell only',
                     'Original panel', 'Bulk + SC', 'Bulk DEG']

    def get_concordance(in_bulk, in_sc):
        if in_bulk and in_sc:     return 'Concordant'
        if in_bulk and not in_sc: return 'Bulk only'
        if not in_bulk and in_sc: return 'Discordant'
        return 'Panel only'

    rows_data = []
    for gene in sorted(all_genes):
        in_panel = gene in panel_set
        in_bulk  = gene in bulk_sig_genes
        in_sc    = gene in sc_lookup

        if   in_panel and in_bulk and in_sc: source = 'Bulk + Single-cell'
        elif in_panel and in_bulk:           source = 'Panel + Bulk'
        elif in_panel and in_sc:             source = 'Single-cell only'
        elif in_panel:                       source = 'Original panel'
        elif in_bulk  and in_sc:             source = 'Bulk + SC'
        else:                                source = 'Bulk DEG'

        bulk = []
        for k in study_keys:
            de    = de_results_bulk[k]
            match = de[de['gene_id'] == gene]
            if len(match):
                r     = match.iloc[0]
                lfc   = round(float(r['log2_fc']), 3)
                fdr_v = float(r['fdr'])
                bulk.append({'lfc': lfc, 'fdr': fdr_v,
                             'sig': (fdr_v < fdr_threshold) and (abs(lfc) >= log2fc_threshold)})
            else:
                bulk.append(None)

        rows_data.append({
            'gene':        gene,
            'source':      source,
            'concordance': get_concordance(in_bulk, in_sc),
            'bulk':        bulk,
            'sc':          sc_lookup.get(gene, []),
        })

    rows_data.sort(key=lambda r: (_source_order.index(r['source']), r['gene']))

    source_counts      = Counter(r['source'] for r in rows_data)
    n_genes            = len(rows_data)
    rows_json          = json.dumps(rows_data)
    study_labels_json  = json.dumps(study_labels)
    source_order_json  = json.dumps(_source_order)
    source_counts_json = json.dumps(dict(source_counts))

    # ONE column per study (sort by log2FC)
    study_th = ''.join(
        f'<th onclick="sortBy_{_uid}({3 + i})">{lbl} <span class="sa">↕</span></th>'
        for i, lbl in enumerate(study_labels)
    )
    base = 3 + len(study_labels)   # SC column index

    html = f"""
<style>
.ph-wrap {{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;max-width:1200px;margin:0 auto;
           background:#ffffff;color:#1a1a2e;padding:4px 0}}
.ph-hdr  {{border-bottom:2px solid #e5e7eb;padding-bottom:10px;margin-bottom:12px}}
.ph-title{{font-size:17px;font-weight:700;color:#1a1a2e;margin:0}}
.ph-sub  {{font-size:12px;color:#6b7280;margin:3px 0 8px}}
.ph-chips{{display:flex;flex-wrap:wrap;gap:5px;margin-bottom:10px}}
.hdr-chip{{padding:2px 10px;border-radius:12px;font-size:11px;font-weight:600;border:1px solid transparent}}

.ph-filters{{display:flex;gap:6px;margin-bottom:10px;flex-wrap:wrap;align-items:center}}
.flt-label{{font-size:11px;color:#9ca3af;font-weight:600;text-transform:uppercase;
            letter-spacing:.05em;margin-right:2px}}
.ph-btn  {{padding:4px 12px;border-radius:6px;border:1px solid #d1d5db;background:white;
           font-size:11px;cursor:pointer;color:#374151;font-weight:500;transition:all .15s}}
.ph-btn:hover{{background:#f9fafb}}
.ph-btn.active{{background:#1a1a2e;color:white;border-color:#1a1a2e}}
.ph-sep  {{width:1px;height:20px;background:#e5e7eb;margin:0 4px}}
.ph-search{{padding:4px 10px;border-radius:6px;border:1px solid #d1d5db;font-size:11px;
            outline:none;width:150px;color:#374151;background:#ffffff}}
.ph-search:focus{{border-color:#6366f1;box-shadow:0 0 0 2px #e0e7ff}}

.ph-table{{width:100%;border-collapse:collapse;font-size:13px;background:#ffffff}}
.ph-table th{{background:#f8f9fb;color:#374151;font-size:11px;font-weight:600;
              text-transform:uppercase;letter-spacing:.05em;
              padding:7px 10px;border-bottom:2px solid #e5e7eb;
              white-space:nowrap;cursor:pointer;user-select:none}}
.ph-table th:hover{{background:#eff2f7}}
.ph-table th .sa{{color:#9ca3af;margin-left:3px;font-size:10px}}
.ph-table td{{padding:6px 10px;border-bottom:1px solid #f0f0f0;vertical-align:middle;
              background:#ffffff;color:#1a1a2e}}
.ph-table tr:nth-child(even) td{{background:#f9fafb}}
.ph-table tr:hover td{{background:#f3f4f6}}
.ph-table tr.row-disc td{{background:#fffbeb}}
.ph-table tr.row-disc:hover td{{background:#fef3c7}}
.ph-table tr.row-disc:nth-child(even) td{{background:#fff8e7}}
.ph-table tr.row-disc:nth-child(even):hover td{{background:#fef3c7}}

.gene-name{{font-weight:700;color:#1a1a2e;font-size:13px}}

.src-badge{{display:inline-block;padding:2px 9px;border-radius:10px;
            font-size:10px;font-weight:700;white-space:nowrap}}
.src-pbs{{background:#cffafe;color:#0e7490;border:1px solid #67e8f9}}
.src-pb {{background:#dbeafe;color:#1e40af;border:1px solid #93c5fd}}
.src-ps {{background:#fef3c7;color:#92400e;border:1px solid #fcd34d}}
.src-op {{background:#f3f4f6;color:#374151;border:1px solid #d1d5db}}
.src-bs {{background:#ede9fe;color:#5b21b6;border:1px solid #c4b5fd}}
.src-bd {{background:#dbeafe;color:#1e40af;border:1px solid #93c5fd}}

.conc-badge{{display:inline-block;padding:2px 9px;border-radius:10px;
             font-size:10px;font-weight:700;white-space:nowrap}}
.conc-concordant{{background:#d1fae5;color:#065f46;border:1px solid #6ee7b7}}
.conc-discordant{{background:#fff3cd;color:#92400e;border:1px solid #fcd34d}}
.conc-bulk_only {{background:#dbeafe;color:#1e40af;border:1px solid #93c5fd}}
.conc-panel_only{{background:#f3f4f6;color:#6b7280;border:1px solid #d1d5db}}

.lfc-up{{color:#dc2626;font-weight:700}} .lfc-dn{{color:#2563eb;font-weight:700}}
.lfc-ns{{color:#9ca3af;font-weight:400}}
.fdr-val{{font-size:10px;color:#9ca3af;margin-top:1px}}
.fdr-sig-val{{font-size:10px;color:#374151;font-weight:600;margin-top:1px}}
.na-val {{color:#d1d5db;font-style:italic;font-size:11px}}

.sc-chips{{display:flex;flex-wrap:wrap;gap:3px}}
.sc-chip {{display:inline-flex;align-items:center;gap:3px;padding:1px 7px;border-radius:10px;
           font-size:10px;font-weight:500;background:#f0f0ff;color:#3730a3;border:1px solid #c7d2fe}}
.sc-up{{color:#dc2626}} .sc-dn{{color:#2563eb}}
</style>

<div class="ph-wrap">
  <div class="ph-hdr">
    <p class="ph-title">{title}</p>
    <p class="ph-sub">{subtitle}</p>
    <div class="ph-chips" id="srcChips_{_uid}"></div>
  </div>

  <div class="ph-filters">
    <span class="flt-label">Concordance:</span>
    <button class="ph-btn active" onclick="setFilter_{_uid}('concordance','all',this)">All ({n_genes})</button>
    <button class="ph-btn" onclick="setFilter_{_uid}('concordance','Concordant',this)">Concordant</button>
    <button class="ph-btn" onclick="setFilter_{_uid}('concordance','Discordant',this)">Discordant</button>
    <div class="ph-sep"></div>
    <input class="ph-search" type="text" id="phSearch_{_uid}" placeholder="Search gene…"
           oninput="window['renderTable_{_uid}']()">
  </div>

  <div style="overflow-x:auto">
  <table class="ph-table">
    <thead><tr>
      <th onclick="sortBy_{_uid}(0)">Gene <span class="sa">↕</span></th>
      <th onclick="sortBy_{_uid}(1)">Source <span class="sa">↕</span></th>
      <th onclick="sortBy_{_uid}(2)">Concordance <span class="sa">↕</span></th>
      {study_th}
      <th onclick="sortBy_{_uid}({base})">SC cell types <span class="sa">↕</span></th>
    </tr></thead>
    <tbody id="phTbody_{_uid}"></tbody>
  </table>
  </div>
</div>

<script>
(function() {{
  const ROWS          = {rows_json};
  const STUDY_LABELS  = {study_labels_json};
  const SOURCE_ORDER  = {source_order_json};
  const SOURCE_COUNTS = {source_counts_json};
  const CONC_ORDER    = ['Concordant','Discordant','Bulk only','Panel only'];
  const N_STUDIES     = STUDY_LABELS.length;
  const BASE          = {base};
  const TBODY_ID      = 'phTbody_{_uid}';
  const CHIPS_ID      = 'srcChips_{_uid}';

  const SRC_CLS = {{
    'Bulk + Single-cell': 'src-pbs',
    'Panel + Bulk':       'src-pb',
    'Single-cell only':   'src-ps',
    'Original panel':     'src-op',
    'Bulk + SC':          'src-bs',
    'Bulk DEG':           'src-bd'
  }};
  const CONC_CLS = {{
    'Concordant':  'conc-concordant',
    'Discordant':  'conc-discordant',
    'Bulk only':   'conc-bulk_only',
    'Panel only':  'conc-panel_only'
  }};

  let filterKey = 'concordance', filterVal = 'all';
  let sortCol = 2, sortAsc = true;

  try {{
    const el = document.getElementById(CHIPS_ID);
    if (el) {{
      const total = document.createElement('span');
      total.className = 'hdr-chip';
      total.style.cssText = 'background:#1a1a2e;color:white;border-color:#1a1a2e';
      total.textContent = ROWS.length + ' genes';
      el.appendChild(total);
      SOURCE_ORDER.forEach(src => {{
        const c = SOURCE_COUNTS[src];
        if (!c) return;
        const span = document.createElement('span');
        span.className = 'hdr-chip';
        span.textContent = c + ' ' + src;
        el.appendChild(span);
      }});
    }}
  }} catch(e) {{ console.warn('panel chips:', e); }}

  function bulkCols(bulk) {{
    return bulk.map(b => {{
      if (!b) return '<td class="na-val">—</td>';
      const lfc    = (b.lfc >= 0 ? '+' : '') + b.lfc.toFixed(2);
      const lfcCls = b.sig ? (b.lfc >= 0 ? 'lfc-up' : 'lfc-dn') : 'lfc-ns';
      const fdrStr = b.fdr < 0.001 ? b.fdr.toExponential(1) : b.fdr.toFixed(3);
      const fdrCls = b.sig ? 'fdr-sig-val' : 'fdr-val';
      return '<td><div style="display:flex;flex-direction:column;line-height:1.3">'
           + '<span class="' + lfcCls + '">' + lfc + '</span>'
           + '<span class="' + fdrCls + '">FDR ' + fdrStr + '</span>'
           + '</div></td>';
    }}).join('');
  }}

  function scChips(sc) {{
    if (!sc.length) return '<span class="na-val">—</span>';
    return '<div class="sc-chips">' + sc.map(h => {{
      const dir = h.lfc >= 0 ? 'sc-up' : 'sc-dn';
      const lfc = (h.lfc >= 0 ? '+' : '') + h.lfc;
      return '<span class="sc-chip">' + h.ct + ' <span class="' + dir + '">' + lfc + '</span></span>';
    }}).join('') + '</div>';
  }}

  function renderRow(r) {{
    const srcBadge  = '<span class="src-badge ' + SRC_CLS[r.source] + '">' + r.source + '</span>';
    const concBadge = '<span class="conc-badge ' + CONC_CLS[r.concordance] + '">' + r.concordance + '</span>';
    const rowCls    = r.concordance === 'Discordant' ? 'row-disc' : '';
    return '<tr class="' + rowCls + '">'
      + '<td><span class="gene-name">' + r.gene + '</span></td>'
      + '<td>' + srcBadge  + '</td>'
      + '<td>' + concBadge + '</td>'
      + bulkCols(r.bulk)
      + '<td>' + scChips(r.sc) + '</td>'
      + '</tr>';
  }}

  function sortVal(r, col) {{
    if (col === 0) return r.gene;
    if (col === 1) return SOURCE_ORDER.indexOf(r.source);
    if (col === 2) return CONC_ORDER.indexOf(r.concordance);
    for (let i = 0; i < N_STUDIES; i++) {{
      if (col === 3 + i) {{
        const b = r.bulk[i];
        return b ? b.lfc : -Infinity;
      }}
    }}
    if (col === BASE) return r.sc.length;
    return 0;
  }}

  function renderTable() {{
    try {{
      const q    = (document.getElementById('phSearch_{_uid}') || {{}}).value || '';
      const qLow = q.toLowerCase().trim();
      let rows = filterVal === 'all' ? ROWS : ROWS.filter(r => r[filterKey] === filterVal);
      if (qLow) rows = rows.filter(r => r.gene.toLowerCase().includes(qLow));
      rows = rows.slice().sort((a, b) => {{
        const va = sortVal(a, sortCol), vb = sortVal(b, sortCol);
        return sortAsc ? (va < vb ? -1 : va > vb ? 1 : 0)
                       : (va < vb ?  1 : va > vb ? -1 : 0);
      }});
      const tbody = document.getElementById(TBODY_ID);
      if (tbody) tbody.innerHTML = rows.map(renderRow).join('');
    }} catch(e) {{ console.error('panel renderTable:', e); }}
  }}
  window['renderTable_{_uid}'] = renderTable;

  window['setFilter_{_uid}'] = function(key, val, btn) {{
    filterKey = key; filterVal = val;
    document.querySelectorAll('.ph-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    renderTable();
  }};

  window['sortBy_{_uid}'] = function(col) {{
    if (sortCol === col) sortAsc = !sortAsc; else {{ sortCol = col; sortAsc = true; }}
    renderTable();
  }};

  renderTable();
}})();
</script>
"""

    display(HTML(f"""
<div style="max-height:700px; overflow-y:auto; overflow-x:auto; border:1px solid {GS_LINE}; border-radius:8px;">
{html}
</div>
"""))

