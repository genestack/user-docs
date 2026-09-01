"""Demo presentation / HTML helpers."""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import seaborn as sns
from IPython.display import HTML, display

from demo_utils.util import scalar_value
from demo_utils._util import (
    _fmt_cells,
    _fmt_duration,
    _fmt_gene_scale,
    _decimal_places,
    _soft_to_numeric,
)
from demo_utils.theme import (
    GS_BLUE,
    GS_CLOUD,
    GS_INK,
    GS_LINE,
    GS_STEEL,
    GS_STEEL_PALE,
    GS_MIST,
    GS_TEXT,
)


def display_odm_timing(label: str, dt: float) -> None:
    """
    Display a timing banner.

    Parameters:
    - label: Short description shown on the banner (e.g. query purpose).
    - dt: Duration in seconds.

    Returns:
    - Displays an HTML timing banner.
    """
    display(HTML(
        f"<div style='font-family:Helvetica,Arial,sans-serif;padding:6px 13px;"
        f"margin:6px 0;background:{GS_MIST};border-left:3px solid {GS_BLUE};"
        f"font-size:.85em;color:{GS_BLUE};border-radius:4px;'>"
        f"&#9201; <b>{label}</b> &mdash; {dt:.1f}s "
        f"<span style='color:{GS_TEXT};opacity:.8'>"
        f"(queried live from ODM)"
        f"</span></div>"
    ))


def display_collapsible_table(
    summary_html: str,
    table_html: str,
    open_by_default: bool = False,
) -> None:
    """
    Wrap a verbose HTML table in a collapsed <details> summary line.
    
    Keeps the demo uncluttered: audience sees one-line summary; full table
    opens on click (e.g. long inventory or method breakdowns).
    
    Parameters:
    - summary_html: Visible summary line / chips HTML.
    - table_html: Full table HTML placed inside <details>.
    - open_by_default: Start expanded if True.
    
    Returns:
    - Displays the collapsible HTML block.
    """
    openattr = ' open' if open_by_default else ''
    display(HTML(f"""
    <details{openattr} style="font-family:Helvetica,Arial,sans-serif;
             border:1px solid {GS_LINE};border-radius:8px;padding:2px 14px;
             margin:8px 0;background:{GS_CLOUD}">
      <summary style="cursor:pointer;padding:8px 0;font-weight:600;
               color:{GS_BLUE};outline:none">{summary_html}</summary>
      <div style="padding:6px 0 12px 0;overflow-x:auto">{table_html}</div>
    </details>
    """))


def display_data_type_card(
    n_studies: int,
    n_bulk: int,
    n_sc: int,
    total_cells: int = 0,
) -> None:
    """
    Platform overview card: studies, bulk datasets, SC datasets, and cell count.
    
    Used at the start of Step 1 to frame the data landscape in four big numbers.
    
    Parameters:
    - n_studies: Total ODM studies considered.
    - n_bulk: Bulk transcriptomics datasets.
    - n_sc: Single-cell datasets.
    - total_cells: Total cells across SC datasets.
    
    Returns:
    - Displays an HTML KPI card.
    """
    html = f"""
<div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
            max-width:860px;background:{GS_CLOUD};border:1px solid {GS_LINE};
            border-radius:12px;padding:24px 28px;margin:8px 0">

  <div style="font-size:13px;font-weight:700;color:{GS_TEXT};text-transform:uppercase;
              letter-spacing:.08em;margin-bottom:18px">
    Platform data landscape
  </div>

  <div style="display:flex;gap:12px">
    {"".join(f'''
    <div style="flex:1;background:white;border:1px solid {GS_LINE};border-radius:8px;
                padding:14px 16px;text-align:center">
      <div style="font-size:32px;font-weight:800;color:{col};line-height:1">{val:,}</div>
      <div style="font-size:11px;color:{GS_TEXT};margin-top:4px;font-weight:500">{lbl}</div>
    </div>''' for val, lbl, col in [
        (n_studies,   'ODM studies total',         GS_INK),
        (n_bulk,      'bulk transcriptomics datasets',          GS_BLUE),
        (n_sc,        'single-cell datasets',   GS_STEEL),
        (total_cells, 'cells',           GS_STEEL_PALE),
    ])}
  </div>
</div>
"""
    display(HTML(html))


def plot_bulk_sc_groups_summary(
    df: pd.DataFrame,
    n_studies: int,
    n_groups: int,
    group_col: str = 'group',
    group_attribute: str = 'group',
) -> None:
    """
    Twin horizontal bar charts: bulk samples and SC cells per group.

    Step 1 detailed view of data availability across groups in the instance.
    Bars share thickness across panels, are ordered by descending count from
    the top, and pin "Not reported" to the bottom of each panel.

    Parameters:
    - df: Columns group (or group_col), bulk_samples, sc_cells.
    - n_studies: Study count shown in the figure title.
    - n_groups: Group count shown in the figure title.
    - group_col: Column in df with group labels.
    - group_attribute: Metadata field name used in axis / title wording.

    Returns:
    - Displays a two-panel matplotlib figure.
    """
    not_reported = 'Not reported'
    panel_specs = [
        ('bulk_samples', GS_BLUE,  'Samples',
         f'Bulk RNA-seq — samples per {group_attribute.lower()}'),
        ('sc_cells',     GS_STEEL, 'Cells',
         f'Single-cell — cells per {group_attribute.lower()}'),
    ]

    panel_data: dict[str, pd.DataFrame] = {}
    for col, *_ in panel_specs:
        d = df.loc[df[col] > 0, [group_col, col]].copy()
        d[group_col] = d[group_col].astype(str)
        nr = d[d[group_col] == not_reported]
        rest = (
            d[d[group_col] != not_reported]
            .sort_values([col, group_col], ascending=[True, False])
        )
        panel_data[col] = pd.concat([nr, rest], ignore_index=True)

    max_rows = max(len(d) for d in panel_data.values()) or 1
    fig, axes = plt.subplots(
        1, 2,
        figsize=(14, max(4.0, 0.42 * max_rows + 1.4)),
        squeeze=False,
    )
    fig.patch.set_facecolor(GS_CLOUD)
    axes = axes[0]

    plt.suptitle(
        f'Data availability — {n_studies} studies · '
        f'{n_groups} {group_attribute.lower()} values',
        fontsize=13, fontweight='bold', color=GS_INK, y=1.02,
    )

    for ax, (col, color, xlabel, panel_title) in zip(axes, panel_specs):
        d = panel_data[col]
        y_pos = np.arange(len(d)) + (max_rows - len(d))

        bars = ax.barh(
            y_pos, d[col],
            color=color, alpha=0.88, height=0.65,
            edgecolor='white', linewidth=0.8,
        )
        ax.set_yticks(y_pos)
        ax.set_yticklabels(d[group_col])
        ax.set_facecolor(GS_CLOUD)
        ax.set_title(panel_title, fontweight='bold', fontsize=12, pad=10, color=GS_INK)
        ax.set_xlabel(xlabel, fontsize=10, color=GS_TEXT)
        ax.tick_params(colors=GS_TEXT)
        max_v = d[col].max() or 1
        for bar, val in zip(bars, d[col]):
            ax.text(
                bar.get_width() + max_v * 0.01,
                bar.get_y() + bar.get_height() / 2,
                f'{int(val):,}', va='center', fontsize=9, color=GS_TEXT,
            )
        ax.set_xlim(0, max_v * 1.2)
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.set_ylim(-0.75, max_rows - 0.25)
        ax.spines['bottom'].set_color(GS_LINE)
        ax.spines['left'].set_color(GS_LINE)
        sns.despine(ax=ax)

    plt.tight_layout()
    plt.show()


def display_metadata_summary(
    df: pd.DataFrame,
    drop_any_na_col: bool = False,
    open_by_default: bool = False,
) -> pd.DataFrame:
    """
    Compute and display summary statistics for a metadata dataframe.
    
    Cleans missing/sentinel values, then shows collapsible tables for
    continuous and categorical columns.
    
    Parameters:
    - df: Metadata dataframe to summarize.
    - drop_any_na_col: If True, drop columns with any missing values;
      otherwise drop only all-missing columns.
    - open_by_default: If True, open the collapsible tables by default.

    Returns:
    - Displays collapsible tables for continuous and categorical columns.
    """
    # filter and clean metadata
    df = (
        df
        .replace({'Not reported': np.nan, '.': np.nan, None: np.nan})
        .dropna(
            axis=1,
            how='any' if drop_any_na_col else 'all'  # drop columns with any or all missing values
        )
        .map(scalar_value)  # join list values into strings
        .apply(_soft_to_numeric)  # convert to numeric, ignore errors
    )

    # compute summary statistics for most common attribute values
    summary_df = pd.DataFrame({
        'not_na': df.notna().sum(),
        'unique': df.nunique(),
        'total': df.shape[0],
        'top_values': df.apply(
            lambda col: (
                " / ".join((vc := col.value_counts(dropna=True)).index.astype(str)[:5])
                + (" / ..." if len(vc) > 5 else "")
            )
        ),
        'col_type': df.dtypes
    })

    # show summary statistics for numeric columns
    is_numeric = (
        summary_df['col_type'].eq('float64')
        | summary_df['col_type'].eq('int64')
    )
    if any(is_numeric):
        numeric_cols = summary_df.index[is_numeric]
        summary_stats = pd.DataFrame({
            "not_na": df[numeric_cols].notna().sum(),
            "total": df[numeric_cols].shape[0],
            "mean": df[numeric_cols].mean().round(2),
            "median": df[numeric_cols].median().round(2),
            "std_dev": df[numeric_cols].std().round(2),
            "min": df[numeric_cols].min().round(2),
            "max": df[numeric_cols].max().round(2),
        })
        display_collapsible_table(
            "Continuous variables",
            summary_stats.to_html(),
            open_by_default
        )
    else:
        print("No continuous variables found.")

    # show summary statistics for categorical columns
    summary_categorical = summary_df[~is_numeric].drop(columns=['col_type'])
    display_collapsible_table(
        "Categorical variables",
        summary_categorical.sort_index().to_html(),
        open_by_default
    )


def plot_metadata_summary(
    df: pd.DataFrame,
    group_attribute: str,
    count_attribute: str,
    bins: int | None = None,
) -> None:
    """
    Horizontal bar charts of sample counts, one panel per group.

    Each panel is one value of `group_attribute`. Bars are counts of `count_attribute`
    (missing values shown as "Not reported"), ordered by descending count. When `bins`
    is set, `count_attribute` is coerced to numeric and cut into that many equal-width
    ranges.

    Parameters:
    - df: Sample metadata (one row per sample).
    - group_attribute: Column used to split panels (e.g. Disease).
    - count_attribute: Column whose value frequencies are plotted.
    - bins: Number of equal-width ranges. If not None, `count_attribute` is coerced to numeric.

    Returns:
    - Displays a matplotlib figure (one panel per group value).
    """
    not_reported = 'Not reported'
    sentinels = {'Not reported': np.nan, '.': np.nan, None: np.nan}
    is_binned = bins is not None

    work = df[[group_attribute, count_attribute]].replace(sentinels)

    group_vals = (
        work[group_attribute]
        .map(scalar_value)
        .replace('', np.nan)
        .fillna(not_reported)
        .astype(str)
    )

    if is_binned:
        count_num = _soft_to_numeric(work[count_attribute])
        assert pd.api.types.is_numeric_dtype(count_num), (
            f"bins={bins!r} requires count_attribute {count_attribute!r} "
            "to be numeric-coercible (object columns with numeric values are OK)"
        )
        missing = count_num.isna()
        observed = count_num[~missing]
        n_unique = observed.nunique()
        decimals = _decimal_places(observed)
        spec = f'.{decimals}f'
        binned = pd.Series(index=work.index, dtype=object)
        if n_unique <= 1:
            binned[~missing] = observed.map(lambda v: format(v, spec))
        else:
            cats = pd.cut(observed, bins=min(bins, n_unique), duplicates='drop')
            binned.loc[observed.index] = cats.map(
                lambda iv: f'{iv.left:{spec}}-{iv.right:{spec}}'
            )
        count_vals = binned.fillna(not_reported)
    else:
        count_vals = (
            work[count_attribute]
            .map(scalar_value)
            .replace('', np.nan)
            .fillna(not_reported)
            .astype(str)
        )

    panels = pd.DataFrame({'group': group_vals, 'count_cat': count_vals})
    group_names = list(dict.fromkeys(panels['group']))
    n_panels = len(group_names)

    # rows are collected up front so every panel can share one y-scale
    panel_data: dict[str, pd.DataFrame] = {}
    for group_name in group_names:
        counts = panels.loc[panels['group'] == group_name, 'count_cat'].value_counts()

        # keep the missing-value bar out of the ordering logic, then pin it below
        n_missing = int(counts.get(not_reported, 0))
        counts = counts.drop(index=not_reported, errors='ignore')

        # ascending here: barh draws the first row at the bottom, so the
        # largest count ends up on top and reads as descending downwards
        rest = (
            counts.rename_axis('label')
            .reset_index(name='n')
            .sort_values(['n', 'label'], ascending=[True, False])
        )
        show_not_reported = not is_binned or n_missing > 0
        nr = [pd.DataFrame({'label': [not_reported], 'n': [n_missing]})]
        d = pd.concat(
            (nr if show_not_reported else []) + [rest],
            ignore_index=True,
        )
        d['n'] = d['n'].astype(int)
        panel_data[group_name] = d

    max_rows = max(len(d) for d in panel_data.values())
    colors = [GS_BLUE, GS_STEEL]
    fig, axes = plt.subplots(
        1, n_panels,
        figsize=(7 * max(n_panels, 1), max(4.0, 0.42 * max_rows + 1.4)),
        squeeze=False,
    )
    fig.patch.set_facecolor(GS_CLOUD)
    axes = axes[0]

    plt.suptitle(
        f'Sample metadata — {len(df):,} samples · '
        f'{n_panels} {group_attribute.lower()} values',
        fontsize=13, fontweight='bold', color=GS_INK, y=1.02,
    )

    panel_colors = (colors * ((n_panels + 1) // 2))[:n_panels]
    for ax, group_name, color in zip(axes, group_names, panel_colors):
        d = panel_data[group_name]
        # shorter panels are pushed up so all panels align at the top
        y_pos = np.arange(len(d)) + (max_rows - len(d))

        bars = ax.barh(
            y_pos, d['n'],
            color=color, alpha=0.88, height=0.65,
            edgecolor='white', linewidth=0.8,
        )
        ax.set_yticks(y_pos)
        ax.set_yticklabels(d['label'])
        ax.set_facecolor(GS_CLOUD)
        ax.set_title(
            f'{count_attribute} — {group_name}',
            fontweight='bold', fontsize=12, pad=10, color=GS_INK,
        )
        ax.set_xlabel('Samples', fontsize=10, color=GS_TEXT)
        ax.tick_params(colors=GS_TEXT)
        max_v = d['n'].max() or 1
        for bar, val in zip(bars, d['n']):
            ax.text(
                bar.get_width() + max_v * 0.01,
                bar.get_y() + bar.get_height() / 2,
                f'{int(val):,}', va='center', fontsize=9, color=GS_TEXT,
            )
        ax.set_xlim(0, max_v * 1.2)
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        # identical y-range keeps bar thickness equal across panels
        ax.set_ylim(-0.75, max_rows - 0.25)
        ax.spines['bottom'].set_color(GS_LINE)
        ax.spines['left'].set_color(GS_LINE)
        sns.despine(ax=ax)

    plt.tight_layout()
    plt.show()


def display_bulk_sc_comparison_summary(
    *,
    n_studies: int,
    n_bulk_datasets: int,
    n_sc_datasets: int,
    total_cells: int,
    n_panel_genes: int,
    n_cell_types: int,
    n_panel_de_cell_types: int,
    n_genomewide_cell_types: int,
    n_genomewide_genes: int,
    timings: dict[str, float] | None = None,
) -> None:
    """
    Closing narrative Summary filled from live run stats and ``ODM_TIMINGS``.
    
    Replaces the hand-written Summary markdown so counts and durations stay
    accurate when the cohort, gene panel, or instance contents change.
    
    Parameters:
    - n_studies / n_bulk_datasets / n_sc_datasets / total_cells: Step 1 overview.
    - n_panel_genes: Size of the analysed gene panel.
    - n_cell_types: Cell types used for composition / gene_summary queries.
    - n_panel_de_cell_types: Cell types with panel SC DE results.
    - n_genomewide_cell_types: Cell types with genome-wide SC DE for GSEA.
    - n_genomewide_genes: Typical gene count from genome-wide DE tables.
    - timings: Optional map of timer keys → seconds; default ``ODM_TIMINGS``.
      Expected keys: ``platform_overview``, ``cell_type_counts``,
      ``gene_summary``, ``panel_sc_de``, ``genomewide_sc_de``.
    
    Returns:
    - Displays an HTML summary block sized like notebook markdown cells.
    """
    if timings is None:
        from demo_utils.util import ODM_TIMINGS as timings
    t = timings
    n_ratio_calls = 2 * n_cell_types

    display(HTML(f"""
<div style="font-size:var(--jp-content-font-size1, 14px); line-height:1.5;
            font-family:var(--jp-content-font-family, -apple-system, BlinkMacSystemFont,
            'Segoe UI', Helvetica, Arial, sans-serif); color:inherit;">
  <p>This notebook walked through a bulk-to-single-cell investigation using ODM's
     Single-Cell Module and its analytical endpoints:</p>
  <ol>
    <li><b>Explored the platform</b> — one query surveyed everything available:
        <b>{n_studies}</b> studies, <b>{n_bulk_datasets}</b> bulk datasets,
        <b>{n_sc_datasets}</b> single-cell datasets,
        <b>{_fmt_cells(total_cells)}</b> cells, back in
        <b>{_fmt_duration(t.get('platform_overview'))}</b>.</li>
    <li><b>Bulk RNA-seq DE</b> — expression data for a {n_panel_genes}-gene panel
        was streamed from ODM, then DE was computed locally in the notebook.</li>
    <li><b>Single-cell exploration:</b>
      <ul>
        <li>cell-type composition came from <b>{n_ratio_calls}</b>
            <code>cell_ratio</code> calls ({n_cell_types} cell types × case + control),
            returning the full case-vs-control picture in
            <b>{_fmt_duration(t.get('cell_type_counts'))}</b>.</li>
        <li>per-cell-type expression via <code>gene_summary</code> for the
            {n_panel_genes}-gene panel — <b>{n_cell_types}</b> calls in
            <b>{_fmt_duration(t.get('gene_summary'))}</b>.</li>
        <li>single-cell DE computed server-side via
            <code>differential_expression</code>: the {n_panel_genes}-gene panel
            across {n_panel_de_cell_types} cell types in
            <b>{_fmt_duration(t.get('panel_sc_de'))}</b>.</li>
      </ul>
    </li>
    <li><b>Bulk vs. single-cell comparison</b> — with both results in hand, panel
        genes that were significant only at cell resolution stood out immediately.</li>
    <li><b>Pathway analysis</b> — genome-wide single-cell DE was retrieved from ODM,
        then GSEA was run locally in the notebook:
      <ul>
        <li><code>differential_expression</code> endpoint scaled to all
            <b>{_fmt_gene_scale(n_genomewide_genes)}</b> genes across
            {n_genomewide_cell_types} cell types ran in
            <b>{_fmt_duration(t.get('genomewide_sc_de'))}</b>.</li>
      </ul>
    </li>
  </ol>
</div>
"""))


def display_data_landscape(
    inventory_df: pd.DataFrame,
    case_studies: list,
    cell_type_counts_df: pd.DataFrame,
    cell_type_counts_ctrl_df: pd.DataFrame,
    genes: list[str],
    case_col: str,
    ctrl_col: str,
) -> None:
    """
    Closing summary card tying bulk inventory, SC cohorts, and the gene panel.
    
    Used in the Summary section to recap what data underpinned the demo
    (bulk studies/samples, SC cell counts, panel size).
    
    Parameters:
    - inventory_df: Bulk inventory with case / control sample-count columns.
    - case_studies: SC case studies used in the analysis.
    - cell_type_counts_df: Case cell-type counts (total_count).
    - cell_type_counts_ctrl_df: Control cell-type counts (total_count).
    - genes: Gene panel analysed in the notebook.
    - case_col: Inventory column with case sample counts.
    - ctrl_col: Inventory column with control sample counts.
    
    Returns:
    - Displays an HTML landscape / recap card.
    """
    n_bulk_studies = len(inventory_df)
    n_sc_studies   = len(case_studies)
    n_bulk_case    = inventory_df[case_col].sum()
    n_bulk_ctrl    = inventory_df[ctrl_col].sum()
    n_sc_cells     = int(
        cell_type_counts_df['total_count'].sum()
        + cell_type_counts_ctrl_df['total_count'].sum()
    )
    n_studies_accessed = n_bulk_studies + n_sc_studies
    n_bulk_samples = int(n_bulk_case + n_bulk_ctrl)
    n_panel_genes = len(genes)

    html = f"""
<div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
            max-width:860px;background:{GS_CLOUD};border:1px solid {GS_LINE};
            border-radius:12px;padding:24px 28px;margin:8px 0">

  <div style="font-size:13px;font-weight:700;color:{GS_TEXT};text-transform:uppercase;
              letter-spacing:.08em;margin-bottom:18px">
    Data accessed during this cohort analysis
  </div>

  <div style="display:flex;gap:12px">
    {"".join(f'''
    <div style="flex:1;background:white;border:1px solid {GS_LINE};border-radius:8px;
                padding:14px 16px;text-align:center">
      <div style="font-size:32px;font-weight:800;color:{col};line-height:1">{val:,}</div>
      <div style="font-size:11px;color:{GS_TEXT};margin-top:4px;font-weight:500">{lbl}</div>
    </div>''' for val, lbl, col in [
        (n_studies_accessed, 'Studies accessed',     GS_INK),
        (n_bulk_samples,     'Bulk samples',         GS_BLUE),
        (n_sc_cells,         'Cells',                GS_STEEL),
        (n_panel_genes,      'Panel genes queried',  GS_STEEL_PALE),
    ])}
  </div>
</div>
"""
    display(HTML(html))
