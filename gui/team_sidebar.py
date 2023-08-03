import tkinter as tk
from tkinter import ttk


class TeamSidebar:
    def __init__(self, parent, draft_callback, config):
        self.position_requirements = config['position_requirements']
        self.draft_order = config['draft_order']
        self.all_teams_drafted_players = {team: [] for team in self.draft_order}
        self.current_drafter_index = 0
        self.snake_direction = 1  # 1 for forward, -1 for reverse (snaking back)

        self.init_ui(parent, draft_callback)

    def init_ui(self, parent, draft_callback):
        self.current_drafter_label = ttk.Label(parent, text=self.current_drafter_text(), font=("Helvetica", 16))
        self.current_drafter_label.pack(pady=10)

        self.draft_button = ttk.Button(parent, text="Draft Player", command=lambda: self.handle_draft(draft_callback))
        self.draft_button.pack(pady=10)

        self.team_combobox = ttk.Combobox(parent, values=self.draft_order, font=("Helvetica", 16))
        self.team_combobox.current(0)  # Set default value to the first team in the list
        self.team_combobox.pack(pady=10)
        self.team_combobox.bind("<<ComboboxSelected>>", self.update_team_display)

        # my_team_label = ttk.Label(parent, text="My Team", font=("Helvetica", 16))
        # my_team_label.pack(pady=10)

        self.player_labels = []
        self.create_positions(parent, "BENCH")

    def update_team_display(self, event=None):
        selected_team = self.team_combobox.get()
        drafted_players = self.all_teams_drafted_players.get(selected_team, [])

        for _, label in self.player_labels:
            label.config(text="[ ]")

        for player_data in drafted_players:
            self.add_player_to_gui(player_data)

    def current_drafter_text(self):
        return f"Up to draft: {self.draft_order[self.current_drafter_index]}"

    def handle_draft(self, draft_callback):
        drafted_player = draft_callback()  # assuming draft_callback returns the drafted player data
        self.add_player_to_team(drafted_player)
        self.update_drafter_order()
        self.current_drafter_label.config(text=self.current_drafter_text())

        self.team_combobox.current(self.current_drafter_index)

        self.update_team_display()

    def add_player_to_team(self, player_data):
        current_team = self.draft_order[self.current_drafter_index]
        self.all_teams_drafted_players[current_team].append(player_data)

        # If the current team is "ME", update the GUI
        if current_team == "ME":
            self.add_player_to_gui(player_data)

    def add_player_to_gui(self, player_data):
        player, position, par = player_data[1], player_data[2], player_data[3]
        target_pos = self.determine_target_position(position)
        self.update_player_label(target_pos, f'{player} ({position}) - {par} PAR')

    def update_drafter_order(self):
        self.current_drafter_index += self.snake_direction
        if self.current_drafter_index >= len(self.draft_order) or self.current_drafter_index < 0:
            self.snake_direction *= -1
            self.current_drafter_index += self.snake_direction

    def create_positions(self, parent, exclude_position):
        for position, count in self.position_requirements.items():
            if position != exclude_position:
                for _ in range(count):
                    self.create_position_row(parent, position)

        # Adding Bench at the end
        for _ in range(self.position_requirements.get(exclude_position, 0)):
            self.create_position_row(parent, exclude_position)

    def create_position_row(self, parent, position):
        frame = tk.Frame(parent)
        frame.pack(pady=2)
        label = ttk.Label(frame, text=f'{position}:', font=("Helvetica", 12))
        label.pack(side=tk.LEFT)
        player_label = ttk.Label(frame, text="[ ]", width=40)
        player_label.pack(side=tk.LEFT)
        self.player_labels.append((position, player_label))

    def determine_target_position(self, position):
        for target_pos in [position, 'FLEX', 'BENCH']:
            if target_pos in ['WR', 'RB', 'TE'] and position == target_pos:
                target_pos = 'FLEX'

            if self.is_position_available(target_pos):
                return target_pos

    def is_position_available(self, target_pos):
        for pos, label in self.player_labels:
            if pos == target_pos and label.cget('text') == "[ ]":
                return True
        return False

    def update_player_label(self, target_pos, text):
        for pos, label in self.player_labels:
            if pos == target_pos and label.cget('text') == "[ ]":
                label.config(text=text)
                break

    def get_target_position_for_removal(self, target_text):
        for pos, label in self.player_labels:
            if label.cget('text') == target_text:
                return pos

