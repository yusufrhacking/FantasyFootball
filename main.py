import pandas as pd
import glob
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


def main():
    csv_files = get_csv_files()
    dfs = [parse_csv_file(file) for file in csv_files if parse_csv_file(file) is not None]

    merged_df = merge_csv_files(dfs)

    if merged_df is None:
        print("No CSV files found.")
        return

    sorted_df = sort_by_projected_points(merged_df)

    qb_df = filter_by_position(sorted_df, ['QB'])
    other_positions_df = filter_by_position(sorted_df, ['RB', 'TE', 'WR'])

    print("QB DataFrame:")
    print(qb_df)
    print("\nOther Positions DataFrame:")
    print(other_positions_df)


if __name__ == "__main__":
    main()
