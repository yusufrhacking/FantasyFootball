import pandas as pd

from fantasy_life_csv_processing import get_fantasy_life_csvs, parse_fantasy_life_csv, merge_dfs, \
    sort_by_projected_points, filter_by_position
from pff_csv_processing import read_pff_csv

def get_df():
    csv_files = get_fantasy_life_csvs()
    temp_dfs = [parse_fantasy_life_csv(file) for file in csv_files if parse_fantasy_life_csv(file) is not None]
    fantasy_life_dfs = merge_dfs(temp_dfs)
    pff_dfs = read_pff_csv("pff_projs/pff_all_projections.csv")

    # Merge the Fantasy Life DataFrames with PFF DataFrame based on 'Player' and 'playerName' columns
    merged_df = pd.merge(fantasy_life_dfs, pff_dfs, left_on='Player', right_on='playerName', how='left', suffixes=('_fl', '_pff'))

    # Calculate the average projected points ('Avg Proj Pts') as the average of 'Proj Pts' and 'fantasyPoints'
    merged_df['Avg Proj Pts'] = (merged_df['Proj Pts'] + merged_df['fantasyPoints']) / 2

    # Select and return the desired columns
    result_df = merged_df[['Player', 'Position', 'Avg Proj Pts']]
    return result_df

def get_players():
    merged_df = get_df()
    sorted_df = sort_by_projected_points(merged_df)

    qb_df = filter_by_position(sorted_df, ['QB'])
    other_positions_df = filter_by_position(sorted_df, ['RB', 'TE', 'WR'])

    # Add a 'Ranking' column with sequential numbers starting from 0
    qb_df['Ranking'] = range(len(qb_df))
    other_positions_df['Ranking'] = range(len(other_positions_df))

    # Reorder columns
    qb_df = qb_df[['Ranking', 'Player', 'Position', 'Avg Proj Pts']]
    other_positions_df = other_positions_df[['Ranking', 'Player', 'Position', 'Avg Proj Pts']]

    return qb_df, other_positions_df
