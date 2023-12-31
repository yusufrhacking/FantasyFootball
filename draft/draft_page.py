import tkinter
from tkinter import ttk

from draft.banner import Banner
from draft.draft_manager import DraftManager
from draft.draft_title import DraftTitle
from draft.team_sidebar import TeamSidebar
from gui.df_view import DataFrameView

title = "Fantasy Draft Page"


class DraftPageApp:
    def __init__(self, root, par_table, config):
        self.establish_root(root)
        self.draft_manager = DraftManager(par_table, config)
        self.banner = Banner(root, self.get_next_teams_text())

        self.title = DraftTitle(root, title)
        self.create_bottom_frame(root)

        side_frame = ttk.Frame(self.bottom_frame, padding="20")
        side_frame.grid(row=0, column=1, sticky="nsew")

        self.team_sidebar = TeamSidebar(side_frame, self.draft_player, self.draft_manager)

    def establish_root(self, root):
        root.title(title)
        root.geometry("1200x800")
        root.configure(bg='#f0f0f0')  # Soft Gray Background
        style = ttk.Style(root)
        style.theme_use("clam")
        style.configure("TFrame", background="lightgray")

    def create_bottom_frame(self, root):
        self.search_bar = ttk.Entry(root)
        self.search_bar.pack()

        self.bottom_frame = ttk.Frame(root, padding="10")
        self.bottom_frame.pack(side="top", fill="both", expand=True)
        self.player_view = DataFrameView(self.bottom_frame, self.draft_manager.draftable_players,
                                         on_enter=self.on_enter_draft, shade_rows=True)

        self.bottom_frame.grid_columnconfigure(0, weight=3)
        self.bottom_frame.grid_columnconfigure(1, weight=1)
        self.bottom_frame.grid_rowconfigure(0, weight=1)

        self.search_bar.bind('<KeyRelease>', self.update_tree_on_search)

    def update_tree_on_search(self, event):
        if event.keysym == 'Return':
            self.on_enter_draft(event)
            self.search_bar.delete(0, 'end')
            self.player_view.reset_tree(self.draft_manager.draftable_players)
            return

        query = self.search_bar.get().lower()
        self.player_view.update_on_query(query, self.draft_manager.draftable_players)

    def add_scrollbar(self, tree, root):
        scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        tree.configure(yscrollcommand=scrollbar.set)

    def get_next_teams_text(self):
        next_teams = self.draft_manager.next_teams_up_to_draft()
        return "Next up to draft: " + ", ".join(next_teams)

    def on_enter_draft(self, event):
        player_data = self.draft_player()
        self.draft_manager.draft_player_data(player_data)
        self.team_sidebar.player_was_drafted()
        self.player_view.df = self.draft_manager.draftable_players


    def draft_player(self):
        player_data = self.player_view.pop_selected_player_data()
        self.banner.update_banner(self.get_next_teams_text())
        return player_data
