import tkinter as tk
from tkinter import ttk


class DraftPageApp:
    def __init__(self, root, par_table):
        self.par_table = par_table
        root.title("Draft Page")
        root.geometry("1200x800")
        root.configure(bg='lightgray')

        # Top Frame to house the title and brief instructions
        top_frame = ttk.Frame(root, padding="10")
        top_frame.pack(side="top", fill="both", expand=False)
        title_label = ttk.Label(top_frame, text="Fantasy Draft", font=("Helvetica", 20))
        title_label.pack(side="left", padx=5)
        instruction_label = ttk.Label(top_frame, text="Select players for your draft.", font=("Helvetica", 12))
        instruction_label.pack(side="left", padx=5)

        # Bottom Frame for Treeview and Action buttons
        bottom_frame = ttk.Frame(root, padding="10")
        bottom_frame.pack(side="top", fill="both", expand=True)

        # Treeview to display the PAR table
        self.tree = self.create_tree(bottom_frame)
        self.tree.grid(row=0, column=0, sticky="nsew")

        # Side frame for buttons and additional controls
        side_frame = ttk.Frame(bottom_frame)
        side_frame.grid(row=0, column=1, sticky="nsew")

        # Button to add a player to the draft
        draft_button = ttk.Button(side_frame, text="Draft Player", command=self.draft_player)
        draft_button.pack(pady=10)

        # Button to remove a player from the draft
        remove_button = ttk.Button(side_frame, text="Remove Player", command=self.remove_player)
        remove_button.pack(pady=10)

        # Resizing configuration
        bottom_frame.grid_columnconfigure(0, weight=3)
        bottom_frame.grid_columnconfigure(1, weight=1)
        bottom_frame.grid_rowconfigure(0, weight=1)

    def create_tree(self, root):
        tree = ttk.Treeview(root, selectmode="browse")
        tree["columns"] = list(self.par_table.columns)
        tree["show"] = "headings"

        # Create the columns with improved aesthetics
        for col in self.par_table.columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        # Insert the rows
        for index, row in self.par_table.iterrows():
            tree.insert("", index, values=list(row))

        # Adding a scrollbar
        scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        tree.configure(yscrollcommand=scrollbar.set)

        return tree

    def draft_player(self):
        # Code to handle drafting the selected player
        pass

    def remove_player(self):
        # Code to handle removing the selected player
        pass
