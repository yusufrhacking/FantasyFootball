import pandas as pd

from data_processing.fantasy_life_csv_processing import get_fantasy_life_csvs, parse_fantasy_life_csv, merge_dfs, \
    sort_by_projected_points, filter_by_position
from data_processing.pff_csv_processing import read_pff_csv

pff_projections_path = "../data/pff_projs/pff_all_projections.csv"


def get_df():
    csv_files = get_fantasy_life_csvs()
    temp_dfs = [parse_fantasy_life_csv(file) for file in csv_files if parse_fantasy_life_csv(file) is not None]
    fantasy_life_dfs = merge_dfs(temp_dfs)
    pff_dfs = read_pff_csv(pff_projections_path)

    merged_df = pd.merge(fantasy_life_dfs, pff_dfs, left_on='Player', right_on='playerName', how='left',
                         suffixes=('_fl', '_pff'))

    merged_df['Fantasy Life Projections'] = merged_df['Proj Pts']
    merged_df['PFF Projections'] = merged_df['fantasyPoints']

    merged_df['Avg Proj Pts'] = (merged_df['Proj Pts'] + merged_df['fantasyPoints']) / 2
    merged_df['Avg Proj Pts'] = merged_df['Avg Proj Pts'].round(1)

    # Select the columns for the final result dataframe
    result_df = merged_df[['Player', 'Position', 'Avg Proj Pts', 'Fantasy Life Projections', 'PFF Projections']]

    return result_df


def get_players():
    merged_df = get_df()
    sorted_df = sort_by_projected_points(merged_df)

    positions = ['QB', 'RB', 'WR', 'TE']
    position_dfs = {}

    for pos in positions:
        df = filter_by_position(sorted_df, [pos])
        df['Ranking'] = range(len(df))
        df = df[['Ranking', 'Player', 'Position', 'Avg Proj Pts', 'Fantasy Life Projections', 'PFF Projections']]
        position_dfs[pos] = df

    # Create the flex data frame with RB, WR, and TE combined
    flex_df = pd.concat([position_dfs['RB'], position_dfs['WR'], position_dfs['TE']])
    flex_df = sort_by_projected_points(flex_df).reset_index(drop=True)
    flex_df['Ranking'] = range(len(flex_df))
    position_dfs['FLEX'] = flex_df

    return position_dfs
