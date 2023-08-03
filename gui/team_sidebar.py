import tkinter as tk
from tkinter import ttk


class TeamSidebar:
    def __init__(self, parent, draft_callback, position_requirements):
        self.drafted_players = {}
        self.position_requirements = position_requirements
        self.draft_button = ttk.Button(parent, text="Draft Player", command=draft_callback)
        self.draft_button.pack(pady=10)

        self.player_labels = []

        for position, count in self.position_requirements.items():
            if position != "BENCH":
                for _ in range(count):
                    frame = tk.Frame(parent)
                    frame.pack(pady=2)
                    label = ttk.Label(frame, text=f'{position}:', font=("Helvetica", 12))
                    label.pack(side=tk.LEFT)
                    player_label = ttk.Label(frame, text="[ ]", width=40)
                    player_label.pack(side=tk.LEFT)
                    self.player_labels.append((position, player_label))

        # Adding Bench at the end
        for _ in range(self.position_requirements.get("BENCH", 0)):
            frame = tk.Frame(parent)
            frame.pack(pady=2)
            label = ttk.Label(frame, text="BENCH:", font=("Helvetica", 12))
            label.pack(side=tk.LEFT)
            player_label = ttk.Label(frame, text="[ ]", width=40)
            player_label.pack(side=tk.LEFT)
            self.player_labels.append(("BENCH", player_label))

    def add_player(self, player_data):
        player, position, par = player_data[1], player_data[2], player_data[3]

        # Try to add to specific position first, then FLEX, then BENCH
        for target_pos in [position, 'FLEX', 'BENCH']:
            if target_pos in ['WR', 'RB', 'TE'] and position == target_pos:
                target_pos = 'FLEX'

            for pos, label in self.player_labels:
                if pos == target_pos and label.cget('text') == "[ ]":
                    label.config(text=f'{player} ({position}) - {par} PAR')
                    if target_pos not in self.drafted_players:
                        self.drafted_players[target_pos] = []
                    self.drafted_players[target_pos].append(player_data)
                    return

    def remove_player(self, player_data):
        player, position, par = player_data[1], player_data[2], player_data[3]
        for pos, label in self.player_labels:
            if label.cget('text') == f'{player} ({position}) - {par} PAR':
                label.config(text="[ ]")
                self.drafted_players[pos].remove(player_data)
                break



