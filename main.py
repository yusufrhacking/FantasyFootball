import tkinter as tk
import pandas as pd
from data_manager import get_players
from gui_manager import FantasyFootballApp


def main():
    players_dfs = get_players()
    root = tk.Tk()

    positions = ["QB", "RB", "WR", "TE", "FLEX"]
    dfs = []

    for position in positions:
        dfs.append((players_dfs[position], position))

    app = FantasyFootballApp(root, dfs)
    root.mainloop()

if __name__ == "__main__":
    main()
