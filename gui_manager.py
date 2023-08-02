import tkinter as tk


def display_players(frame, df):
    for index, row in df.iterrows():
        player = f"Player: {row['Player']}, Position: {row['Position']}, Proj Pts: {row['Proj Pts']}"
        label = tk.Label(frame, text=player, wraplength=500)
        label.pack()


def create_scrollable_frame(root, df):
    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=1)
    canvas = tk.Canvas(frame)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
    scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    scroll_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    display_players(scroll_frame, df)
