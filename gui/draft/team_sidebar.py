import tkinter as tk
from tkinter import ttk

from gui.draft.player_display import PlayerDisplay


class TeamSidebar:
    def __init__(self, parent, draft_callback, config):
        self.position_requirements = config['position_requirements']
        self.draft_order = config['draft_order']
        self.all_teams_drafted_players = {team: [] for team in self.draft_order}
        self.current_drafter_index = 0
        self.snake_direction = 1
        self.current_round = 1
        self.current_overall_pick = 1

        self.init_ui(parent, draft_callback)

    def init_ui(self, parent, draft_callback):
        self.current_drafter_label = ttk.Label(parent, text=self.current_drafter_text(), font=("Helvetica", 16))
        self.current_drafter_label.pack(pady=10)

        self.draft_button = ttk.Button(parent, text="Draft Player", command=lambda: self.handle_draft(draft_callback))
        self.draft_button.pack(pady=10)

        self.team_combobox = ttk.Combobox(parent, values=self.draft_order, font=("Helvetica", 16))
        self.team_combobox.current(0)
        self.team_combobox.pack(pady=10)
        self.team_combobox.bind("<<ComboboxSelected>>", self.update_team_display)

        self.player_display = PlayerDisplay(parent, self.position_requirements)

    def update_team_display(self, event=None):
        selected_team = self.team_combobox.get()
        drafted_players = self.all_teams_drafted_players.get(selected_team, [])

        for _, label in self.player_display.player_labels:
            label.config(text="[ ]")

        for player_data in drafted_players:
            self.player_display.add_player_to_gui(player_data)

    def current_drafter_text(self):
        text = f"Round {self.current_round}, Pick #{self.current_drafter_index+1}\nOverall: #{self.current_overall_pick}\n"
        text += f"Up to draft: {self.draft_order[self.current_drafter_index]}"
        return text

    def handle_draft(self, draft_callback):
        drafted_player = draft_callback()
        current_team = self.draft_order[self.current_drafter_index]
        self.all_teams_drafted_players[current_team].append(drafted_player)

        self.update_drafter_order()
        self.current_drafter_label.config(text=self.current_drafter_text())
        self.team_combobox.current(self.current_drafter_index)
        self.update_team_display()

    def get_next_teams(self, num_teams):
        next_teams = []
        index = self.current_drafter_index
        for _ in range(num_teams):
            next_teams.append(self.draft_order[index])
            index += self.snake_direction
            if index >= len(self.draft_order) or index < 0:
                self.snake_direction *= -1
                index += self.snake_direction
        return next_teams

    def update_drafter_order(self):
        self.current_drafter_index += self.snake_direction
        self.current_overall_pick += 1
        if self.current_drafter_index >= len(self.draft_order) or self.current_drafter_index < 0:
            self.current_round += 1
            self.snake_direction *= -1
            self.current_drafter_index += self.snake_direction