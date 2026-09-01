"""Small shared helpers (not exported)."""

import re

import numpy as np
import pandas as pd
from matplotlib.ticker import AutoLocator


def _quote_attr(name: str) -> str:
    """Quote an ODM metadata field name when it contains spaces."""
    return f'"{name}"' if ' ' in name else name


def _fmt_duration(seconds: float | None) -> str:
    """Format seconds as a short duration string (e.g. ``12.3s``, ``~10 minutes``)."""
    if seconds is None:
        return '—'
    if seconds < 90:
        return f'{seconds:.1f}s'
    minutes = seconds / 60
    if minutes < 10:
        return f'~{minutes:.1f} minutes'
    return f'~{minutes:.0f} minutes'


def _fmt_cells(n: int) -> str:
    """Format a cell count for display (e.g. ``~4.1M``, ``12,345``)."""
    if n >= 1_000_000:
        return f'~{n / 1_000_000:.1f}M'
    return f'{n:,}'


def _fmt_gene_scale(n: int) -> str:
    """Format a large gene count rounded down to thousands (e.g. ``~16,000+``)."""
    if n >= 1000:
        return f'~{n // 1000 * 1000:,}+'
    return str(n)


def _soft_to_numeric(s: pd.Series) -> pd.Series:
    try:
        return pd.to_numeric(s, errors="raise")
    except (ValueError, TypeError):
        return s


def _decimal_places(s: pd.Series) -> int:
    """Max decimal places among original numeric values (0 if all integral)."""
    s = s.dropna()
    if s.empty or (s == s.round(0)).all():
        return 0
    n = 0
    for v in pd.unique(s):
        text = format(float(v), 'f').rstrip('0')
        if '.' in text:
            n = max(n, len(text.split('.')[1]))
    return n


def _short_label(k: str) -> str:
    r"""Shorten the label to the Genestack accession (GSF\d+) or first 12 characters."""
    m = re.search(r'(GSF\d+)', k)
    return m.group(1) if m else k[:12]


def _rename_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Rename duplicate index entries: first occurrence unchanged, subsequent get _1, _2, ..."""
    counts = {}
    new_index = []
    for name in df.index:
        if name in counts:
            counts[name] += 1
            new_index.append(f"{name}_{counts[name]}")
        else:
            counts[name] = 0
            new_index.append(name)
    df = df.copy()
    df.index = new_index
    return df


def _ordered_categories(series: pd.Series, fill_na_color: str) -> list:
    """Categories in order of appearance, missing ones last as fill_na_color."""
    cats = [c for c in series.dropna().unique() if c != fill_na_color]
    return cats + ([fill_na_color] if series.isna().any() else [])


def _get_adata_gene_values(adata, gene: str) -> np.ndarray:
    """Return a flat expression vector for ``gene`` from an AnnData object."""
    x = adata[:, gene].X
    if hasattr(x, "toarray"):
        x = x.toarray()
    return np.asarray(x).ravel()


def _shared_vmin_vmax(adatas, gene: str, qmax: float = 98) -> tuple[float, float]:
    """
    Shared colour-scale limits for a gene across multiple AnnData objects.
    
    ``vmin`` is 0; ``vmax`` is the qmax-th percentile of positive values
    (floored at the max positive value), with a safe fallback when empty.
    """
    vals = np.concatenate([_get_adata_gene_values(a, gene) for a in adatas])
    vmin = 0.0
    positive = vals[vals > 0]
    if positive.size == 0:
        vmax = 1.0
    else:
        vmax = float(np.percentile(positive, qmax))
        vmax = max(vmax, float(positive.max()))
    if vmax <= vmin:
        vmax = vmin + 1.0
    return vmin, vmax


def _enable_umap_axis_ticks(ax) -> None:
    """Show UMAP1/UMAP2 axis labels and major ticks on a Scanpy UMAP axis."""
    ax.set_xlabel("UMAP1")
    ax.set_ylabel("UMAP2")
    ax.xaxis.set_major_locator(AutoLocator())
    ax.yaxis.set_major_locator(AutoLocator())
    ax.tick_params(
        axis="both",
        which="major",
        bottom=True,
        left=True,
        labelbottom=True,
        labelleft=True,
        labelsize=9,
    )
