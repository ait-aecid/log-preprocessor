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

def run_AMiner(df: pd.DataFrame, input_path: str, output_path: str, config: dict, training: bool, label: str, tmp_dir="/tmp", password=None):
    """Run AMiner with data in training or test mode."""
    tmp_input_path = os.path.join(tmp_dir, f"tmp_data_{label}.log")
    tmp_config_path = os.path.join(tmp_dir, f"tmp_config_{label}.yaml")
    # update config
    config["LearnMode"] = training
    config["LogResourceList"] = ["file://" + tmp_input_path]
    config["LogLineIdentifier"] = True
    config["EventHandlers"][0]["output_file_path"] = output_path
    # save data for aminer
    copy_and_save_file(input_path, tmp_input_path, list(df.index))
    # parse to config file
    with open(tmp_config_path, "w") as file:
        yaml.dump(config, file, sort_keys=False, indent=4)
    # run AMiner (os.command is not really elegant - maybe change later)
    if training:
        clear_persistency = "-C"
    else:
        clear_persistency = ""
    command = f"aminer -o {clear_persistency} -c {tmp_config_path}"
    if password is not None:
        os.system(f"echo {password} | sudo -S {command}")
    else:
        os.system(f"sudo {command}")