import tkinter as tk
import pandas as pd

class DraftPageApp:
    def __init__(self, root, par_table):
        root.title("Draft Page")
        root.geometry("1000x700")

        # You can create a Treeview to display the PAR table or any other widgets you need
        self.tree = self.create_tree(root, par_table)

        # Add other widgets or functionality as needed for the draft

    def create_tree(self, root, par_table):
        tree = tk.ttk.Treeview(root)
        tree["columns"] = list(par_table.columns)
        tree["show"] = "headings"

        # Create the columns
        for col in par_table.columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        # Insert the rows
        for index, row in par_table.iterrows():
            tree.insert("", index, values=list(row))

        tree.pack()

        return tree
