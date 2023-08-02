import tkinter as tk
from tkinter import ttk


class DataFrameView:
    def __init__(self, parent, df, position_title):
        container = ttk.Frame(parent)
        container.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        header_label = ttk.Label(container, text=position_title, font=('Helvetica', 16, 'bold'))
        header_label.pack(side=tk.TOP, pady=10, padx=20)

        columns = tuple(df.columns)
        self.tree = ttk.Treeview(container, columns=columns, show="headings")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.configure(yscrollcommand=scrollbar.set)

        # Add data
        for index, row in df.iterrows():
            self.tree.insert("", tk.END, values=tuple(row))


def create_gui(root, qb_df, other_positions_df):
    root.title("Fantasy Football Projections")
    root.geometry("800x600")
    root.configure(bg='lightgray')

    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure("TFrame", background="lightgray")  # Set background color for ttk.Frame widgets

    def show_frame(frame_to_show):
        frame_to_show.tkraise()

    container = ttk.Frame(root)
    container.pack(side="top", fill="both", expand=True)
    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)

    qb_frame = ttk.Frame(container)
    other_positions_frame = ttk.Frame(container)

    for frame in (qb_frame, other_positions_frame):
        frame.grid(row=0, column=0, sticky="nsew")

    DataFrameView(qb_frame, qb_df, "Quarterbacks")
    DataFrameView(other_positions_frame, other_positions_df, "Other Positions")

    button_frame = ttk.Frame(root)
    button_frame.pack(side=tk.TOP, fill=tk.X)

    qb_button = ttk.Button(button_frame, text="Quarterbacks", command=lambda: show_frame(qb_frame))
    qb_button.pack(side=tk.LEFT, padx=5, pady=5)

    other_positions_button = ttk.Button(button_frame, text="Other Positions (RB/TE/WR)",
                                        command=lambda: show_frame(other_positions_frame))
    other_positions_button.pack(side=tk.LEFT, padx=5, pady=5)

    # Initially show the Quarterbacks frame
    show_frame(qb_frame)
