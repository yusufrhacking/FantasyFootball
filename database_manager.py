import sqlite3
import pandas as pd


def is_database_empty(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    return len(tables) == 0


def write_to_sqlite(players_dfs, conn):
    for pos, df in players_dfs.items():
        df.to_sql(pos, conn, if_exists='replace')


def read_from_sqlite(conn):
    positions = ["QB", "RB", "WR", "TE", "FLEX"]
    players_dfs = {}

    for position in positions:
        players_dfs[position] = pd.read_sql_query(f"SELECT * FROM {position}", conn)

    return players_dfs


def get_players_data(players_dfs=None):
    conn = sqlite3.connect('fantasy_football.sqlite3')

    if is_database_empty(conn) and players_dfs is not None:
        write_to_sqlite(players_dfs, conn)

    players_data = read_from_sqlite(conn)
    conn.close()

    return players_data
