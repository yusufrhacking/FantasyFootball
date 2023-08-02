import pandas as pd
import glob
import re

def get_csv_files():
    return glob.glob("*.csv")

def parse_csv_file(file):
    position_match = re.search(r"dwain_(\w+)_projections.csv", file)
    if position_match:
        position = position_match.group(1).upper()
        df = pd.read_csv(file)
        df['Position'] = position
        return df
    return None

def merge_csv_files(dfs):
    return pd.concat(dfs, ignore_index=True) if dfs else None

def sort_by_projected_points(df):
    df.sort_values(by='Proj Pts', ascending=False, inplace=True)
    return df

def filter_by_position(df, positions):
    return df[df['Position'].isin(positions)][['Player', 'Position', 'Proj Pts']]