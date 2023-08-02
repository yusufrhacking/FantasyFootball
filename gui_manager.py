import tkinter as tk
from tkinter import ttk

def create_scrollable_frame(container, df, position_title):
    header_label = ttk.Label(container, text=position_title, font=('Helvetica', 16, 'bold'))
    header_label.pack(side=tk.TOP, pady=10, padx=20)

    canvas = tk.Canvas(container, highlightthickness=0)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    scroll_frame = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

    # Create table header
    header_frame = ttk.Frame(scroll_frame)
    header_frame.pack(side=tk.TOP, fill=tk.X)

    ttk.Label(header_frame, text="Player", width=25, font=('Helvetica', 12, 'bold')).pack(side=tk.LEFT, padx=5, pady=5)
    ttk.Label(header_frame, text="Position", font=('Helvetica', 12, 'bold')).pack(side=tk.LEFT, padx=5, pady=5)
    ttk.Label(header_frame, text="Proj Pts", font=('Helvetica', 12, 'bold')).pack(side=tk.LEFT, padx=5, pady=5)

    # Add players
    for index, row in df.iterrows():
        row_frame = ttk.Frame(scroll_frame)
        row_frame.pack(side=tk.TOP, fill=tk.X)

        ttk.Label(row_frame, text=row['Player'], width=25).pack(side=tk.LEFT, padx=5, pady=2)
        ttk.Label(row_frame, text=row['Position']).pack(side=tk.LEFT, padx=5, pady=2)
        ttk.Label(row_frame, text=row['Proj Pts']).pack(side=tk.LEFT, padx=5, pady=2)

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

    create_scrollable_frame(qb_frame, qb_df, "Quarterbacks")
    create_scrollable_frame(other_positions_frame, other_positions_df, "Other Positions")
