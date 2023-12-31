import sqlite3
import pandas as pd

from data_analysis.data_manager import run_rankings_pipeline, get_players


def is_database_empty(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    return len(tables) == 0


def write_to_sqlite(players_dfs, conn):
    for pos, df in players_dfs.items():
        df.to_sql(pos, conn, if_exists='replace')


def read_from_sqlite(conn):
    positions = ["OVR", "QB", "RB", "WR", "TE", "RB/WR/TE"]
    players_dfs = {}

    for position in positions:
        df = pd.read_sql_query(f"SELECT * FROM {position}", conn)
        # Drop the 'index' column from the DataFrame
        df = df.drop(columns='index', errors='ignore')
        players_dfs[position] = df

    return players_dfs


def get_players_data():
    # conn = sqlite3.connect('../data_intake/data/fantasy_football.sqlite3')
    total_df = run_rankings_pipeline()

    data_frames = get_players(total_df)
    # write_to_sqlite(data_frames, conn)
    #
    # players_data = read_from_sqlite(conn)
    # conn.close()

    players_data = data_frames
    return players_data
