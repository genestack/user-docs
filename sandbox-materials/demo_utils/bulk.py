"""Bulk expression analysis and visualisation helpers."""

import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from IPython.display import HTML, display
from pydeseq2.dds import DeseqDataSet
from pydeseq2.ds import DeseqStats
from scipy.cluster.hierarchy import leaves_list, linkage
from scipy.spatial.distance import pdist
from scipy.stats import false_discovery_control, mannwhitneyu

from demo_utils._util import _rename_duplicates, _short_label
from demo_utils.theme import GS_BLUE, GS_CLOUD, GS_INK, GS_LINE, GS_MIST, GS_STEEL, GS_TEXT


def run_bulk_de(
    case_df: pd.DataFrame,
    ctrl_df: pd.DataFrame,
    is_log_scale: bool = False,
) -> pd.DataFrame:
    """
    Wilcoxon rank-sum DE between case and control expression matrices.
    
    Parameters:
    - case_df: genes × samples for the case group.
    - ctrl_df: genes × samples for the control group.
    - is_log_scale: If True (log2 / RMA), log2FC = mean_case − mean_ctrl;
      if False (CPM/TMM/TPM), log2FC = log2((mean_case+1)/(mean_ctrl+1)).
    
    Returns:
    - Sorted by FDR with columns
      gene_id, n_case, n_ctrl, mean_case, mean_ctrl, log2_fc, p_value, fdr.
    """
    case_df = _rename_duplicates(case_df)
    ctrl_df = _rename_duplicates(ctrl_df)

    genes = case_df.index.intersection(ctrl_df.index)
    rows = []
    for gene in genes:
        case_vals = pd.to_numeric(case_df.loc[gene], errors='coerce').dropna().values
        ctrl_vals = pd.to_numeric(ctrl_df.loc[gene], errors='coerce').dropna().values
        if len(case_vals) < 2 or len(ctrl_vals) < 2:
            continue
        _, pval = mannwhitneyu(case_vals, ctrl_vals, alternative='two-sided')
        mean_case = float(np.mean(case_vals))
        mean_ctrl = float(np.mean(ctrl_vals))
        if is_log_scale:
            log2fc = mean_case - mean_ctrl
        else:
            log2fc = float(np.log2((mean_case + 1) / (mean_ctrl + 1)))
        rows.append({
            'gene_id': gene,
            'n_case': len(case_vals),
            'n_ctrl': len(ctrl_vals),
            'mean_case': mean_case,
            'mean_ctrl': mean_ctrl,
            'log2_fc': log2fc,
            'p_value': pval,
        })
    de_df = pd.DataFrame(rows)
    if len(de_df) == 0:
        return de_df
    de_df['p_value'] = de_df['p_value'].replace(0, 1e-16).fillna(1.0)
    de_df['fdr'] = false_discovery_control(de_df['p_value'], method='bh')
    return de_df.sort_values('fdr').reset_index(drop=True)


def run_bulk_de_deseq2(
    case_df: pd.DataFrame,
    ctrl_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    DESeq2 differential expression between case and control count matrices.
    
    Parameters:
    - case_df: genes × samples raw/roundable counts for case.
    - ctrl_df: genes × samples raw/roundable counts for control.
    
    Returns:
    - Sorted by FDR with columns
      gene_id, n_case, n_ctrl, mean_case, mean_ctrl, log2_fc, p_value, fdr.
    """
    genes = case_df.index.intersection(ctrl_df.index)
    case_df = case_df.loc[genes]
    ctrl_df = ctrl_df.loc[genes]

    counts = pd.concat([case_df.T, ctrl_df.T]).fillna(0).round().astype(int)
    metadata = pd.DataFrame(
        {'condition': ['case'] * case_df.shape[1] + ['ctrl'] * ctrl_df.shape[1]},
        index=counts.index
    )

    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        dds = DeseqDataSet(
            counts=counts,
            metadata=metadata,
            design_factors='condition',
            refit_cooks=True,
            quiet=True,
            n_cpus=1,
        )
        dds.deseq2()
        stat_res = DeseqStats(dds, contrast=['condition', 'case', 'ctrl'], quiet=True)
        stat_res.summary()

    res = stat_res.results_df.dropna(subset=['pvalue', 'log2FoldChange'])
    mean_case = case_df.mean(axis=1).reindex(res.index)
    mean_ctrl = ctrl_df.mean(axis=1).reindex(res.index)

    return pd.DataFrame({
        'gene_id':   res.index,
        'n_case':    case_df.shape[1],
        'n_ctrl':    ctrl_df.shape[1],
        'mean_case': mean_case.values,
        'mean_ctrl': mean_ctrl.values,
        'log2_fc':   res['log2FoldChange'].values,
        'p_value':   res['pvalue'].values,
        'fdr':       res['padj'].fillna(1.0).values,
    }).sort_values('fdr').reset_index(drop=True)


def display_bulk_de_card(
    label: str,
    row: pd.Series,
    case_ex: pd.DataFrame,
    ctrl_ex: pd.DataFrame,
    de: pd.DataFrame,
    case_label: str = 'Case',
    ctrl_label: str = 'Control',
    case_col: str | None = None,
    ctrl_col: str | None = None,
    fdr_threshold: float = 0.05,
    log2fc_threshold: float = 1,
) -> None:
    """
    Show a per-dataset summary card after bulk DE (sample counts, matrix size, hits).
    
    Used in the demo while bulk DE runs study-by-study so the audience sees
    case vs control sample numbers, gene×sample matrix shape, and how many genes
    pass FDR / |log2FC| thresholds (with top up/down gene names).
    
    Parameters:
    - label: Dataset / study label for the card title.
    - row: Inventory row with case / control sample-count columns.
    - case_ex: Case expression matrix (genes × samples).
    - ctrl_ex: Control expression matrix (genes × samples).
    - de: DE table with gene_id, log2_fc, fdr.
    - case_label: Display label for the case group.
    - ctrl_label: Display label for the control group.
    - case_col: Inventory column for case counts; default ``f'{case_label} samples'``.
    - ctrl_col: Inventory column for control counts; default ``f'{ctrl_label} samples'``.
    - fdr_threshold: FDR cutoff for counting significant genes.
    - log2fc_threshold: |log2FC| cutoff for counting significant genes.
    
    Returns:
    - Displays an HTML summary card in the notebook.
    """
    case_col = case_col or f'{case_label} samples'
    ctrl_col = ctrl_col or f'{ctrl_label} samples'
    sig_mask = (de['fdr'] < fdr_threshold) & (de['log2_fc'].abs() >= log2fc_threshold)
    n_sig  = sig_mask.sum()
    n_up   = (sig_mask & (de['log2_fc'] > 0)).sum()
    n_dn   = (sig_mask & (de['log2_fc'] < 0)).sum()
    top_up = ', '.join(de[sig_mask & (de['log2_fc'] > 0)].head(5)['gene_id'].tolist())
    top_dn = ', '.join(de[sig_mask & (de['log2_fc'] < 0)].head(5)['gene_id'].tolist())

    display(HTML(f"""
    <div style="border-left:4px solid {GS_STEEL};padding:10px 16px;margin:12px 0;
                background:{GS_CLOUD};border-radius:4px">
      <div style="font-size:1.05em;font-weight:bold;color:{GS_INK};margin-bottom:8px">{label}</div>
      <table style="border-collapse:collapse;font-size:0.9em;width:100%">
        <tr>
          <td style="padding:3px 12px 3px 0;color:{GS_TEXT}">Samples</td>
          <td><b>{case_label}</b>: {row[case_col]} &nbsp;|&nbsp; <b>{ctrl_label}</b>: {row[ctrl_col]}</td>
        </tr>
        <tr>
          <td style="padding:3px 12px 3px 0;color:{GS_TEXT}">Matrix</td>
          <td>{case_ex.shape[0]:,} genes × {case_ex.shape[1]} {case_label} &nbsp;|&nbsp; {ctrl_ex.shape[1]} {ctrl_label}</td>
        </tr>
        <tr>
          <td style="padding:3px 12px 3px 0;color:{GS_TEXT}">DE (FDR&lt;{fdr_threshold}, |log2FC|≥{log2fc_threshold})</td>
          <td><b>{n_sig:,}</b> genes &nbsp;—&nbsp;
            <span style="color:#c0392b">▲ {n_up} up</span> &nbsp;
            <span style="color:{GS_BLUE}">▼ {n_dn} down</span>
          </td>
        </tr>
        <tr>
          <td style="padding:3px 12px 3px 0;color:{GS_TEXT};vertical-align:top">Top UP</td>
          <td style="color:#c0392b">{top_up or '—'}</td>
        </tr>
        <tr>
          <td style="padding:3px 12px 3px 0;color:{GS_TEXT};vertical-align:top">Top DOWN</td>
          <td style="color:{GS_BLUE}">{top_dn or '—'}</td>
        </tr>
      </table>
    </div>
    """))


def display_bulk_de_table(
    de_results: dict,
    genes: list[str],
    log2fc_threshold: float,
) -> None:
    """
    Show a gene × study styled table of bulk log2FC (and FDR) for the panel.
    
    Used after bulk DE to compare the candidate gene panel across datasets in
    one compact view; cells exceeding |log2FC| are colour-highlighted.
    
    Parameters:
    - de_results: Mapping study label → DE DataFrame with
      gene_id, log2_fc, fdr.
    - genes: Gene panel order (rows).
    - log2fc_threshold: |log2FC| used for highlight styling.
    
    Returns:
    - Displays a pandas Styler table in the notebook.
    """
    _frames = []
    for lbl, de in de_results.items():
        sl  = _short_label(lbl)
        tmp = de.set_index('gene_id')[['log2_fc', 'fdr']].rename(columns={
            'log2_fc': f'{sl} log2FC',
            'fdr':     f'{sl} FDR',
        })
        _frames.append(tmp)

    agg_df = (
        pd.concat(_frames, axis=1)
        .reindex(genes)
        .round(3)
        .reset_index()
        .rename(columns={'gene_id': 'Gene'})
    )

    bulk_de_table = (agg_df.style
        .format(precision=3, na_rep='—')
        .apply(lambda col: [
            'color:#c0392b;font-weight:bold' if (
                'log2FC' in col.name and isinstance(v, float) and v > log2fc_threshold
            ) else f'color:{GS_BLUE};font-weight:bold' if (
                'log2FC' in col.name and isinstance(v, float) and v < -log2fc_threshold
            ) else ''
            for v in col
        ])
        .set_table_styles([
            {'selector': 'th', 'props': f'background:{GS_STEEL};color:white;padding:6px 10px;font-size:11px'},
            {'selector': 'td', 'props': f'padding:4px 10px;font-size:12px;border-bottom:1px solid {GS_LINE}'},
            {'selector': 'tr:hover td', 'props': f'background:{GS_MIST}'},
        ])
        .set_properties(subset=['Gene'], **{'background-color': GS_MIST, 'color': 'black'})
        .hide(axis='index')
    )

    display(bulk_de_table)


def plot_bulk_de_heatmap(
    de_results: dict,
    panel_genes: list[str],
    fdr_threshold: float = 0.05,
    log2fc_threshold: float = 1,
    cluster_log2fc_threshold: float = 0.5,
    figsize: tuple[float, float] | None = None,
    contrast_label: str = 'Case vs Control',
) -> None:
    """
    Heatmap of bulk log2FC for panel genes across studies (★ = significant).
    
    Rows are panel genes (optionally clustered); columns are datasets. Colour is
    log2FC (case vs control); stars mark cells passing FDR and |log2FC| thresholds.
    
    Parameters:
    - de_results: Mapping study label → DE DataFrame (gene_id, log2_fc, fdr).
    - panel_genes: Genes to show as rows.
    - fdr_threshold: FDR cutoff for ★ markers.
    - log2fc_threshold: |log2FC| cutoff for ★ markers.
    - cluster_log2fc_threshold: |log2FC| used when building the clustering matrix.
    - figsize: Optional (width, height).
    - contrast_label: Wording used in the colour-bar label.
    
    Returns:
    - Displays a matplotlib heatmap.
    """
    # pivot: rows = genes, cols = datasets
    lfc_df = pd.DataFrame({
        _short_label(lbl): de.set_index('gene_id')['log2_fc']
        for lbl, de in de_results.items()
    }).reindex(panel_genes)

    sig_df = pd.DataFrame({
        _short_label(lbl): (
            (de.set_index('gene_id')['fdr'] < fdr_threshold) &
            (de.set_index('gene_id')['log2_fc'].abs() >= log2fc_threshold)
        ).reindex(panel_genes)
        for lbl, de in de_results.items()
    })

    # cluster order — mirrors plot_bulk_sc_de_comparison's bulk clustering exactly,
    # so gene rows line up across both plots
    if len(lfc_df) > 1:
        cluster_sig_df = pd.DataFrame({
            _short_label(lbl): (
                (de.set_index('gene_id')['fdr'] < fdr_threshold) &
                (de.set_index('gene_id')['log2_fc'].abs() >= cluster_log2fc_threshold)
            ).reindex(panel_genes)
            for lbl, de in de_results.items()
        }).fillna(False)
        cluster_mat = lfc_df.fillna(0).where(cluster_sig_df, 0)
        row_ord = leaves_list(linkage(pdist(cluster_mat.values, metric='euclidean'), method='ward'))
        row_order = lfc_df.index[row_ord]
    else:
        row_order = lfc_df.index

    lfc_df = lfc_df.loc[row_order]
    sig_df = sig_df.reindex(row_order)

    n_genes, n_ds = lfc_df.shape
    if figsize is None:
        figsize = (max(4, n_ds * 1.8), max(5, n_genes * 0.42))
    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor(GS_CLOUD)
    ax.set_facecolor(GS_CLOUD)

    vals = lfc_df.values[~np.isnan(lfc_df.values)]
    vmax = max(abs(vals).max(), log2fc_threshold) if len(vals) else log2fc_threshold

    sns.heatmap(
        lfc_df,
        ax=ax,
        cmap='RdBu_r',
        center=0,
        vmin=-vmax, vmax=vmax,
        linewidths=0.5,
        linecolor=GS_LINE,
        cbar_kws={'label': f'log₂FC ({contrast_label})', 'shrink': 0.6},
    )

    # asterisk on significant cells
    for i, gene in enumerate(lfc_df.index):
        for j, col in enumerate(lfc_df.columns):
            if pd.notna(sig_df.loc[gene, col]) and sig_df.loc[gene, col]:
                ax.text(j + 0.5, i + 0.5, '★', ha='center', va='center',
                        fontsize=7, color='black')

    ax.set_title('Bulk DE · log₂FC per panel gene',
                  fontweight='bold', color=GS_INK, fontsize=9.5, pad=18)
    ax.text(0.5, 1.02, f'★ FDR < {fdr_threshold}, |log₂FC| ≥ {log2fc_threshold}',
            transform=ax.transAxes, ha='center', va='bottom',
            fontsize=8, color=GS_TEXT)
    ax.set_xlabel('', fontsize=0)
    ax.set_ylabel('', fontsize=0)
    ax.tick_params(axis='x', rotation=30, colors=GS_TEXT, labelsize=9)
    ax.tick_params(axis='y', rotation=0,  colors=GS_TEXT, labelsize=8)
    sns.despine(ax=ax, left=True, bottom=True)
    plt.tight_layout()
    plt.show()


def plot_volcano(
    de_df: pd.DataFrame,
    label_genes: list[str] | None = None,
    fdr_threshold: float = 0.05,
    log2fc_threshold: float = 0.5,
    title: str = 'Volcano plot',
    figsize: tuple[float, float] = (9, 6),
    ax=None,
) -> None:
    """
    Volcano plot of bulk DE (−log10 FDR vs log2FC) with optional gene labels.
    
    Points are coloured by up / down / not significant relative to the FDR and
    |log2FC| thresholds.
    
    Parameters:
    - de_df: DE table with gene_id, log2_fc, fdr.
    - label_genes: Gene symbols to annotate; default labels extremes.
    - fdr_threshold: Horizontal significance line.
    - log2fc_threshold: Vertical effect-size lines.
    - title: Plot title.
    - figsize: Figure size when ax is not provided.
    - ax: Optional existing axes.
    
    Returns:
    - Displays (or draws onto ax) a matplotlib volcano plot.
    """
    df = de_df.copy()
    df['fdr'] = df['fdr'].replace(0, np.nextafter(0, 1)).fillna(1.0)
    df['neg_log10_fdr'] = -np.log10(df['fdr'])
    sig = (df['fdr'] < fdr_threshold) & (df['log2_fc'].abs() >= log2fc_threshold)
    df['regulation'] = 'Not significant'
    df.loc[sig & (df['log2_fc'] >= log2fc_threshold), 'regulation'] = 'Up'
    df.loc[sig & (df['log2_fc'] <= -log2fc_threshold), 'regulation'] = 'Down'

    color_map = {'Up': '#d62728', 'Down': '#1f77b4', 'Not significant': '#bdbdbd'}
    size_map  = {'Up': 20, 'Down': 20, 'Not significant': 8}

    standalone = ax is None
    if standalone:
        fig, ax = plt.subplots(figsize=figsize)

    for reg in ['Not significant', 'Down', 'Up']:
        sub = df[df['regulation'] == reg]
        ax.scatter(sub['log2_fc'], sub['neg_log10_fdr'],
                   c=color_map[reg], s=size_map[reg], alpha=0.7,
                   linewidths=0.3 if reg != 'Not significant' else 0,
                   edgecolors='#555', label=reg,
                   zorder=2 if reg != 'Not significant' else 1)

    ax.axvline(-log2fc_threshold, color='#aaa', linewidth=1, linestyle='--', zorder=0)
    ax.axvline( log2fc_threshold, color='#aaa', linewidth=1, linestyle='--', zorder=0)
    ax.axhline(-np.log10(fdr_threshold), color='#aaa', linewidth=1, linestyle='--', zorder=0)

    if label_genes is None:
        sig_df = df[df['regulation'] != 'Not significant']
        label_df = pd.concat([
            sig_df.nlargest(5, 'log2_fc'),
            sig_df.nsmallest(5, 'log2_fc'),
        ]).drop_duplicates(subset='gene_id') if len(sig_df) else df.iloc[0:0]
    else:
        label_df = df[df['gene_id'].isin(set(label_genes))].copy()

    y_max   = df['neg_log10_fdr'].max()
    y_min   = max(-np.log10(fdr_threshold) - 0.3, df['neg_log10_fdr'].min())
    x_max   = df['log2_fc'].max()
    x_min   = df['log2_fc'].min()
    x_range = x_max - x_min

    up_df = label_df[label_df['log2_fc'] >= 0].sort_values('neg_log10_fdr', ascending=False)
    dn_df = label_df[label_df['log2_fc'] <  0].sort_values('neg_log10_fdr', ascending=False)

    def annotate_column(group_df, is_up):
        if len(group_df) == 0:
            return
        min_gap  = (y_max - y_min) * 0.08
        x_anchor = x_max + x_range * 0.05 if is_up else x_min - x_range * 0.05
        ha       = 'left' if is_up else 'right'
        prev_y   = None
        for row in group_df.itertuples(index=False):
            y_label = row.neg_log10_fdr
            if prev_y is not None:
                y_label = min(y_label, prev_y - min_gap)
            ax.annotate(row.gene_id,
                        xy=(row.log2_fc, row.neg_log10_fdr),
                        xytext=(x_anchor, y_label),
                        fontsize=8, ha=ha, va='center',
                        fontweight='bold', color='#333',
                        arrowprops=dict(arrowstyle='-', color='#ccc', lw=0.6))
            prev_y = y_label

    annotate_column(up_df, True)
    annotate_column(dn_df, False)

    if len(label_df):
        ax.set_xlim(x_min - x_range * 0.35, x_max + x_range * 0.35)

    ax.set_xlabel('log2 fold change', fontsize=9)
    ax.set_ylabel('-log10 FDR', fontsize=9)
    ax.set_title(title, fontsize=10)
    ax.set_facecolor('white')
    ax.grid(True, color='#eeeeee', linewidth=0.5, zorder=0)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    if standalone:
        ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', framealpha=0.85, edgecolor='#ddd')
        fig.subplots_adjust(right=0.82)
        plt.show()
