import os
import pandas as pd
import hashlib
from typing import Union
from pathlib import Path

from utils.constants import POSSIBLE_TIMESTAMP_FORMATS

def concatenate_files(input_files, output_file):
    """Concatenate multiple files into one file. Filepaths have to be sorted."""
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
            return pd.to_datetime(ts, format=ts_format)
        except:
            continue
    try: # unix time
        return pd.to_datetime(ts, unit="s") # audit
    except:
        pass
    raise ValueError("No timestamp format fits. Please, extend 'POSSIBLE_TIMESTAMP_FORMATS' with the required format.")

def decode_match_dict(match_dict: dict) -> dict:
    """Decode the match dictionary into str objects."""
    return dict(map(lambda item: (item[0], item[1].get_match_string().decode()), match_dict.items(),))

def get_timestamp_from_decoded_match_dict(match_dict: dict, default_timestamp_paths: list):
    """Returns the timestamp from the decoded match dict."""
    for default_timestamp_path in default_timestamp_paths:
        ts_match = match_dict.get(default_timestamp_path, None)
        if ts_match is not None:
            return ts_match
    raise ValueError("Timestamp could not be identified.")

def hash_string(input_string):
    """Hash a string."""
    hash_object = hashlib.sha256()
    hash_object.update(input_string.encode('utf-8'))
    return hash_object.hexdigest()