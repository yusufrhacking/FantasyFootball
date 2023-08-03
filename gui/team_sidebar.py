import tkinter as tk
from tkinter import ttk

class TeamSidebar:
    def __init__(self, parent, draft_callback):
        self.drafted_players = []

        self.drafted_label = ttk.Label(parent, text="My Team", font=("Helvetica", 16))
        self.drafted_label.pack(pady=10)

        self.draft_button = ttk.Button(parent, text="Draft Player", command=draft_callback)
        self.draft_button.pack(pady=10)

        self.drafted_list = tk.Listbox(parent, selectmode="single", height=10, width=50)
        self.drafted_list.pack(pady=10)

    def add_player(self, player_data):
        player, position, par = player_data[0], player_data[1], player_data[2]  # Adjust based on your data structure
        self.drafted_players.append(player_data)
        self.drafted_list.insert(tk.END, f'{player} ({position}) - {par} PAR')

    def remove_player(self, selected_index):
        del self.drafted_players[selected_index]
        self.drafted_list.delete(selected_index)

    def get_selected_index(self):
        return self.drafted_list.curselection()[0]
