import tkinter as tk

from draft.draft_page import DraftPageApp
from gui.rankings_app import PositionalRankingsApp


class FantasyCanonApp:
    def __init__(self, root, par_table, position_separated_dfs, config):
        root.title("Fantasy Canon")
        root.geometry("1000x700")
        self.par_table = par_table
        self.position_separated_dfs = position_separated_dfs
        self.config = config

        button = tk.Button(root, text="Open Positional Rankings", command=self.open_positional_rankings)
        button.pack(pady=20)

        draft_button = tk.Button(root, text="Open Draft Page", command=self.open_draft_page)
        draft_button.pack(pady=20)

    def open_positional_rankings(self):
        # Create a new window for the PositionalRankingsApp
        new_window = tk.Toplevel()
        app = PositionalRankingsApp(new_window, self.position_separated_dfs)

    def open_draft_page(self):
        # Create a new window for the DraftPageApp
        draft_window = tk.Toplevel()
        app = DraftPageApp(draft_window, self.par_table, self.config)
