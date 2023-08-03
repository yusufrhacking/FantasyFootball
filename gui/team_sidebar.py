import tkinter as tk
from tkinter import ttk


class TeamSidebar:
    def __init__(self, parent, draft_callback, config):
        self.drafted_players = {}
        self.position_requirements = config['position_requirements']

        self.init_ui(parent, draft_callback)

    def init_ui(self, parent, draft_callback):
        my_team_label = ttk.Label(parent, text="My Team", font=("Helvetica", 16))
        my_team_label.pack(pady=10)
        self.draft_button = ttk.Button(parent, text="Draft Player", command=draft_callback)
        self.draft_button.pack(pady=10)

        self.player_labels = []
        self.create_positions(parent, "BENCH")

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

    def add_player(self, player_data):
        player, position, par = player_data[1], player_data[2], player_data[3]
        target_pos = self.determine_target_position(position)
        self.update_player_label(target_pos, f'{player} ({position}) - {par} PAR')
        self.update_drafted_players(target_pos, player_data)

    def remove_player(self, player_data):
        player, position, par = player_data[1], player_data[2], player_data[3]
        target_text = f'{player} ({position}) - {par} PAR'
        target_pos = self.get_target_position_for_removal(target_text)
        self.update_player_label(target_pos, "[ ]")
        self.update_drafted_players(target_pos, player_data, add=False)

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

    def update_drafted_players(self, target_pos, player_data, add=True):
        if target_pos not in self.drafted_players:
            self.drafted_players[target_pos] = []

        if add:
            self.drafted_players[target_pos].append(player_data)
        else:
            self.drafted_players[target_pos].remove(player_data)

    def get_target_position_for_removal(self, target_text):
        for pos, label in self.player_labels:
            if label.cget('text') == target_text:
                return pos

