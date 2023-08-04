import tkinter as tk
from tkinter import ttk
import pandas as pd


class DataFrameView:
    def __init__(self, container, df, title=""):
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
