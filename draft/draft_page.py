import tkinter
from tkinter import ttk

from draft.draft_manager import DraftManager
from draft.team_sidebar import TeamSidebar


class DraftPageApp:
    def __init__(self, root, par_table, config):
        self.bottom_frame = None
        # self.par_table = par_table
        root.title("Fantasy Draft Page")
        root.geometry("1200x800")
        root.configure(bg='#f0f0f0')  # Soft Gray Background

        style = ttk.Style(root)
        style.theme_use("clam")
        style.configure("TFrame", background="lightgray")

        self.draft_manager = DraftManager(par_table, config)
        self.create_banner(root)

        self.create_top_frame(root)
        self.create_bottom_frame(root)

        side_frame = ttk.Frame(self.bottom_frame, padding="20")
        side_frame.grid(row=0, column=1, sticky="nsew")

        self.team_sidebar = TeamSidebar(side_frame, self.draft_player, self.draft_manager)

    def create_top_frame(self, root):
        top_frame = ttk.Frame(root, padding="10")
        top_frame.pack(side="top", fill="both", expand=False)
        self.add_title(top_frame)

    def add_title(self, frame):
        title_label = ttk.Label(frame, text="Fantasy Draft", font=("Helvetica", 24), foreground="#333333")
        title_label.pack(side="top", padx=5)

    def create_bottom_frame(self, root):
        self.search_bar = ttk.Entry(root)
        self.search_bar.pack()

        self.bottom_frame = ttk.Frame(root, padding="10")
        self.bottom_frame.pack(side="top", fill="both", expand=True)
        self.tree = self.create_tree(self.bottom_frame)
        self.tree.grid(row=0, column=0, sticky="nsew")

        self.bottom_frame.grid_columnconfigure(0, weight=3)
        self.bottom_frame.grid_columnconfigure(1, weight=1)
        self.bottom_frame.grid_rowconfigure(0, weight=1)

        self.search_bar.bind('<KeyRelease>', self.update_tree)


    def create_tree(self, root):
        tree = ttk.Treeview(root, selectmode="browse")
        tree["columns"] = list(self.draft_manager.get_draftable_players().columns)
        tree["show"] = "headings"

        self.create_columns(tree)
        self.insert_rows(tree)
        self.apply_row_colors(tree)
        self.add_scrollbar(tree, root)

        tree.bind('<Return>', self.on_enter)

        return tree

    def update_tree(self, event):
        query = self.search_bar.get().lower()  # Get the current search query
        self.tree.delete(*self.tree.get_children())  # Delete all existing items from the tree
        for row in self.draft_manager.get_draftable_players().itertuples():  # Iterate through your original data
            # Check if the query matches any part of the row
            if query in str(row).lower():
                self.tree.insert("", "end", values=row[1:])  # Insert only the matching rows into the tree

    def create_columns(self, tree):
        for col in self.draft_manager.get_draftable_players().columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

    def insert_rows(self, tree):
        for index, row in self.draft_manager.get_draftable_players().iterrows():
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

    def create_banner(self, root):
        banner_frame = tkinter.Frame(root, bg="#468B97", padx=10, pady=10)
        banner_frame.pack(side="top", fill="both", expand=False)

        separator_above = ttk.Separator(banner_frame, orient="horizontal")
        separator_above.pack(side="top", fill="x", padx=5, pady=5)

        self.banner_label = ttk.Label(banner_frame, text=self.get_next_teams_text(),
                                      font=("Helvetica", 16, "bold"), foreground="#f0f0f0",
                                      background="#468B97")
        self.banner_label.pack(side="top", padx=10, pady=5)

        separator_below = ttk.Separator(banner_frame, orient="horizontal")
        separator_below.pack(side="bottom", fill="x", padx=5, pady=5)

    def get_next_teams_text(self):
        next_teams = self.draft_manager.next_teams_up_to_draft()
        return "Next up to draft: " + ", ".join(next_teams)

    def update_banner(self):
        self.banner_label.configure(text=self.get_next_teams_text())

    def draft_player(self):
        selected_item = self.tree.selection()[0]
        player_data = self.tree.item(selected_item)['values']
        self.tree.delete(selected_item)
        self.update_banner()
        return player_data

    def on_enter(self, event):
        player_data = self.draft_player()
        self.draft_manager.draft_player_data(player_data)
        self.team_sidebar.player_was_drafted()
