import pandas as pd


def read_adjustments_data(file_path):
    df = pd.read_csv(file_path)
    return df