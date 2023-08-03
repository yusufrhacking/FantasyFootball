import tkinter as tk
from tkinter import ttk


class TeamSidebar:
    def __init__(self, parent, draft_callback, config):
        self.position_requirements = config['position_requirements']
        self.draft_order = config['draft_order']
        self.all_teams_drafted_players = {team: [] for team in self.draft_order}
        self.current_drafter_index = 0
        self.snake_direction = 1  # 1 for forward, -1 for reverse (snaking back)

        self.init_UI(parent, draft_callback)

    def init_UI(self, parent, draft_callback):
        self.current_drafter_label = ttk.Label(parent, text=self.current_drafter_text(), font=("Helvetica", 16))
        self.current_drafter_label.pack(pady=10)

        my_team_label = ttk.Label(parent, text="My Team", font=("Helvetica", 16))
        my_team_label.pack(pady=10)

        self.draft_button = ttk.Button(parent, text="Draft Player", command=lambda: self.handle_draft(draft_callback))
        self.draft_button.pack(pady=10)

        self.player_labels = []
        self.create_positions(parent, "BENCH")

    def current_drafter_text(self):
        return f"Up to draft: {self.draft_order[self.current_drafter_index]}"

    def handle_draft(self, draft_callback):
        drafted_player = draft_callback()  # assuming draft_callback returns the drafted player data
        self.add_player_to_team(drafted_player)
        self.update_drafter_order()
        self.current_drafter_label.config(text=self.current_drafter_text())

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
        # self.update_drafted_players(target_pos, player_data)

    def update_drafter_order(self):
        self.current_drafter_index += self.snake_direction
        if self.current_drafter_index >= len(self.draft_order) or self.current_drafter_index < 0:
            self.snake_direction *= -1
            self.current_drafter_index += self.snake_direction * 2

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

    # def update_drafted_players(self, target_pos, player_data, add=True):
    #     if target_pos not in self.drafted_players:
    #         self.drafted_players[target_pos] = []
    #
    #     if add:
    #         self.drafted_players[target_pos].append(player_data)
    #     else:
    #         self.drafted_players[target_pos].remove(player_data)

    def get_target_position_for_removal(self, target_text):
        for pos, label in self.player_labels:
            if label.cget('text') == target_text:
                return pos

