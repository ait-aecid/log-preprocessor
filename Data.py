
import os
import pandas as pd
from typing import Optional

from utils.utils import *
from Parser import Parser

class Data:
    """A data object acts as a single representation of the provided log files (optionally including labels)."""

    def __init__(
        self, 
        data_dir: str,
        parser_name: str,
        default_timestamp_paths: str,
        label_file_path: Optional[str] = None,
        tmp_save_path="tmp/current_data.log",
        parsed_data_dir="tmp/data_parsed/",
        #data_file_paths: Optional[list] = None,
    ):
        self.data_dir = data_dir
        #self.data_file_paths = data_file_paths
        self.label_file_path = label_file_path
        self.parser_name = parser_name
        self.parser = Parser(parser_name, default_timestamp_paths)
        self.default_timestamp_paths = default_timestamp_paths
        self.tmp_save_path = tmp_save_path
        self.parsed_data_dir = parsed_data_dir
        self.input_filepaths = self._get_input_filepaths(ordered=True)

    def get_labels(): #TO-DO
        return
    
    def get_df(self, use_parsed_data=True) -> pd.DataFrame:
        """Get the data as a single dataframe."""
        concatenate_files(self.input_filepaths, self.tmp_save_path) # concat files and save to tmp folder
        # for faster repeated data usage save parsed df to .h5 file
        if use_parsed_data:
            h5_label = "-".join([p.split("/")[-1] for p in self.input_filepaths])
            h5_filename = f"{h5_label}_{self.parser_name}.h5"
            os.makedirs(self.parsed_data_dir, exist_ok=True)
            parsed_data_path = os.path.join(self.parsed_data_dir, h5_filename)
            root, dirs, files = list(os.walk(self.parsed_data_dir))[0]
            if h5_filename in files: # get parsed file
                df = pd.read_hdf(parsed_data_path, 'df')
                print("Got parsed data from .h5 file.")
            else:
                df = self.parser.parse_file(self.tmp_save_path, None, True, "ts")
                df.to_hdf(parsed_data_path, key='df', mode='w') 
                print("Saving parsed data to .h5 file.")
        else: # parse file
            df = self.parser.parse_file(self.tmp_save_path, None, True, "ts")
        return df

    def get_logfiles_info_from_dir(self):
        """Returns number of lines and starting time of log files."""
        root, dirs, files = list(os.walk(self.data_dir))[0]
        n_lines = {}
        # get files sorted by start times of data files
        start_timestamps = {}
        for file in files:
            path = os.path.join(self.data_dir, file)
            with open(path, "rb") as f:
                for line in f:
                    parsed_line = self.parser.parse_line(line, decode=True)
                    timestamp_string = get_timestamp_from_decoded_match_dict(parsed_line, self.default_timestamp_paths)
                    start_timestamps[file] = str_to_datetime(timestamp_string)
                    break # get only first line
            with open(path, "r") as f:
                n_lines[file] = sum(1 for _ in f) # get number of lines for offset
        return n_lines, start_timestamps

    def _get_input_filepaths(self, ordered=False):
        """Return input filespaths."""
        root, dirs, files = list(os.walk(self.data_dir))[0]
        if ordered:
            n_lines, start_timestamps = self.get_logfiles_info_from_dir()
            files = list(dict(sorted(start_timestamps.items(), key=lambda x: x[1])).keys()) # sort files
        self.input_filepaths = [os.path.join(self.data_dir, file) for file in files]
        return self.input_filepaths