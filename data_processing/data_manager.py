import pandas as pd

from data_processing.adp_processing import read_adp_data
from data_processing.data_standardizer import standardize_name
from data_processing.fantasy_life_csv_processing import filter_by_position, get_fantasy_life_dfs
from data_processing.pff_csv_processing import read_pff_csv

pff_projections_path = "/Users/yusufhacking/Documents/Projects/FantasyFootball/data/pff_projs/pff_all_projections.csv"
adp_path = "/Users/yusufhacking/Documents/Projects/FantasyFootball/data/adp/4for4-adp-table.csv"


def run_data_pipeline():
    # raw data
    fantasy_life_df = get_fantasy_life_dfs()
    pff_df = read_pff_csv(pff_projections_path)
    adp_df = read_adp_data(adp_path)

    fantasy_life_df['Player'] = fantasy_life_df['Player'].apply(standardize_name)
    pff_df['playerName'] = pff_df['playerName'].apply(standardize_name)
    adp_df['Player'] = adp_df['Player'].apply(standardize_name)

    # Merge Fantasy Life DataFrame with PFF DataFrame
    merged_df = pd.merge(fantasy_life_df, pff_df, left_on='Player', right_on='playerName', how='left',
                         suffixes=('_fl', '_pff'))
    merged_df['Proj Pts'] = pd.to_numeric(merged_df['Proj Pts'], errors='coerce')
    merged_df['fantasyPoints'] = pd.to_numeric(merged_df['fantasyPoints'], errors='coerce')
    merged_df['Avg Proj Pts'] = merged_df[['Proj Pts', 'fantasyPoints']].mean(axis=1, skipna=True)
    merged_df['Avg Proj Pts'] = merged_df['Avg Proj Pts'].round(1)

    # Merge the above DataFrame with ADP DataFrame
    result_df = pd.merge(merged_df, adp_df, on='Player', how='left')

    # Rename columns and select the desired columns
    result_df = result_df.rename(columns={
        'Proj Pts': 'Fantasy Life Projections',
        'fantasyPoints': 'PFF Projections',
        'Y!': 'ADP_Yahoo'
    })[['Player', 'Position', 'Avg Proj Pts', 'Fantasy Life Projections', 'PFF Projections', 'ADP_Yahoo']]

    return result_df


def create_ranking_df(sorted_df, positions):
    df = filter_by_position(sorted_df, positions).copy()  # Make a copy after filtering
    df.reset_index(drop=True, inplace=True)
    df['Ranking'] = df.index
    return df[['Ranking', 'Player', 'Position', 'Avg Proj Pts',
               'Fantasy Life Projections', 'PFF Projections', 'ADP_Yahoo']]


def sort_by_projected_points(df, category):
    df.sort_values(by=category, ascending=False, inplace=True)
    return df


def get_players(merged_df, positions=None):
    if positions is None:
        positions = ['QB', 'RB', 'WR', 'TE']
    sorted_df = sort_by_projected_points(merged_df, 'Avg Proj Pts')
    position_dfs = {}

    for pos in positions:
        position_dfs[pos] = create_ranking_df(sorted_df, [pos])

    position_dfs['FLEX'] = create_ranking_df(sorted_df, ['RB', 'WR', 'TE'])

    position_dfs['OVR'] = create_ranking_df(sorted_df, ['QB', 'RB', 'WR', 'TE'])

    return position_dfs
