import getpass
import time
import os
import yaml
import pandas as pd
import json
import shutil
from typing import Optional

def copy_and_save_file(input_file_path: str, output_file_path: str, line_idx_list: list):
    """Write specified lines of the input file into the output file."""
    with open(input_file_path, 'r') as infile, open(output_file_path, 'w') as outfile:
        lines = infile.readlines()
        for line_number in line_idx_list:
            if 0 <= line_number < len(lines):
                outfile.write(lines[line_number])

def get_AMiner_results(path='/tmp/aminer_out.json', save=False, save_to="tmp/aminer_out.json") -> list:
    """Get output file generated the AMiner. JSON format is expected ('pretty=false')."""
    results = []
    with open(path, 'r') as file:
        for line in file:
            results.append(json.loads(line))
    if save:
        shutil.copy(path, save_to)
    return results

def extract_relevant_results(result: dict) -> dict:
    """Extract relevant results from a single result line from the AMiner results."""
    relevant_results = {
        "detector": result['AnalysisComponent']["AnalysisComponentType"],
        "feature": result['AnalysisComponent']["AffectedLogAtomPaths"],
        "idx": result["LogLineIdentifier"],
        "timestamp": pd.to_datetime(result['LogData']["Timestamps"], unit="s"),
        "crit": result['AnalysisComponent']["CriticalValue"] if "CriticalValue" in result['AnalysisComponent'].keys() else None,
        "id": result['AnalysisComponent']["AnalysisComponentName"],
    }
    return relevant_results

def get_AMiner_results_df(detectors: Optional[list], path='/tmp/aminer_out.json') -> dict:
    """Returns detector type, id of the triggered instance, line index, timestamp and variable(s) for each alert."""
    column_names = ["detector", "feature", "idx", "timestamp", "crit", "id"]
    results = get_AMiner_results(path)
    if len(results) == 0:
        return pd.DataFrame([], columns=column_names)
    relevant_results_list = []
    if detectors is not None: # if detectors are specified
        for detector in detectors:
            for result in results:
                if result['AnalysisComponent']["AnalysisComponentType"].startswith(detector):
                    relevant_results = extract_relevant_results(result)
                    relevant_results["detector"] = detector
                    relevant_results_list.append(relevant_results)
    else:
        for result in results:
            relevant_results_list.append(extract_relevant_results(result))
    return pd.DataFrame(relevant_results_list, columns=column_names)

class AMinerModel:
    """This class contains the functionality to train and test the AMiner in a 'scikit-learn'-like way."""

    def __init__(
            self,
            config: dict,
            input_path="/tmp/aminer/current_data.log", # single input file - whole data (train + test)
            output_path="/tmp/aminer_out.json", # output file should be in /tmp
            tmp_dir="/tmp/aminer", 
            files_suffix="",
            pwd=None # necessary for usage in jupyter notebooks
        ):
        self.config = config
        self.input_path = input_path
        self.output_path = output_path
        self.tmp_dir = tmp_dir
        os.makedirs(tmp_dir, exist_ok=True)
        self.files_suffix = files_suffix
        # probably not best practice but necessary for usage in jupyter notebooks
        self.pwd = pwd
    
    def run_AMiner(self, df: pd.DataFrame, training: bool, label: str) -> None:
        """Run AMiner with data in training or test mode."""
        tmp_input_path = os.path.join(self.tmp_dir, f"tmp_data_{label}{self.files_suffix}.log")
        tmp_config_path = os.path.join(self.tmp_dir, f"tmp_config_{label}{self.files_suffix}.yaml")
        # update config
        self.config["LearnMode"] = training
        self.config["LogResourceList"] = ["file://" + tmp_input_path]
        self.config["LogLineIdentifier"] = True
        self.config["EventHandlers"] = [{
            "id": "stpefile",
            "type": "StreamPrinterEventHandler",
            "json": True,
            "pretty": False,
            "output_file_path": self.output_path
        }]
        # save data for aminer
        copy_and_save_file(self.input_path, tmp_input_path, list(df.index))
        # parse to config file
        with open(tmp_config_path, "w") as file:
            yaml.dump(self.config, file, sort_keys=False, indent=4)
        # run AMiner (os.command is not really elegant - maybe change later)
        if training:
            clear_persistency = "-C"
        else:
            clear_persistency = ""
        command = f"aminer -o {clear_persistency} -c {tmp_config_path}"
        if self.pwd is not None:
            os.system(f"echo {self.pwd} | sudo -S {command}")
        else:
            os.system(f"sudo {command}")

    def fit(self, df: pd.DataFrame, print_progress=True) -> None:
        """Train the AMiner with the given data."""
        if print_progress:
            print("Training AMiner ...")
        start = time.time()
        self.run_AMiner(df, training=True, label="train")
        self.last_runtime = time.time() - start
        if print_progress:
            print(f"Finished. (runtime: {self.last_runtime})")
    
    def predict(self, df: pd.DataFrame, print_progress=True) -> None:
        """Test the AMiner with the given data."""
        if print_progress:
            print("Testing AMiner ...")
        start = time.time()
        self.run_AMiner(df, training=False, label="test")
        self.last_runtime = time.time() - start
        if print_progress:
            print(f"Finished. (runtime: {self.last_runtime})")
            print("Raw results saved to:", self.output_path)
    
    def fit_predict(self, df_train: pd.DataFrame, df_test: pd.DataFrame, print_progress=True) -> None:
        """Train and test the AMiner with the given data."""
        self.fit(df_train, print_progress=print_progress)
        self.predict(df_test, print_progress=print_progress)
    
    def get_latest_results_df(self, detectors: Optional[list]=None):
        """Returns latest results as a Dataframe."""
        results_df = get_AMiner_results_df(detectors, path=self.output_path)
        return results_df
