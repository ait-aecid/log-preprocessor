import getpass
import time
import os
import yaml
import pandas as pd

def copy_and_save_file(input_file_path: str, output_file_path: str, line_idx_list: list):
    """Write specified lines of the input file into the output file."""
    with open(input_file_path, 'r') as infile, open(output_file_path, 'w') as outfile:
        lines = infile.readlines()
        for line_number in line_idx_list:
            if 0 <= line_number < len(lines):
                outfile.write(lines[line_number])

class AMinerModel:
    """This class contains the functionality to train and test the AMiner in a 'scikit-learn'-like way."""

    def __init__(
            self,
            config: dict,
            permanent_permission=False,
            input_path="/tmp/aminer/current_data.log", # single input file - whole data (train + test)
            output_path="/tmp/aminer_out.json", # output file should be in /tmp
            tmp_dir="/tmp/aminer", 
        ):
        self.config = config
        self.tmp_dir = tmp_dir
        os.makedirs(tmp_dir, exist_ok=True)
        self.input_path = input_path
        self.output_path = output_path
        # probably not best practice but necessary as long as we use the aminer.py script
        self.password = None
        if permanent_permission:
            self.password = getpass.getpass("Enter sudo password: ")
    
    def run_AMiner(self, df: pd.DataFrame, training: bool, label: str):
        """Run AMiner with data in training or test mode."""
        tmp_input_path = os.path.join(self.tmp_dir, f"tmp_data_{label}.log")
        tmp_config_path = os.path.join(self.tmp_dir, f"tmp_config_{label}.yaml")
        # update config
        self.config["LearnMode"] = training
        self.config["LogResourceList"] = ["file://" + tmp_input_path]
        self.config["LogLineIdentifier"] = True
        self.config["EventHandlers"][0]["output_file_path"] = self.output_path
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
        if self.password is not None:
            os.system(f"echo {self.password} | sudo -S {command}")
        else:
            os.system(f"sudo {command}")

    def fit(self, df: pd.DataFrame, print_progress=True):
        """Train the AMiner with the given data."""
        if print_progress:
            print("Training AMiner ...")
        start = time.time()
        self.run_AMiner(df, training=True, label="train")
        self.last_runtime = time.time() - start
        if print_progress:
            print(f"Finished. (runtime: {self.last_runtime})")
    
    def predict(self, df: pd.DataFrame, print_progress=True):
        """Test the AMiner with the given data."""
        if print_progress:
            print("Testing AMiner ...")
        start = time.time()
        self.run_AMiner(df, training=False, label="test")
        self.last_runtime = time.time() - start
        if print_progress:
            print(f"Finished. (runtime: {self.last_runtime})")
        print("Raw results saved to:", self.output_path)
    
    def fit_predict(self, df_train: pd.DataFrame, df_test: pd.DataFrame, print_progress=True):
        """Train and test the AMiner with the given data."""
        self.fit(df_train, print_progress=print_progress)
        self.predict(df_test, print_progress=print_progress)
