from tkinter import ttk

from gui.df_view import DataFrameView


class FrameController:
    def __init__(self, root, df_title_pairs):
        container = ttk.Frame(root)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for df, title in df_title_pairs:
            frame = DataFrameView(container, df, title)
            self.frames[title] = frame.container
