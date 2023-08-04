import tkinter as tk
from tkinter import ttk
import pandas as pd


class PlayerDFView:
    def __init__(self, container, df):
        self.container = ttk.Frame(container, padding="10")
        self.df = df
        self.create_bottom_frame(container)

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
        tree["columns"] = list(self.df.columns)
        tree["show"] = "headings"

        self.create_columns(tree)
        self.insert_rows(tree)
        self.add_scrollbar(tree, root)

        return tree

    def create_columns(self, tree):
        for col in self.df.columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

    def insert_rows(self, tree):
        for index, row in self.df.iterrows():
            tree.insert("", index, values=list(row), tags=row['Position'])

    def add_scrollbar(self, tree, root):
        scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        tree.configure(yscrollcommand=scrollbar.set)
