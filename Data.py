
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
        tmp_save_path="tmp/current_data.log",
        parsed_data_dir="tmp/data_parsed/",
        # data_file_paths: Optional[list] = None,
    ):
        self.data_dir = data_dir
        self.parser_name = parser_name
        self.parser = Parser(parser_name, default_timestamp_paths)
        self.default_timestamp_paths = default_timestamp_paths
        self.tmp_save_path = tmp_save_path
        self.parsed_data_dir = parsed_data_dir
        self.n_lines, self.start_timestamps = self._get_logfiles_info_from_dir()
        self.input_filepaths = self._get_input_filepaths(ordered=True) # order is crucial!!!

    def get_df(self, use_parsed_data=True) -> pd.DataFrame:
        """Get the data as a single dataframe."""
        concatenate_files(self.input_filepaths, self.tmp_save_path) # concat files and save to tmp folder
        if use_parsed_data: # for faster repeated data usage save parsed df
            filestorage_label = "-".join([p.split("/")[-1] for p in self.input_filepaths])
            filestorage_name = f"{filestorage_label}_{self.parser_name}.feather"
            os.makedirs(self.parsed_data_dir, exist_ok=True)
            parsed_data_path = os.path.join(self.parsed_data_dir, filestorage_name)
            root, dirs, files = list(os.walk(self.parsed_data_dir))[0]
            if filestorage_name in files: # get parsed file
                df = pd.read_feather(parsed_data_path)
                print("Retrieved previously parsed data.")
            else:
                df = self.parser.parse_file(self.tmp_save_path, None, True, "ts")
                df.to_feather(parsed_data_path)
                print("Saving parsed data.")
        else: # parse file
            df = self.parser.parse_file(self.tmp_save_path, None, True, "ts")
        return df

    def _get_logfiles_info_from_dir(self):
        """Returns number of lines and starting time of log files."""
        root, dirs, files = list(os.walk(self.data_dir))[0]
        n_lines = {}
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
        if ordered:
            files = list(dict(sorted(self.start_timestamps.items(), key=lambda x: x[1])).keys()) # sort files
        self.input_filepaths = [os.path.join(self.data_dir, file) for file in files]
        return self.input_filepaths