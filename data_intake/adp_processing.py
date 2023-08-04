import pandas as pd


def read_adp_data(file_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    adp_used = "Y!"

    filtered_df = df[["Player", adp_used]]

    filtered_df = filtered_df.rename(columns={adp_used: 'ADP'})
    filtered_df['ADP'] = pd.to_numeric(filtered_df['ADP'], errors='coerce')

    filtered_df['ADP'] = filtered_df['ADP'].fillna(0).astype(int)

    return filtered_df

