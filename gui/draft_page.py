import tkinter as tk
from tkinter import ttk


class DraftPageApp:
    def __init__(self, root, par_table):
        self.par_table = par_table
        root.title("Fantasy Draft Page")
        root.geometry("1200x800")
        root.configure(bg='#f0f0f0')  # Soft Gray Background

        # Top Frame for Title and Brief Instructions
        top_frame = ttk.Frame(root, padding="10")
        top_frame.pack(side="top", fill="both", expand=False)
        title_label = ttk.Label(top_frame, text="Fantasy Draft", font=("Helvetica", 24), foreground="#333333")
        title_label.pack(side="top", padx=5)
        instruction_label = ttk.Label(top_frame, text="Select players for your draft.", font=("Helvetica", 14), foreground="#555555")
        instruction_label.pack(side="top", padx=5)

        # Bottom Frame for Treeview and Action buttons
        bottom_frame = ttk.Frame(root, padding="10")
        bottom_frame.pack(side="top", fill="both", expand=True)

        # Treeview to display the PAR table
        self.tree = self.create_tree(bottom_frame)
        self.tree.grid(row=0, column=0, sticky="nsew")

        # Side Frame for Buttons and Additional Controls
        side_frame = ttk.Frame(bottom_frame, padding="20")
        side_frame.grid(row=0, column=1, sticky="nsew")

        # Button to Add a Player to the Draft
        draft_button = ttk.Button(side_frame, text="Draft Player", command=self.draft_player)
        draft_button.pack(pady=10)

        # Button to Remove a Player from the Draft
        remove_button = ttk.Button(side_frame, text="Remove Player", command=self.remove_player)
        remove_button.pack(pady=10)

        # Resizing Configuration
        bottom_frame.grid_columnconfigure(0, weight=3)
        bottom_frame.grid_columnconfigure(1, weight=1)
        bottom_frame.grid_rowconfigure(0, weight=1)

        # Styling
        style = ttk.Style()
        style.theme_use('default')
        style.configure('TFrame', background='#f0f0f0')  # Match frame background with root background
        style.configure('TButton', background='#d9d9d9')  # Soft color for buttons

    # Rest of your code (create_tree, draft_player, remove_player)

    def create_tree(self, root):
        tree = ttk.Treeview(root, selectmode="browse")
        tree["columns"] = list(self.par_table.columns)
        tree["show"] = "headings"

        # Create the columns with improved aesthetics
        for col in self.par_table.columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        colors = {
            'QB': '#1D5B79',  # Light Red
            'RB': '#468B97',  # Light Green
            'WR': '#EF6262',  # Light Blue
            'TE': '#F3AA60',  # Light Orange
        }

        # colors = {
        #     'QB': '#ED1C24',  # Vibrant Red
        #     'RB': '#F1D302',  # Vibrant Green
        #     'WR': '#235789',  # Vibrant Blue
        #     'TE': '#020100',  # Vibrant Orange
        # }

        # Insert the rows with position-based colors
        for index, row in self.par_table.iterrows():
            color = colors.get(row['Position'], '#ffffff')  # Default White
            tree.insert("", index, values=list(row), tags=row['Position'])

        # Apply the position-based colors
        for position, color in colors.items():
            tree.tag_configure(position, background=color)

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
