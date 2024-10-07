import os
import pandas as pd
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