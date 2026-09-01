"""Correlation, GSEA, and related analysis helpers."""
from typing import Literal
import textwrap
import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba
from matplotlib.lines import Line2D
import plotly.express as px
from plotly.graph_objects import Figure
from scipy.cluster.hierarchy import leaves_list, linkage
from scipy.spatial.distance import pdist
from scipy.stats import pearsonr, spearmanr
import gseapy as gp

from demo_utils._util import _ordered_categories
from demo_utils.theme import (
    GS_BLUE,
    GS_CLOUD,
    GS_INK,
    GS_LINE,
    GS_MIST,
    GS_TEXT,
)


def plot_correlation_scatter(
    df: pd.DataFrame,
    x: str,
    y: str,
    method: Literal['pearson', 'spearman'] = 'pearson',
    color_by: str | None = None,
    shape_by: str | None = None,
    fill_na_color: str = 'Not applicable',
    title: str | None = None,
    figsize: tuple[float, float] = (8, 6),
    ax=None,
) -> None:
    """
    Scatter of two numeric columns with an OLS line and correlation stats.

    Optional ``color_by`` colours points as numeric (colour bar) or
    categorical (legend); ``shape_by`` varies the marker per category and
    gets its own legend. Missing annotation values are drawn in grey (or
    with the last marker) and listed last under ``fill_na_color``. The
    fitted line is ordinary least squares even when ``method='spearman'``.

    Parameters:
    - df: Table containing x, y, and optionally color_by / shape_by.
    - x / y: Numeric column names to plot.
    - method: 'pearson' or 'spearman' for the reported r and p-value.
    - color_by: Optional column used to colour points.
    - shape_by: Optional categorical column used to vary marker shape.
    - fill_na_color: Legend label for missing color_by / shape_by values.
    - title: Optional figure title.
    - figsize: Figure size when ax is not provided.
    - ax: Optional existing axes.

    Returns:
    - Displays (or draws onto ax) a matplotlib scatter plot.
    """
    for col in (x, y):
        if col not in df.columns:
            raise ValueError(f"Column {col!r} not found in dataframe.")
    for col in (color_by, shape_by):
        if col is not None and col not in df.columns:
            raise ValueError(f"Column {col!r} not found in dataframe.")

    method = method.lower()
    if method == 'pearson':
        corr_fn, method_label = pearsonr, 'Pearson'
    elif method == 'spearman':
        corr_fn, method_label = spearmanr, 'Spearman'
    else:
        raise ValueError("method must be either 'pearson' or 'spearman'.")

    title = title or f'{x} vs {y}'

    NA_COLOR = '#bdbdbd'
    MARKERS = ('o', 's', '^', 'D', 'v', 'P', 'X', '<', '>', '*')

    cols = [x, y] + [c for c in (color_by, shape_by) if c is not None]
    clean = df[cols].copy()
    clean[x] = pd.to_numeric(clean[x], errors='coerce')
    clean[y] = pd.to_numeric(clean[y], errors='coerce')
    clean = clean.dropna(subset=[x, y])  # keep rows with missing annotations
    if len(clean) < 3:
        raise ValueError('Need at least 3 valid points for correlation.')

    x_vals = clean[x].to_numpy()
    y_vals = clean[y].to_numpy()
    corr_coef, p_value = corr_fn(x_vals, y_vals)

    standalone = ax is None
    if standalone:
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig = ax.figure
    fig.patch.set_facecolor(GS_CLOUD)
    ax.set_facecolor(GS_CLOUD)

    # colour per point: single colour, categorical palette, or numeric colour map
    color_numeric = color_by is not None and pd.api.types.is_numeric_dtype(clean[color_by])
    color_na = (
        clean[color_by].isna().to_numpy() if color_by is not None
        else np.zeros(len(clean), dtype=bool)
    )
    color_handles: list[Line2D] = []
    norm = None
    if color_by is None:
        point_colors = np.tile(to_rgba(GS_BLUE), (len(clean), 1))
    elif color_numeric:
        point_colors = None  # values are mapped through cmap/norm at draw time
        color_values = clean[color_by].to_numpy(dtype=float)
        if (~color_na).any():
            finite = color_values[~color_na]
            norm = plt.Normalize(vmin=finite.min(), vmax=finite.max())
    else:
        categories = _ordered_categories(clean[color_by], fill_na_color)
        cmap = plt.get_cmap('tab10' if len(categories) <= 10 else 'tab20')
        color_map = {
            cat: (NA_COLOR if cat == fill_na_color else cmap(i % cmap.N))
            for i, cat in enumerate(categories)
        }
        filled = clean[color_by].where(~color_na, fill_na_color)
        point_colors = np.array([to_rgba(color_map[v]) for v in filled])
        color_handles = [
            Line2D(
                [0], [0], marker='o', color='w', markerfacecolor=color_map[cat],
                markersize=8, label=str(cat),
            )
            for cat in categories
        ]

    # marker per shape_by category
    shape_handles: list[Line2D] = []
    if shape_by is None:
        shape_groups = [(np.ones(len(clean), dtype=bool), 'o')]
    else:
        shape_cats = _ordered_categories(clean[shape_by], fill_na_color)
        filled_shapes = clean[shape_by].where(~clean[shape_by].isna(), fill_na_color)
        shape_groups = []
        for i, cat in enumerate(shape_cats):
            marker = MARKERS[i % len(MARKERS)]
            shape_groups.append(((filled_shapes == cat).to_numpy(), marker))
            shape_handles.append(
                Line2D(
                    [0], [0], marker=marker, color='w', markerfacecolor=GS_TEXT,
                    markeredgecolor='white', markersize=8, label=str(cat),
                )
            )

    scatter_kwargs = dict(alpha=0.7, s=50, zorder=2, edgecolors='white', linewidths=0.4)
    na_kwargs = {**scatter_kwargs, 'zorder': 1}
    scatter = None
    for mask, marker in shape_groups:
        if not mask.any():
            continue
        if not color_numeric:
            ax.scatter(
                x_vals[mask], y_vals[mask],
                c=point_colors[mask], marker=marker, **scatter_kwargs,
            )
            continue
        na_points = mask & color_na
        if na_points.any():
            ax.scatter(
                x_vals[na_points], y_vals[na_points],
                c=NA_COLOR, marker=marker, **na_kwargs,
            )
        valued = mask & ~color_na
        if valued.any():
            scatter = ax.scatter(
                x_vals[valued], y_vals[valued], c=color_values[valued],
                cmap='viridis', norm=norm, marker=marker, **scatter_kwargs,
            )

    has_colorbar = False
    if color_numeric and scatter is not None:
        cbar = fig.colorbar(scatter, ax=ax, fraction=0.05, pad=0.04)
        cbar.set_label(color_by, fontsize=10, color='black')
        cbar.ax.tick_params(colors='black', labelsize=8)
        has_colorbar = True
    if color_numeric and color_na.any():
        color_handles = [
            Line2D(
                [0], [0], marker='o', color='w', markerfacecolor=NA_COLOR,
                markersize=8, label=fill_na_color,
            )
        ]

    coef = np.polyfit(x_vals, y_vals, 1)
    x_line = np.linspace(x_vals.min(), x_vals.max(), 100)
    ax.plot(
        x_line, np.poly1d(coef)(x_line),
        color=GS_INK, linestyle='--', alpha=0.85, linewidth=1.6, zorder=3,
    )

    ax.text(
        0.05, 0.95,
        f'{method_label}:\nr = {corr_coef:.3f}\np = {p_value:.2e}',
        transform=ax.transAxes, fontsize=11, va='top', color='black',
        bbox=dict(boxstyle='round', facecolor=GS_MIST, edgecolor=GS_LINE, alpha=0.9),
    )

    ax.set_xlabel(x, fontsize=12, color='black')
    ax.set_ylabel(y, fontsize=12, color='black')
    ax.set_title(title, fontsize=14, fontweight='bold', color='black', pad=10)
    ax.tick_params(colors='black', labelcolor='black')
    ax.grid(True, alpha=0.3)

    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_color('black')

    # legends stack outside on the right; shift further out past a colour bar
    legend_specs = [
        (handles, legend_title)
        for handles, legend_title in ((color_handles, color_by), (shape_handles, shape_by))
        if handles
    ]
    legend_x = 1.24 if has_colorbar else 1.02
    legend_kwargs = dict(
        borderaxespad=0.0, fontsize=8, title_fontsize=9, frameon=False,
    )
    if len(legend_specs) == 1:
        handles, legend_title = legend_specs[0]
        ax.legend(
            handles=handles, title=legend_title, loc='center left',
            bbox_to_anchor=(legend_x, 0.5), **legend_kwargs,
        )
    elif len(legend_specs) == 2:
        # anchor both to mid-height so they read as one block, colours above shapes
        gap = 0.02
        upper = ax.legend(
            handles=legend_specs[0][0], title=legend_specs[0][1], loc='lower left',
            bbox_to_anchor=(legend_x, 0.5 + gap), **legend_kwargs,
        )
        ax.add_artist(upper)
        ax.legend(
            handles=legend_specs[1][0], title=legend_specs[1][1], loc='upper left',
            bbox_to_anchor=(legend_x, 0.5 - gap), **legend_kwargs,
        )

    if standalone:
        if legend_specs:
            fig.subplots_adjust(right=0.68 if has_colorbar else 0.78)
        else:
            fig.tight_layout()
        plt.show()


def run_gsea_per_cell_type(
    input_dict: dict,
    rank_by: str = 'log2_fc',
    gene_sets: str = 'MSigDB_Hallmark_2020',
    min_size: int = 5,
    max_size: int = 500,
    permutation_num: int = 1000,
    fdr_thresh: float = 0.25,
) -> pd.DataFrame:
    """
    Run preranked GSEA independently for each cell type.
    
    Parameters:
    - input_dict: Dictionary with DataFrames (e.g. DE results with gene_id, log2_fc) as values and cell types as keys.
    - rank_by: Column to be used for ranking (must be numeric).
    - gene_sets: gseapy gene-set library name (e.g. MSigDB_Hallmark_2020).
    - min_size: Minimum gene-set size.
    - max_size: Maximum gene-set size.
    - permutation_num: Number of permutations.
    - fdr_thresh: Keep pathways with FDR below this value.
    
    Returns:
    - Combined GSEA table (pathway, nes, fdr, cell_type, …);
      empty if nothing passed filters.
    """
    results = []

    for ct, df in input_dict.items():
        keep_cols = ['gene_id'] + [rank_by]
        rnk = (
            df[keep_cols]
            .dropna()
            .drop_duplicates('gene_id')
            .set_index('gene_id')[rank_by]
            .sort_values(ascending=False)
        )

        if len(rnk) < min_size * 2:
            print(f"  Skipping {ct}: only {len(rnk)} genes")
            continue

        try:
            with warnings.catch_warnings():
                warnings.simplefilter('ignore')
                pre = gp.prerank(
                    rnk=rnk,
                    gene_sets=gene_sets,
                    outdir=None,
                    min_size=min_size,
                    max_size=max_size,
                    permutation_num=permutation_num,
                    seed=42,
                    verbose=False,
                    threads=1,
                )

            res = (pre.res2d if hasattr(pre, 'res2d') else pre.results).copy()
            res['cell_type'] = ct

            col_map = {
                'Term': 'pathway', 'ES': 'es', 'NES': 'nes',
                'NOM p-val': 'pval', 'FDR q-val': 'fdr',
                'Tag %': 'tag_pct', 'Lead_genes': 'leading_genes',
            }
            res = res.rename(columns={k: v for k, v in col_map.items() if k in res.columns})

            res['n_leading'] = res['leading_genes'].apply(
                lambda x: len(str(x).split(';')) if pd.notna(x) and str(x) != '' else 0
            )
            res['significant'] = res['fdr'] < fdr_thresh

            keep = ['pathway', 'cell_type', 'es', 'nes', 'pval', 'fdr',
                    'tag_pct', 'leading_genes', 'n_leading', 'significant']
            results.append(res[[c for c in keep if c in res.columns]])

            n_sig = int(res['significant'].sum())
            print(f"  {ct}: {n_sig} significant pathways (FDR < {fdr_thresh})")

        except Exception as e:
            print(f"  WARNING {ct}: {e}")

    if not results:
        print("No results — check that input_dict has enough genes per cell type.")
        return pd.DataFrame()

    return (pd.concat(results, ignore_index=True)
              .sort_values(['cell_type', 'nes'], ascending=[True, False])
              .reset_index(drop=True))


def plot_gsea_dotplot(
    gsea_results: pd.DataFrame,
    top_n: int = 20,
    title: str = 'GSEA · size = −log10(FDR) · colour = NES (Case vs Control)',
    cluster_pathways: bool = True,
    cluster_cell_types: bool = True,
) -> None:
    """
    Dot plot of GSEA results: pathways × cell types.
    
    Dot colour = NES; dot size = −log10(FDR). Shows the top_n pathways by
    aggregate signal across cell types.
    
    Parameters:
    - gsea_results: Columns pathway, cell_type, nes, fdr.
    - top_n: Number of pathways to keep.
    - title: Plot title.
    - cluster_pathways: Cluster pathway rows.
    - cluster_cell_types: Cluster cell-type columns.
    
    Returns:
    - Displays a matplotlib dot plot.
    """
    df_sig = gsea_results[gsea_results['significant']].copy()
    if df_sig.empty:
        df_sig = gsea_results.copy()
        print("No significant pathways — showing all")

    top_pws = (df_sig.groupby('pathway')['nes'].apply(lambda x: x.abs().max())
                     .nlargest(top_n).index.tolist())

    df_top = gsea_results[gsea_results['pathway'].isin(top_pws)].copy()
    df_top['neg_log_fdr'] = -np.log10(df_top['fdr'].clip(lower=1e-4))

    size_df  = df_top.pivot_table(index='pathway', columns='cell_type',
                                   values='neg_log_fdr', aggfunc='first').fillna(0)
    color_df = df_top.pivot_table(index='pathway', columns='cell_type',
                                   values='nes', aggfunc='first').fillna(0)
    size_df, color_df = size_df.align(color_df, join='left', fill_value=0)

    # clustering matrix: significant NES only, zero-filled elsewhere
    cluster_matrix = (
        df_sig[df_sig['pathway'].isin(top_pws)]
        .pivot_table(index='pathway', columns='cell_type', values='nes', aggfunc='first')
        .reindex(index=color_df.index, columns=color_df.columns)
        .fillna(0)
    )

    if cluster_cell_types and len(cluster_matrix.columns) > 1:
        col_ord  = leaves_list(linkage(pdist(cluster_matrix.values.T, metric='euclidean'), method='ward'))
        color_df = color_df.iloc[:, col_ord]
        size_df  = size_df.iloc[:, col_ord]

    if cluster_pathways and len(cluster_matrix) > 1:
        row_ord  = leaves_list(linkage(pdist(cluster_matrix.values, metric='euclidean'), method='ward'))
        color_df = color_df.iloc[row_ord]
        size_df  = size_df.iloc[row_ord]
    else:
        pw_order = (df_sig.groupby('pathway')['nes'].apply(lambda x: x.abs().max())
                          .reindex(top_pws).sort_values(ascending=True).index.tolist())
        size_df  = size_df.reindex([p for p in pw_order if p in size_df.index])
        color_df = color_df.reindex(size_df.index)

    n_pw, n_ct = len(size_df), len(size_df.columns)
    fig, ax = plt.subplots(figsize=(max(10, n_ct * 0.95), max(2.4, 1.6 + n_pw * 0.55)))

    vmax  = max(abs(color_df.values.max()), abs(color_df.values.min())) or 1
    s_max = size_df.values.max() or 1
    max_dot = 350

    for i, pw in enumerate(size_df.index):
        for j, ct in enumerate(size_df.columns):
            s   = size_df.loc[pw, ct]
            nes = color_df.loc[pw, ct]
            norm_c = (nes + vmax) / (2 * vmax + 1e-9)
            ax.scatter(j, i, s=s / s_max * max_dot,
                       c=[[plt.cm.RdBu_r(np.clip(norm_c, 0, 1))]],
                       edgecolors='#aaa', linewidths=0.3, zorder=2)

    ax.set_xticks(range(n_ct))
    ax.set_xticklabels(size_df.columns, rotation=45, ha='right', fontsize=13)
    ax.set_yticks(range(n_pw))
    ax.set_yticklabels(size_df.index, fontsize=13)
    ax.invert_yaxis()
    ax.set_title(title, fontsize=19)
    ax.grid(True, color='#f0f0f0', linewidth=0.5, zorder=0)
    ax.set_facecolor('white')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    for fdr_val in [0.25, 0.1, 0.05]:
        dot_s = -np.log10(fdr_val) / s_max * max_dot
        ax.scatter([], [], s=dot_s, c='#bbb',
                   label=f'FDR={fdr_val}', edgecolors='#aaa', linewidths=0.3)
    ax.legend(title='FDR', bbox_to_anchor=(1.02, 1), loc='upper left',
              fontsize=14, title_fontsize=15)

    sm = plt.cm.ScalarMappable(cmap='RdBu_r', norm=plt.Normalize(vmin=-vmax, vmax=vmax))
    sm.set_array([])

    # vertical NES colorbar directly below the FDR legend — axes-fraction coords
    cax = ax.inset_axes([1.02, 0.1, 0.02, 0.3])
    cbar = fig.colorbar(sm, cax=cax, orientation='vertical')
    cbar.set_label('NES', fontsize=15)
    cbar.ax.tick_params(labelsize=13)

    fig.subplots_adjust(right=0.78)
    plt.show()


def plot_gsea_heatmap(
    gsea_results: pd.DataFrame,
    top_n: int = 20,
    title: str = 'GSEA NES · pathway × cell type (Case vs Control) · * FDR < 0.25',
    cluster_pathways: bool = True,
    cluster_cell_types: bool = True,
) -> None:
    """
    Heatmap of GSEA NES values: pathways × cell types.
    
    Same pathway selection as the GSEA dot plot, coloured by normalised
    enrichment score.
    
    Parameters:
    - gsea_results: Columns pathway, cell_type, nes, fdr.
    - top_n: Number of pathways to keep.
    - title: Plot title.
    - cluster_pathways: Cluster pathway rows.
    - cluster_cell_types: Cluster cell-type columns.
    
    Returns:
    - Displays a matplotlib heatmap.
    """
    df_sig = gsea_results[gsea_results['significant']].copy()
    if df_sig.empty:
        df_sig = gsea_results.copy()

    top_pws = (df_sig.groupby('pathway')['nes'].apply(lambda x: x.abs().max())
                     .nlargest(top_n).index.tolist())

    df_top    = gsea_results[gsea_results['pathway'].isin(top_pws)]
    pivot     = df_top.pivot_table(index='pathway', columns='cell_type',
                                   values='nes', aggfunc='first').fillna(0)
    sig_pivot = df_top.pivot_table(index='pathway', columns='cell_type',
                                   values='significant', aggfunc='first').fillna(False)

    # clustering matrix: significant NES only, zero-filled elsewhere
    cluster_matrix = (
        df_sig[df_sig['pathway'].isin(top_pws)]
        .pivot_table(index='pathway', columns='cell_type', values='nes', aggfunc='first')
        .reindex(index=pivot.index, columns=pivot.columns)
        .fillna(0)
    )

    if cluster_cell_types and len(cluster_matrix.columns) > 1:
        col_ord   = leaves_list(linkage(pdist(cluster_matrix.values.T, metric='euclidean'), method='ward'))
        pivot     = pivot.iloc[:, col_ord]
        sig_pivot = sig_pivot.iloc[:, col_ord]

    if cluster_pathways and len(cluster_matrix) > 1:
        row_ord   = leaves_list(linkage(pdist(cluster_matrix.values, metric='euclidean'), method='ward'))
        pivot     = pivot.iloc[row_ord]
        sig_pivot = sig_pivot.iloc[row_ord]
    else:
        pw_order  = pivot.abs().max(axis=1).sort_values(ascending=True).index.tolist()
        pivot     = pivot.reindex(pw_order)
        sig_pivot = sig_pivot.reindex(index=pw_order, columns=pivot.columns).fillna(False)

    n_pw, n_ct = len(pivot), len(pivot.columns)
    fig, ax = plt.subplots(figsize=(max(10, n_ct * 0.95), max(2.4, 1.6 + n_pw * 0.55)))

    vmax = max(abs(pivot.values.max()), abs(pivot.values.min())) or 1
    im   = ax.imshow(pivot.values, cmap='RdBu_r', vmin=-vmax, vmax=vmax, aspect='auto')

    for i in range(n_pw):
        for j in range(n_ct):
            if sig_pivot.values[i, j]:
                ax.text(j, i, '*', ha='center', va='center',
                        fontsize=15, color='white', fontweight='bold')

    ax.set_xticks(range(n_ct))
    ax.set_xticklabels(pivot.columns, rotation=45, ha='right', fontsize=13)
    ax.set_yticks(range(n_pw))
    ax.set_yticklabels(pivot.index, fontsize=13)
    ax.set_title(title, fontsize=19)
    cbar = fig.colorbar(im, ax=ax, shrink=0.4)
    cbar.set_label('NES (Normalised Enrichment Score)', fontsize=15)
    cbar.ax.tick_params(labelsize=13)
    plt.tight_layout()
    plt.show()


def plot_gsea_bubble(
    gsea_results: pd.DataFrame,
    cell_type: str | None = None,
    top_n: int | None = None,
    title: str | None = None,
) -> None:
    """
    Interactive Plotly bubble plot of significant GSEA results.

    y = pathway, x = −log10(FDR), colour = NES, size = n_leading.
    Leading-edge genes appear in the hover tooltip.

    Parameters:
    - gsea_results: Output of run_gsea_per_cell_type (needs pathway, fdr, nes,
      n_leading, leading_genes, significant; cell_type optional).
    - cell_type: If set, restrict to this cell type. When several cell types
      remain, pathway labels include the cell type to stay unique.
    - top_n: Keep at most this many pathways (highest −log10(FDR)).
    - title: Plot title; default mentions cell type when filtered.

    Returns:
    - Displays a Plotly Figure.
    """
    required = {'pathway', 'fdr', 'nes', 'n_leading', 'leading_genes', 'significant'}
    missing = required - set(gsea_results.columns)
    if missing:
        raise ValueError(f"gsea_results missing columns: {sorted(missing)}")

    df = gsea_results.loc[gsea_results['significant']].copy()
    if df.empty:
        print("No significant pathways — nothing to plot")
        return

    if cell_type is not None:
        if 'cell_type' not in df.columns:
            raise ValueError("cell_type filter requested but column is missing")
        df = df.loc[df['cell_type'] == cell_type].copy()
        if df.empty:
            print(f"No significant pathways for cell_type={cell_type!r}")
            return

    df['fdr'] = pd.to_numeric(df['fdr'], errors='coerce')
    df['nes'] = pd.to_numeric(df['nes'], errors='coerce')
    df['n_leading'] = pd.to_numeric(df['n_leading'], errors='coerce').fillna(0)
    df['leading_genes'] = df['leading_genes'].apply(
        lambda genes: '<br>'.join(
            textwrap.wrap(
                str(genes).replace(';', ', '),
                width=60,
                break_long_words=False,
                break_on_hyphens=False,
            )
        )
        if pd.notna(genes)
        else ''
    )
    df = df.dropna(subset=['fdr', 'nes', 'pathway'])
    if df.empty:
        print("No significant pathways with valid fdr/nes — nothing to plot")
        return

    df['neg_log_fdr'] = -np.log10(df['fdr'].clip(lower=1e-300))

    if top_n is not None and top_n > 0 and len(df) > top_n:
        df = df.nlargest(top_n, 'neg_log_fdr')

    multi_ct = 'cell_type' in df.columns and df['cell_type'].nunique() > 1
    if multi_ct:
        df['pathway_label'] = df['pathway'].astype(str) + ' · ' + df['cell_type'].astype(str)
    else:
        df['pathway_label'] = df['pathway'].astype(str)

    df = df.sort_values('neg_log_fdr', ascending=True)

    if title is None:
        if cell_type is not None:
            title = f'GSEA bubble · {cell_type} · colour = NES · size = n_leading'
        else:
            title = 'GSEA bubble · colour = NES · size = n_leading'

    hover = {
        'pathway': True,
        'leading_genes': True,
        'nes': ':.3f',
        'fdr': ':.3f',
        'pathway_label': False,
    }
    for column, format_spec in (('pval', ':.2e'), ('tag_pct', True)):
        if column in df.columns:
            hover[column] = format_spec
    if 'cell_type' in df.columns:
        hover['cell_type'] = True

    fig = px.scatter(
        df,
        x='neg_log_fdr',
        y='pathway_label',
        color='nes',
        size='n_leading',
        hover_data=hover,
        color_continuous_scale='RdBu_r',
        color_continuous_midpoint=0,
        size_max=28,
        title=title,
        labels={
            'neg_log_fdr': '−log₁₀(FDR)',
            'pathway_label': 'Pathway',
            'nes': 'NES',
            'n_leading': 'Leading-edge genes',
        },
    )

    n_pw = len(df)
    fig.update_layout(
        height=max(360, 80 + n_pw * 28),
        yaxis=dict(categoryorder='array', categoryarray=df['pathway_label'].tolist()),
        template='plotly_white',
        margin=dict(l=20, r=20, t=60, b=40),
        coloraxis_colorbar=dict(
            title="NES",
            len=0.6,
            thickness=20,
        )
    )
    fig.update_layout(yaxis_title=None)
    fig.update_traces(marker=dict(line=dict(width=0.5, color='#888')))
    fig.show()
