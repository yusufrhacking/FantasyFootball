import tkinter as tk
from data_manager import get_players
import sys
print(sys.version)
print("TK Version: " + str(tk.TclVersion))
from gui_manager import create_scrollable_frame

def main():
    qb_df, other_positions_df = get_players()
    root = tk.Tk()
    root.title("Top Players")

    message = tk.Label(root, text="Hello, World!")
    message.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
