import tkinter as tk
from data_manager import get_players
from gui_manager import FantasyFootballApp


def main():
    qb_df, other_positions_df = get_players()
    root = tk.Tk()
    app = FantasyFootballApp(root, qb_df, other_positions_df)
    root.mainloop()

if __name__ == "__main__":
    main()
