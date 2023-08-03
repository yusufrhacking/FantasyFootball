import tkinter as tk

from config_manager import load_config
from data_processing.database_manager import get_players_data
from fantasy_canon import FantasyCanonApp

def main():
    root = tk.Tk()

    config = load_config()
    number_of_teams = config['number_of_teams']
    position_requirements = config['position_requirements']

    players_data = get_players_data()
    dfs = [(df, position) for position, df in players_data.items()]

    app = FantasyCanonApp(root, dfs)
    root.mainloop()


if __name__ == "__main__":
    main()