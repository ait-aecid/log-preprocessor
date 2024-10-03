import sys
import importlib
from typing import Optional

sys.path.append("/usr/lib/logdata-anomaly-miner")
sys.path.append("/etc/aminer/conf-available/ait-lds")
from aminer.parsing.MatchElement import MatchElement
from aminer.parsing.MatchContext import MatchContext
from aminer.input.LogAtom import LogAtom
from aminer.parsing.ParserMatch import ParserMatch

from utils import *

class Parser:
    """Parser class for easy log parsing."""
    def __init__(self, parser_name: str, default_timestamp_paths: Optional[list]=None):
        self.parser_name = parser_name
        module = importlib.import_module(parser_name)
        self.parsing_model = module.get_model()
        self.default_timestamp_paths = default_timestamp_paths
    
    # copied from /usr/lib/logdata-anomaly-miner/aminer/input/ByteStreamLineAtomizer.py
    def parse_line(self, line_data: bytes, decode=False) -> dict:
        """Parse a single log line into a dictionary."""
        log_atom = LogAtom(line_data, None, None, None)
        match_context = MatchContext(line_data)
        match_element = self.parsing_model.get_match_element("", match_context)
        if match_element is None:
            return {}
        log_atom.parser_match = ParserMatch(match_element)
        match_dict = log_atom.parser_match.get_match_dictionary()
        if decode:
            return decode_match_dict(match_dict)
        return match_dict

    def parse_file(self, path: str, interval: Optional[tuple]=None, include_timestamps=False):
        """Parse log file. Returns parsed data including timestamps (in str format)."""
        match_dict_list = []
        with open(path, "rb") as file:
            if interval is None:
                for line_data in file:
                    match_dict_list.append(self.parse_line(line_data))
            else:
                for _ in range(interval[0]): # skip lines
                    file.readline()
                for i in range(interval[0], interval[1]):
                    line_data = file.readline().strip()
                    match_dict_list.append(self.parse_line(line_data))
        match_dict_list_decoded = [decode_match_dict(item) for item in match_dict_list]
        df = pd.DataFrame(match_dict_list_decoded)
        if include_timestamps:
            if self.default_timestamp_paths is not None:
                timestamps = [get_timestamp_from_decoded_match_dict(item, self.default_timestamp_paths) for item in match_dict_list_decoded]
                df["ts_str"] = timestamps
            else:
                raise ValueError("Variable 'default_timestamp_paths' is not set.")
        return df