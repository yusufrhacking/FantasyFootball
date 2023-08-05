from tkinter import ttk


class DraftTitle:
    def __init__(self, root, title_text):
        self.create_top_frame(root, title_text)

    def create_top_frame(self, root, title_text):
        top_frame = ttk.Frame(root, padding="10")
        top_frame.pack(side="top", fill="both", expand=False)
        self.add_title(top_frame, title_text)

    def add_title(self, frame, title_text):
        title_label = ttk.Label(frame, text=title_text, font=("Helvetica", 24), foreground="#333333")
        title_label.pack(side="top", padx=5)