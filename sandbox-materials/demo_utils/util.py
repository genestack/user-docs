"""Small shared helpers (exported)."""

import re
import time
import json
from collections.abc import Iterator
from contextlib import contextmanager

import pandas as pd

from demo_utils._util import _quote_attr

# Wall-clock seconds recorded by odm_timer (keyed by ``key`` or ``label``).
ODM_TIMINGS: dict[str, float] = {}


@contextmanager
def odm_timer(label: str, *, key: str | None = None) -> Iterator[None]:
    """
    Context manager that times a block of ODM calls and shows a duration banner.
    
    Highlights that the query ran in-platform (vs download + local pipeline).
    Each run is also stored in ``ODM_TIMINGS`` under ``key`` (or ``label`` 
    if key is omitted) so the Summary section can quote live durations.
    
    Parameters:
    - label: Short description shown on the banner (e.g. query purpose).
    - key: Optional stable key for ``ODM_TIMINGS`` (use when ``label`` is dynamic).
    
    Returns:
    - On exit, displays an HTML timing banner; yields None.
    """
    from demo_utils.presentation import display_odm_timing
    t0 = time.time()
    yield
    dt = time.time() - t0
    ODM_TIMINGS[key or label] = dt
    display_odm_timing(label, dt)


def build_sample_filter(
    group_value: str,
    group_attribute: str,
    shared_filters: dict[str, str] | None = None,
) -> str:
    """
    Build an ODM sample_filter string for one group plus optional shared filters.
    
    Parameters:
    - group_value: Value of the primary grouping attribute (case or control).
    - group_attribute: Metadata field name (e.g. 'Disease', 'Treatment').
    - shared_filters: Extra field → value pairs AND-ed into the filter.
    
    Returns:
    - ODM sample_filter expression, e.g. ``Disease="UC" AND "Tissue General"="colon"``.
    """
    parts = [f'{_quote_attr(group_attribute)}="{group_value}"']
    for key, value in (shared_filters or {}).items():
        parts.append(f'{_quote_attr(key)}="{value}"')
    return ' AND '.join(parts)


def scalar_value(value: object) -> str:
    """
    Convert a metadata value to a plain string for display.
    
    Lists are joined with commas; falsy values become an empty string.
    
    Parameters:
    - value: Scalar or list-like metadata field.
    
    Returns:
    - Display-ready string.
    """
    if isinstance(value, list):
        return ', '.join(str(v) for v in value)
    return '' if value is None else value


def camel_case_keys(d: dict[str, object]) -> dict[str, object]:
    """
    Convert dictionary keys from snake_case to camelCase.
    
    Used when building ODM request bodies (e.g. sample_filter → sampleFilter).
    
    Parameters:
    - d: Mapping with snake_case keys.
    
    Returns:
    - New mapping with camelCase keys (values unchanged).
    """
    return {
        re.sub(r"_([a-z])", lambda m: m.group(1).upper(), k): v
        for k, v in d.items()
    }


def flatten_value(val: object) -> str:
    """
    Convert lists and dicts to readable strings for table display.

    Parameters:
    - val: Scalar, list, or dict value to flatten.

    Returns:
    - Display-ready string.
    """
    if isinstance(val, list):
        return ', '.join(str(v) for v in val)
    elif isinstance(val, dict):
        return json.dumps(val, indent=2)
    else:
        return val


def clean_expression_metadata(expression: pd.DataFrame) -> pd.DataFrame:
    """
    Flatten nested expression-group metadata into tabular columns.
    
    Expands itemOrigin keys (runSourceId, runId, groupId) and other nested
    dicts into top-level columns for joining with expression matrices.
    
    Parameters:
    - expression: Expression metadata table with nested fields.
    
    Returns:
    - Copy with flattened metadata columns.
    """
    # transforms extracted metadata from gene expression query
    df = expression.copy()
           
    # extract keys from itemOrigin
    for key in ['runSourceId', 'runId', 'groupId']:
        df[key] = df['itemOrigin'].apply(lambda x: x.get(key))
    
    # metadata
    df['Data Class'] = df['metadata'].apply(lambda x: x.get('Data Class'))

    # gene ids
    df['Features (string)'] = df['feature'].apply(lambda x: ' ,'.join(x.keys()))
    df['feature_id'] = df['feature'].apply(lambda x: x.get('feature_id'))
    df['gene'] = df['feature_id']
    df['geneId'] = df['feature'].apply(lambda x: x.get('geneId'))

    # expression
    df['value'] = df['value'].apply(lambda x: x.get('value'))

    columns_keep = ['runSourceId', 'runId', 'groupId', 'Data Class', 'Features (string)',
                    'gene', 'geneId', 'feature_id', 'value']
    new_df = df[columns_keep]
    return new_df