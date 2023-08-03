import tkinter as tk

from config_manager import load_config
from data_processing.database_manager import get_players_data
from data_processing.rankings_processor import RankingsProcessor
from fantasy_canon import FantasyCanonApp

def main():
    root = tk.Tk()

    config = load_config()
    number_of_teams = config['number_of_teams']
    position_requirements = config['position_requirements']

    players_data = get_players_data()

    overall_ranking_dfs = players_data['OVR']
    rankings_processor = RankingsProcessor(overall_ranking_dfs, position_requirements, number_of_teams)
    replacement_level_players = rankings_processor.find_replacement_level_players()

    position_separated_dfs = [(df, position) for position, df in players_data.items()]

    app = FantasyCanonApp(root, position_separated_dfs)
    root.mainloop()


if __name__ == "__main__":
    main()