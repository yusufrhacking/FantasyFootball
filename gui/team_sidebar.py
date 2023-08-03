import tkinter as tk
from tkinter import ttk


class TeamSidebar:
    def __init__(self, parent, draft_callback, position_requirements):
        self.drafted_players = []
        self.position_requirements = position_requirements
        self.position_labels = {}
        self.draft_button = ttk.Button(parent, text="Draft Player", command=draft_callback)
        self.draft_button.pack(pady=10)

        for position, count in self.position_requirements.items():
            label = ttk.Label(parent, text=f'{position}: 0/{count}', font=("Helvetica", 12))
            label.pack(pady=2)
            self.position_labels[position] = label

        self.drafted_tree = ttk.Treeview(parent, columns=('Player', 'Position', 'PAR'), show='headings')
        self.drafted_tree.heading('Player', text='Player')
        self.drafted_tree.heading('Position', text='Position')
        self.drafted_tree.heading('PAR', text='PAR')
        self.drafted_tree.pack(pady=10)

    def add_player(self, player_data):
        player, position, par = player_data[1], player_data[2], player_data[3]
        self.drafted_players.append(player_data)
        self.drafted_tree.insert('', tk.END, values=(player, position, par))
        self.update_position_count(position, 1)

    def remove_player(self, selected_index):
        player_data = self.drafted_players[selected_index]
        position = player_data[1]
        del self.drafted_players[selected_index]
        self.drafted_tree.delete(self.drafted_tree.get_children()[selected_index])
        self.update_position_count(position, -1)

    def update_position_count(self, position, change):
        if position in ['WR', 'RB', 'TE']:
            position = 'FLEX'
        current_count = int(self.position_labels[position].cget('text').split(':')[1].split('/')[0])
        new_count = current_count + change
        self.position_labels[position].config(text=f'{position}: {new_count}/{self.position_requirements[position]}')

    def get_selected_index(self):
        return self.drafted_tree.selection()[0]

