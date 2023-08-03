import tkinter as tk

from fantasy_canon import FantasyCanonApp

def main():
    root = tk.Tk()
    app = FantasyCanonApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()