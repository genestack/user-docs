"""ODM API query helpers (pagination, expression, discovery)."""

import inspect
from collections.abc import Callable
from typing import Any


def get_all_data(api_call: Callable[..., Any], **kwargs: Any) -> list:
    """
    Retrieve all pages from a cursor- or offset-paginated ODM API call.
    
    Parameters:
    - api_call: Bound API method that accepts cursor= or page_offset=.
    - **kwargs: Forwarded to each page request.
    
    Returns:
    - Concatenated response.data items from all pages.
    """
    data = []
    sig = inspect.signature(api_call)
    uses_cursor = 'cursor' in sig.parameters
    uses_offset = 'page_offset' in sig.parameters
    if uses_cursor:
        cursor = None
        while True:
            response = api_call(cursor=cursor, **kwargs)
            data.extend(response.data)
            if not response.data or getattr(response, 'results_exhausted', False):
                break
            if cursor == response.cursor:
                break
            cursor = response.cursor
    elif uses_offset:
        offset = 0
        while True:
            response = api_call(page_offset=offset, **kwargs)
            data.extend(response.data)
            pagination = response.meta.pagination
            offset += pagination.count
            if offset >= pagination.total:
                break
    else:
        raise ValueError(f"{api_call.__name__} supports neither cursor nor page_offset pagination")
    return data



