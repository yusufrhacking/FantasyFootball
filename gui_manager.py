import tkinter as tk
from tkinter import ttk
import pandas as pd

class ScrollableFrame:
    def __init__(self, parent, df, position_title):
        container = ttk.Frame(parent)
        container.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        header_label = ttk.Label(container, text=position_title, font=('Helvetica', 16, 'bold'))
        header_label.pack(side=tk.TOP, pady=10, padx=20)

        self.canvas = tk.Canvas(container, highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.scroll_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")

        # Create table header
        header_frame = ttk.Frame(self.scroll_frame)
        header_frame.pack(side=tk.TOP, fill=tk.X)

        ttk.Label(header_frame, text="Player", width=25, font=('Helvetica', 12, 'bold')).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Label(header_frame, text="Position", font=('Helvetica', 12, 'bold')).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Label(header_frame, text="Proj Pts", font=('Helvetica', 12, 'bold')).pack(side=tk.LEFT, padx=5, pady=5)

        # Add players
        self.rows = []
        for index, row in df.iterrows():
            row_frame = ttk.Frame(self.scroll_frame)
            row_frame.pack(side=tk.TOP, fill=tk.X)

            ttk.Label(row_frame, text=row['Player'], width=25).pack(side=tk.LEFT, padx=5, pady=2)
            ttk.Label(row_frame, text=row['Position']).pack(side=tk.LEFT, padx=5, pady=2)
            ttk.Label(row_frame, text=row['Proj Pts']).pack(side=tk.LEFT, padx=5, pady=2)

            self.rows.append(row_frame)

    def update_scrollregion(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


def create_gui(root, qb_df, other_positions_df):
    root.title("Fantasy Football Projections")
    root.geometry("800x600")
    root.configure(bg='lightgray')

    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure("TFrame", background="lightgray")  # Set background color for ttk.Frame widgets

    notebook = ttk.Notebook(root)
    notebook.pack(expand=1, fill=tk.BOTH, padx=20, pady=20)

    qb_frame = ttk.Frame(notebook)
    other_positions_frame = ttk.Frame(notebook)

    notebook.add(qb_frame, text="Quarterbacks")
    notebook.add(other_positions_frame, text="Other Positions (RB/TE/WR)")

    qb_scrollable_frame = ScrollableFrame(qb_frame, qb_df, "Quarterbacks")
    other_positions_scrollable_frame = ScrollableFrame(other_positions_frame, other_positions_df, "Other Positions")

    qb_scrollable_frame.canvas.bind('<Configure>', qb_scrollable_frame.update_scrollregion)
    other_positions_scrollable_frame.canvas.bind('<Configure>', other_positions_scrollable_frame.update_scrollregion)


# Example usage
# qb_df = pd.DataFrame(...)
# other_positions_df = pd.DataFrame(...)
# root = tk.Tk()
# create_gui(root, qb_df, other_positions_df)
# root.mainloop()
