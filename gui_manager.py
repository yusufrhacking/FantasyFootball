import tkinter as tk
from tkinter import ttk
import pandas as pd


class DataFrameView:
    def __init__(self, container, df, title):
        self.container = ttk.Frame(container)
        self.container.grid(row=0, column=0, sticky="nsew")

        self._add_header(title)
        self._create_tree_view(df)
        self._populate_tree_view(df)

    def _add_header(self, title):
        header_label = ttk.Label(self.container, text=title, font=('Helvetica', 16, 'bold'))
        header_label.pack(side=tk.TOP, pady=10, padx=20)

    def _create_tree_view(self, df):
        columns = tuple(df.columns)
        self.tree = ttk.Treeview(self.container, columns=columns, show="headings")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        scrollbar = ttk.Scrollbar(self.container, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)

    def _populate_tree_view(self, df):
        for index, row in df.iterrows():
            self.tree.insert("", tk.END, values=tuple(row))


class FrameController:
    def __init__(self, container, df_title_pairs):
        self.frames = {}
        for df, title in df_title_pairs:
            frame = DataFrameView(container, df, title)
            self.frames[title] = frame.container


class ButtonController:
    def __init__(self, root, frame_controller, button_texts):
        button_frame = ttk.Frame(root)
        button_frame.pack(side=tk.TOP, fill=tk.X)
        for text in button_texts:
            button = ttk.Button(button_frame, text=text, command=lambda f=frame_controller.frames[text]: f.tkraise())
            button.pack(side=tk.LEFT, padx=5, pady=5)


class FantasyFootballApp:
    def __init__(self, root, data_frames):
        root.title("Fantasy Football Projections")
        root.geometry("800x600")
        root.configure(bg='lightgray')

        style = ttk.Style(root)
        style.theme_use("clam")
        style.configure("TFrame", background="lightgray")  # Set background color for ttk.Frame widgets

        container = ttk.Frame(root)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Unpack the list of data frames and titles using zip
        dfs, titles = zip(*data_frames)
        frame_controller = FrameController(container, zip(dfs, titles))
        button_controller = ButtonController(root, frame_controller, titles)

        # Initially show the first frame in the list
        frame_controller.frames[titles[0]].tkraise()
