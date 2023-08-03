import tkinter as tk
from data_processing.database_manager import get_players_data
from gui.rankings_app import PositionalRankingsApp


class FantasyCanonApp:
    def __init__(self, root, position_separated_dfs):
        root.title("Fantasy Canon")
        root.geometry("1000x700")
        self.position_separated_dfs = position_separated_dfs

        button = tk.Button(root, text="Open Positional Rankings", command=self.open_positional_rankings)
        button.pack(pady=20)

    def open_positional_rankings(self):
        # Create a new window for the PositionalRankingsApp
        new_window = tk.Toplevel()
        app = PositionalRankingsApp(new_window, self.position_separated_dfs)
