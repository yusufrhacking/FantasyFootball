import pandas as pd

from data_processing.fantasy_life_csv_processing import get_fantasy_life_csvs, parse_fantasy_life_csv, merge_dfs, \
    sort_by_projected_points, filter_by_position
from data_processing.pff_csv_processing import read_pff_csv


def get_df(csv_files, pff_projections_path):
    temp_dfs = [parse_fantasy_life_csv(file) for file in csv_files if parse_fantasy_life_csv(file) is not None]
    fantasy_life_dfs = merge_dfs(temp_dfs)
    pff_dfs = read_pff_csv(pff_projections_path)

    merged_df = pd.merge(fantasy_life_dfs, pff_dfs, left_on='Player', right_on='playerName', how='left',
                         suffixes=('_fl', '_pff'))

    merged_df['Proj Pts'] = pd.to_numeric(merged_df['Proj Pts'], errors='coerce')
    merged_df['fantasyPoints'] = pd.to_numeric(merged_df['fantasyPoints'], errors='coerce')
    merged_df['Avg Proj Pts'] = merged_df[['Proj Pts', 'fantasyPoints']].mean(axis=1, skipna=True)
    merged_df['Avg Proj Pts'] = merged_df['Avg Proj Pts'].round(1)

    result_df = merged_df.rename(columns={
        'Proj Pts': 'Fantasy Life Projections',
        'fantasyPoints': 'PFF Projections'
    })[['Player', 'Position', 'Avg Proj Pts', 'Fantasy Life Projections', 'PFF Projections']]

    return result_df


def create_ranking_df(sorted_df, positions):
    df = filter_by_position(sorted_df, positions).copy()  # Make a copy after filtering
    df.reset_index(drop=True, inplace=True)
    df['Ranking'] = df.index
    return df[['Ranking', 'Player', 'Position', 'Avg Proj Pts', 'Fantasy Life Projections', 'PFF Projections']]



def get_players(merged_df, positions=None):
    if positions is None:
        positions = ['QB', 'RB', 'WR', 'TE']
    sorted_df = sort_by_projected_points(merged_df)
    position_dfs = {}

    for pos in positions:
        position_dfs[pos] = create_ranking_df(sorted_df, [pos])

    position_dfs['FLEX'] = create_ranking_df(sorted_df, ['RB', 'WR', 'TE'])

    position_dfs['OVR'] = create_ranking_df(sorted_df, ['QB', 'RB', 'WR', 'TE'])

    return position_dfs
