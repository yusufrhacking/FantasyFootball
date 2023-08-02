import pandas as pd

def read_pff_csv(file_path):
    # Read the CSV file
    df = pd.read_csv(file_path)

    # Select only the required columns
    df = df[['playerName', 'position', 'fantasyPoints']]

    return df
