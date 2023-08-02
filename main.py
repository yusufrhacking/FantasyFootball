import tkinter as tk
from data_manager import get_players
from gui_manager import create_gui

def main():
    qb_df, other_positions_df = get_players()
    root = tk.Tk()
    root.title("Top Fantasy Players")
    root.geometry('800x600') # You can set the dimensions as per your requirement

    print("Main " + str(qb_df.columns))

    create_gui(root, qb_df, other_positions_df)

    root.mainloop()

if __name__ == "__main__":
    main()
