import pandas as pd
import glob
import re


def get_fantasy_life_dfs():
    csv_files = get_fantasy_life_csvs()
    separated_dfs = [parse_fantasy_life_csv(file) for file in csv_files if parse_fantasy_life_csv(file) is not None]
    return merge_dfs(separated_dfs)


def get_fantasy_life_csvs():
    return glob.glob("/Users/yusufhacking/Documents/Projects/FantasyFootball/data_intake/data/dwain_projs/*.csv")


def parse_fantasy_life_csv(file):
    position_match = re.search(r"dwain_(\w+)_projections.csv", file)
    if position_match:
        position = position_match.group(1).upper()
        df = pd.read_csv(file)
        df['Position'] = position
        return df
    return None


def merge_dfs(dfs):
    return pd.concat(dfs, ignore_index=True) if dfs else None


def filter_by_position(df, positions):
    return df[df['Position'].isin(positions)]
