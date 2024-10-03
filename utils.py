import os
from pathlib import Path


import os
import pandas as pd
from typing import Union

POSSIBLE_TIMESTAMP_FORMATS = [
    "%Y-%m-%d %H:%M:%S",       # Common ISO-like format: '2023-10-02 14:30:59'
    "%d/%b/%Y:%H:%M:%S %z",    # Apache/Nginx logs: '02/Oct/2023:14:30:59 +0000'
    "%Y-%m-%dT%H:%M:%S",       # ISO 8601 format: '2023-10-02T14:30:59'
    "%Y-%m-%d %H:%M:%S.%f",    # With microseconds: '2023-10-02 14:30:59.123456'
    "%d/%m/%Y %H:%M:%S",       # European format: '02/10/2023 14:30:59'
    "%a, %d %b %Y %H:%M:%S %Z",# RFC 1123 format: 'Mon, 02 Oct 2023 14:30:59 GMT'
    "%Y/%m/%d %H:%M:%S",       # Slashed date format: '2023/10/02 14:30:59'
    "%m/%d/%Y %I:%M:%S %p",    # US format with AM/PM: '10/02/2023 02:30:59 PM'
    "%b %d %H:%M:%S",          # Syslog format: 'Oct 02 14:30:59'
    "%Y%m%d %H:%M:%S",         # Compact format: '20231002 14:30:59'
    "%Y-%m-%d",                # Date only: '2023-10-02'
    "%H:%M:%S",                # Time only: '14:30:59'
    "%Y%m%dT%H%M%S",           # Basic ISO 8601: '20231002T143059'
    "%Y-%m-%dT%H:%M:%S.%fZ",   # ISO 8601 with microseconds and 'Z' for UTC: '2023-10-02T14:30:59.123456Z'
    "%d-%b-%Y %H:%M:%S",       # Day-Month-Year format: '02-Oct-2023 14:30:59'
    "%Y%m%d",                  # Date only without separators: '20231002'
    "%d-%m-%Y",                # European date format: '02-10-2023'
    "%a %b %d %H:%M:%S %Y",    # C-style asctime format: 'Mon Oct 02 14:30:59 2023'
]

def concatenate_files(input_files, output_file):
    """Concatenate multiple files into one file."""
    directory = str(Path(output_file).parent)
    if not os.path.exists(directory):
      os.makedirs(directory)
    with open(output_file, 'w') as outfile:
        for input_file in input_files:
            with open(input_file, 'r') as infile:
                outfile.write(infile.read())

def str_to_datetime(ts: Union[pd.Series, str]):
    """Converts str timestamps to datetime object."""
    for ts_format in POSSIBLE_TIMESTAMP_FORMATS:
        try:
            #return pd.to_datetime(ts_series, unit="s") # audit 
            return pd.to_datetime(ts, format=ts_format) #apache
        except:
            continue
    raise ValueError("No timestamp format fits. Please, extend 'POSSIBLE_TIMESTAMP_FORMATS' with the required format.")

def decode_match_dict(match_dict: dict) -> dict:
    """Decode the match dictionary into str objects."""
    return dict(map(lambda item: (item[0], item[1].get_match_string().decode()), match_dict.items(),))

def get_timestamp_from_decoded_match_dict(match_dict: dict, default_timestamp_paths: list):
    for default_timestamp_path in default_timestamp_paths:
        ts_match = match_dict.get(default_timestamp_path, None)
        if ts_match is not None:
            return ts_match