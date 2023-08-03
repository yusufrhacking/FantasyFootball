import tkinter as tk
from tkinter import ttk


class TeamSidebar:
    def __init__(self, parent, draft_callback, position_requirements):
        self.drafted_players = {}
        self.position_requirements = position_requirements
        self.draft_button = ttk.Button(parent, text="Draft Player", command=draft_callback)
        self.draft_button.pack(pady=10)

        self.position_frames = {}
        self.player_labels = []

        for position, count in self.position_requirements.items():
            for _ in range(count):
                frame = tk.Frame(parent)
                frame.pack(pady=2)
                label = ttk.Label(frame, text=f'{position}:', font=("Helvetica", 12))
                label.pack(side=tk.LEFT)
                player_label = ttk.Label(frame, text="[ ]", width=40)
                player_label.pack(side=tk.LEFT)
                self.position_frames[position] = frame
                self.player_labels.append((position, player_label))

    def add_player(self, player_data):
        player, position, par = player_data[1], player_data[2], player_data[3]
        if position in ['WR', 'RB', 'TE']:
            position = 'FLEX'

        for pos, label in self.player_labels:
            if pos == position and label.cget('text') == "[ ]":
                label.config(text=f'{player} ({position}) - {par} PAR')
                break

        if position not in self.drafted_players:
            self.drafted_players[position] = []
        self.drafted_players[position].append(player_data)

    def remove_player(self, player_data):
        player, position, par = player_data[1], player_data[2], player_data[3]
        if position in ['WR', 'RB', 'TE']:
            position = 'FLEX'

        for pos, label in self.player_labels:
            if pos == position and label.cget('text') == f'{player} ({position}) - {par} PAR':
                label.config(text="[ ]")
                break

        self.drafted_players[position].remove(player_data)



