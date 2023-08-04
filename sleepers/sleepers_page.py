from tkinter import ttk
import tkinter as tk

from data_processing.sleepers_processor import get_sleepers
from gui.player_df_view import PlayerDFView


class SleepersPageApp:
    def __init__(self, root, par_table, config):
        self.bottom_frame = None
        self.data_table = get_sleepers(par_table, config)
        # self.par_table = par_table
        root.title("Sleepers Page")
        root.geometry("1200x800")
        root.configure(bg='#f0f0f0')  # Soft Gray Background

        style = ttk.Style(root)
        style.theme_use("clam")
        style.configure("TFrame", background="lightgray")

        self.create_top_frame(root)
        player_df_view = PlayerDFView(root, self.data_table)
        # self.create_bottom_frame(root)

    def create_top_frame(self, root):
        top_frame = ttk.Frame(root, padding="10")
        top_frame.pack(side="top", fill="both", expand=False)
        self.add_title(top_frame)

    def add_title(self, frame):
        title_label = ttk.Label(frame, text="Sleepers", font=("Helvetica", 24), foreground="#333333")
        title_label.pack(side="top", padx=5)

    def create_bottom_frame(self, root):
        self.bottom_frame = ttk.Frame(root, padding="10")
        self.bottom_frame.pack(side="top", fill="both", expand=True)
        self.tree = self.create_tree(self.bottom_frame)
        self.tree.grid(row=0, column=0, sticky="nsew")

        self.bottom_frame.grid_columnconfigure(0, weight=3)
        self.bottom_frame.grid_columnconfigure(1, weight=1)
        self.bottom_frame.grid_rowconfigure(0, weight=1)


    def create_tree(self, root):
        tree = ttk.Treeview(root, selectmode="browse")
        tree["columns"] = list(self.data_table.columns)
        tree["show"] = "headings"

        self.create_columns(tree)
        self.insert_rows(tree)
        self.add_scrollbar(tree, root)

        return tree

    def create_columns(self, tree):
        for col in self.data_table.columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

    def insert_rows(self, tree):
        for index, row in self.data_table.iterrows():
            tree.insert("", index, values=list(row), tags=row['Position'])

    def add_scrollbar(self, tree, root):
        scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        tree.configure(yscrollcommand=scrollbar.set)
