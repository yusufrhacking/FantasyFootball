import tkinter as tk
from tkinter import ttk

def display_players(frame, df):
    for index, row in df.iterrows():
        player = f"{row['Player']} ({row['Position']}): {row['Proj Pts']} Proj Pts"
        label = tk.Label(frame, text=player, wraplength=500)
        label.pack(side=tk.TOP, pady=2)

def create_scrollable_frame(parent, df):
    canvas = tk.Canvas(parent, bg='white')
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    scroll_frame = tk.Frame(canvas, bg='white')
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

    display_players(scroll_frame, df)

def create_gui(root, qb_df, other_positions_df):
    notebook = ttk.Notebook(root)
    notebook.pack(expand=1, fill=tk.BOTH)

    qb_frame = ttk.Frame(notebook)
    other_positions_frame = ttk.Frame(notebook)

    notebook.add(qb_frame, text="Quarterbacks")
    notebook.add(other_positions_frame, text="Other Positions (RB/TE/WR)")

    create_scrollable_frame(qb_frame, qb_df)
    create_scrollable_frame(other_positions_frame, other_positions_df)
