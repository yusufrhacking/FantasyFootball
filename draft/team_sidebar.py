from tkinter import ttk

from draft.player_display import PlayerDisplay

class TeamSidebar:
    def __init__(self, parent, draft_callback, draft_manager):
        self.draft_manager = draft_manager

        self.init_ui(parent, draft_callback)

    def init_ui(self, parent, draft_callback):
        self.current_drafter_label = ttk.Label(parent, text=self.draft_manager.current_drafter_text(), font=("Helvetica", 16))
        self.current_drafter_label.pack(pady=10)

        self.draft_button = ttk.Button(parent, text="Draft Player", command=lambda: self.handle_draft(draft_callback))
        self.draft_button.pack(pady=10)

        self.team_combobox = ttk.Combobox(parent, values=self.draft_manager.teams_in_draft_order, font=("Helvetica", 16))
        self.team_combobox.current(0)
        self.team_combobox.pack(pady=10)
        self.team_combobox.bind("<<ComboboxSelected>>", self.update_team_display)

        self.player_display = PlayerDisplay(parent, self.draft_manager.position_requirements)

    def update_team_display(self, event=None):
        selected_team = self.team_combobox.get()
        drafted_players = self.draft_manager.get_players_from_team(selected_team)

        for _, label in self.player_display.player_labels:
            label.config(text="[ ]")

        for player_data in drafted_players:
            self.player_display.add_player_to_gui(player_data)

    def handle_draft(self, draft_callback):
        self.draft_manager.draft_player(draft_callback)
        self.current_drafter_label.config(text=self.draft_manager.current_drafter_text())
        self.team_combobox.current(self.draft_manager.current_drafter_index)
        self.update_team_display()