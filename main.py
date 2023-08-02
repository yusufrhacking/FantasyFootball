import tkinter as tk
from data_manager import get_players
from gui_manager import create_scrollable_frame

def main():
    qb_df, other_positions_df = get_players()
    root = tk.Tk()
    root.title("Top Players")
    # create_scrollable_frame(root, qb_df)
    # create_scrollable_frame(root, other_positions_df)
    root.mainloop()

if __name__ == "__main__":
    main()
