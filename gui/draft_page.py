import tkinter as tk
from tkinter import ttk

from gui.team_sidebar import TeamSidebar


class DraftPageApp:
    def __init__(self, root, par_table, config):
        self.bottom_frame = None
        self.par_table = par_table
        root.title("Fantasy Draft Page")
        root.geometry("1200x800")
        root.configure(bg='#f0f0f0')  # Soft Gray Background

        self.create_top_frame(root)
        self.create_bottom_frame(root)

        side_frame = ttk.Frame(self.bottom_frame, padding="20")
        side_frame.grid(row=0, column=1, sticky="nsew")
        self.team_sidebar = TeamSidebar(side_frame, self.draft_player, config['position_requirements'])

    def create_top_frame(self, root):
        top_frame = ttk.Frame(root, padding="10")
        top_frame.pack(side="top", fill="both", expand=False)
        self.add_title(top_frame)
        self.add_instruction(top_frame)

    def add_title(self, frame):
        title_label = ttk.Label(frame, text="Fantasy Draft", font=("Helvetica", 24), foreground="#333333")
        title_label.pack(side="top", padx=5)

    def add_instruction(self, frame):
        instruction_label = ttk.Label(frame, text="Select players for your draft.", font=("Helvetica", 14),
                                      foreground="#555555")
        instruction_label.pack(side="top", padx=5)

    def create_bottom_frame(self, root):
        self.bottom_frame = ttk.Frame(root, padding="10")
        self.bottom_frame.pack(side="top", fill="both", expand=True)
        self.tree = self.create_tree(self.bottom_frame)
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.create_side_frame(self.bottom_frame)

        self.bottom_frame.grid_columnconfigure(0, weight=3)
        self.bottom_frame.grid_columnconfigure(1, weight=1)
        self.bottom_frame.grid_rowconfigure(0, weight=1)

    def create_side_frame(self, bottom_frame):
        side_frame = ttk.Frame(bottom_frame, padding="20")
        side_frame.grid(row=0, column=1, sticky="nsew")
        self.create_draft_button(side_frame)
        self.create_remove_button(side_frame)

    def create_draft_button(self, side_frame):
        draft_button = ttk.Button(side_frame, text="Draft Player", command=self.draft_player)
        draft_button.pack(pady=10)

    def create_remove_button(self, side_frame):
        remove_button = ttk.Button(side_frame, text="Remove Player", command=self.remove_player)
        remove_button.pack(pady=10)

    def create_tree(self, root):
        tree = ttk.Treeview(root, selectmode="browse")
        tree["columns"] = list(self.par_table.columns)
        tree["show"] = "headings"

        self.create_columns(tree)
        self.insert_rows(tree)
        self.apply_row_colors(tree)
        self.add_scrollbar(tree, root)

        return tree

    def create_columns(self, tree):
        for col in self.par_table.columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

    def insert_rows(self, tree):
        for index, row in self.par_table.iterrows():
            tree.insert("", index, values=list(row), tags=row['Position'])

    def apply_row_colors(self, tree):
        colors = {
            'QB': '#1D5B79',
            'RB': '#468B97',
            'WR': '#EF6262',
            'TE': '#F3AA60',
        }

        for position, color in colors.items():
            tree.tag_configure(position, background=color)

    def add_scrollbar(self, tree, root):
        scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        tree.configure(yscrollcommand=scrollbar.set)

    def draft_player(self):
        selected_item = self.tree.selection()[0]
        player_data = self.tree.item(selected_item)['values']
        position = player_data[1]  # Assuming the position is at index 1
        self.team_sidebar.add_player(player_data)
        self.tree.delete(selected_item)

    def remove_player(self):
        selected_index = self.team_sidebar.get_selected_index()
        player_data = self.team_sidebar.drafted_players[selected_index]
        self.team_sidebar.remove_player(selected_index)
        self.tree.insert("", tk.END, values=player_data, tags=player_data['Position'])
