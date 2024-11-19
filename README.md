# Log-Preprocessor

This project is about preprocessing log lines in order to allow efficient and effective data analysis.

## **Installation**
Please install the [logdata-anomaly-miner](https://github.com/ait-aecid/logdata-anomaly-miner) (AMiner) first.

Next you can simply clone the repository from git:
```
git clone https://github.com/ait-aecid/log-preprocessor
```

## **Usage:**

A small example for how to use the **LogData** class from [LogData.py](LogData.py) is given in [example.ipynb](example.ipynb). The LogData class solely requires the parser name and the path to the folder containing the data as input parameters.

The file [AMinerModel.py](tools/AMinerModel.py) additionally contains the **AMinerModel**, which allows easy usage of the AMiner in a 'scikit-learn-like' way. Training and testing the model is thereby already possible with a few lines of code. Be aware that the execution in Jupyter notebooks requires sudo priviledges and will therefore ask for your password (this is not a good practice in general but necessary since the AMiner requires sudo priviledges).

