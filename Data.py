
import os
import pandas as pd
from typing import Optional

from utils.utils import *
from utils.constants import POSSIBLE_TIMESTAMP_PATHS
from Parser import Parser

class Data:
    """A data object acts as a single representation of the provided log files (optionally including labels)."""

    def __init__(
        self, 
        data_dir: str,
        parser_name: str,
<<<<<<< HEAD
        tmp_save_path="tmp/current_data.log",
        parsed_data_dir="tmp/data_parsed/",
        #default_timestamp_paths: str,
        #label_file_path: Optional[str] = None,
        #input_filenames: Optional[list] = None,
    ):
        self.data_dir = data_dir
        self.input_filenames = os.listdir(self.data_dir)
        #self.label_file_path = label_file_path
=======
        default_timestamp_paths: str,
        tmp_save_path="tmp/current_data.log",
        parsed_data_dir="tmp/data_parsed/",
        # data_file_paths: Optional[list] = None,
    ):
        self.data_dir = data_dir
>>>>>>> 01254299b87b36fce3842ba28d7fb9f58cfe8186
        self.parser_name = parser_name
        self.parser = Parser(parser_name, POSSIBLE_TIMESTAMP_PATHS)
        self.default_timestamp_paths = POSSIBLE_TIMESTAMP_PATHS
        self.tmp_save_path = tmp_save_path
        self.parsed_data_dir = parsed_data_dir
        self.n_lines, self.start_timestamps = self._get_logfiles_info_from_dir()
        self.input_filepaths = self._get_input_filepaths(ordered=True) # order is crucial!!!

<<<<<<< HEAD
    # def get_labels():
    #     return
    
=======
>>>>>>> 01254299b87b36fce3842ba28d7fb9f58cfe8186
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
        n_lines = {}
        start_timestamps = {}
        for file in self.input_filenames:
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
<<<<<<< HEAD
            n_lines, start_timestamps = self.get_logfiles_info_from_dir()
            self.input_filenames = list(dict(sorted(start_timestamps.items(), key=lambda x: x[1])).keys()) # sort files
        self.input_filepaths = [os.path.join(self.data_dir, file) for file in self.input_filenames]
=======
            files = list(dict(sorted(self.start_timestamps.items(), key=lambda x: x[1])).keys()) # sort files
        self.input_filepaths = [os.path.join(self.data_dir, file) for file in files]
>>>>>>> 01254299b87b36fce3842ba28d7fb9f58cfe8186
        return self.input_filepaths