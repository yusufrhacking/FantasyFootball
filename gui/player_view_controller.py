from tkinter import ttk

from gui.df_view import DataFrameView
from gui.player_df_view import PlayerDFView


class PlayerController:
    def __init__(self, root, df):
        container = ttk.Frame(root)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        frame = PlayerDFView(container, df)
