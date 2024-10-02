from typing import List, Optional

class Data:
    """
    This class contains all the information of the data and functionality for preprocessing.
    A data object acts as a single representation of the provided log files (including optional labels).
    """

    def __init__(
        self, 
        data_dir: Optional[str] = None,
        data_file_paths: Optional[list] = None,
        label_file_path: Optional[str] = None,
    ):
        self.data_dir = data_dir
        self.data_file_paths = data_file_paths
        self.label_file_path = label_file_path

    def get_df(self, parser):
        return
    
    def get_timestamps(self):
        return
    
    def get_labels(self):
        if self.label_file_path is None:
            raise AttributeError("No label file path was provided.")
        return