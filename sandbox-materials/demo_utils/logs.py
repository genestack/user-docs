"""Log extraction helpers."""

import re
import json
import pandas as pd
from IPython.display import display, HTML

def display_log_records(logs: bytes | str) -> None:
    """
    Display structured log records as a left-aligned, scrollable HTML table.

    Parses log output for JSON records, extracts relevant fields, and renders them
    in a pandas DataFrame as an HTML table for easy viewing in Jupyter notebooks.

    Parameters:
    - logs: Raw log output from transformation jobs.

    Returns:
    - Displays the HTML table, or prints a message if no records are found.
    """
    logs_str = logs.decode('utf-8') if isinstance(logs, bytes) else logs

    # find all JSON log records (those starting with '{"record":')
    json_records = re.findall(r'{"record":.*?}\n', logs_str)
    records = []
    for rec in json_records:
        try:
            record = json.loads(rec)['record']
            records.append(record)
        except Exception:
            pass
    if records:
        df_logs = pd.DataFrame([{
            'Time': r.get('time', {}).get('repr', ''),
            'Level': r.get('level', {}).get('name', ''),
            'Message': r.get('message', ''),
        } for r in records])
        html_table = df_logs.to_html(index=False)

        # add CSS for left alignment
        html_table = html_table.replace('<table', '<table style="text-align:left"')
        html_table = html_table.replace('<td>', '<td style="text-align:left">')
        html_table = html_table.replace('<th>', '<th style="text-align:left">')
        html_table = f'''
            <div style="height:400px; overflow:auto; border:1px solid #ccc;">
            {html_table}
            </div>
            '''
        display(HTML(html_table))
    else:
        print('No log records found.')

def extract_accessions_from_logs(logs: bytes | str) -> dict[str, str | None]:
    """
    Extract group accessions from transformation job logs.

    Parses structured JSON log records and returns the accessions for
    the cell, library, and expression groups produced during the job.

    Parameters:
    - logs: Raw log output from jobs_api.post_api_v1_transformations_jobs_by_id_logs().

    Returns:
    - Dict with keys 'sample_group_accession', 'library_group_accession',
      'preparation_group_accession', 'cell_group_accession',
      'expression_group_accession', and 'study_group_accession'; values are
      accession strings (e.g. 'GSF000136') or None if not found.
    """
    logs_str = logs.decode('utf-8') if isinstance(logs, bytes) else logs
    json_records = re.findall(r'{"record":.*?}\n', logs_str)

    patterns = {
        'sample_group_accession': r'[Ss]ample group accession[^:]*:\s*(GSF\w+)',
        'library_group_accession': r'[Ll]ibrary group accession[^:]*:\s*(GSF\w+)',
        'preparation_group_accession': r'[Pp]reparation group accession[^:]*:\s*(GSF\w+)',
        'cell_group_accession': r'[Cc]ell group accession[^:]*:\s*(GSF\w+)',
        'expression_group_accession': r'[Ee]xpression group accession[^:]*:\s*(GSF\w+)',
        'study_group_accession': r'[Ss]tudy accession[^:]*:\s*(GSF\w+)',
    }

    accessions = {key: None for key in patterns}
    for rec in json_records:
        try:
            msg = json.loads(rec)['record'].get('message', '')
            for key, pattern in patterns.items():
                if accessions[key] is None:
                    m = re.search(pattern, msg)
                    if m:
                        accessions[key] = m.group(1)
        except Exception:
            pass

    return accessions