import pandas as pd


def read_adp_data(file_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Filter down to the "Player" and "Y!" columns
    filtered_df = df[["Player", "Y!"]]

    return filtered_df

