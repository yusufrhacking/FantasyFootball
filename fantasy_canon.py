import tkinter as tk
from data_processing.database_manager import get_players_data
from gui.rankings_app import PositionalRankingsApp


class FantasyCanonApp:
    def __init__(self, root):
        root.title("Fantasy Canon")
        root.geometry("1000x700")

        button = tk.Button(root, text="Open Positional Rankings", command=self.open_positional_rankings)
        button.pack(pady=20)

    def open_positional_rankings(self):
        # Create a new window for the PositionalRankingsApp
        new_window = tk.Toplevel()
        players_data = get_players_data()
        dfs = [(df, position) for position, df in players_data.items()]
        app = PositionalRankingsApp(new_window, dfs)