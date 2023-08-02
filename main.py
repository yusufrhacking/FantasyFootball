import tkinter as tk

from data_processing.database_manager import get_players_data
from gui.app import FantasyFootballApp


def main():
    # Get the data from the database manager, writing if the database is empty
    players_data = get_players_data()

    root = tk.Tk()
    dfs = [(df, position) for position, df in players_data.items()]

    app = FantasyFootballApp(root, dfs)
    root.mainloop()

if __name__ == "__main__":
    main()
