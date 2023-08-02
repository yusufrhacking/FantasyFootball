from csv_processing import get_csv_files, parse_csv_file, merge_csv_files, sort_by_projected_points, filter_by_position

def get_df():
    csv_files = get_csv_files()
    dfs = [parse_csv_file(file) for file in csv_files if parse_csv_file(file) is not None]
    return merge_csv_files(dfs)

def get_players():
    merged_df = get_df()
    sorted_df = sort_by_projected_points(merged_df)
    qb_df = filter_by_position(sorted_df, ['QB'])
    other_positions_df = filter_by_position(sorted_df, ['RB', 'TE', 'WR'])
    return qb_df, other_positions_df
