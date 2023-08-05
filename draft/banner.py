import tkinter
from tkinter import ttk


class Banner:
    def __init__(self, root, banner_text):
        banner_frame = tkinter.Frame(root, bg="#468B97", padx=10, pady=10)
        banner_frame.pack(side="top", fill="both", expand=False)

        separator_above = ttk.Separator(banner_frame, orient="horizontal")
        separator_above.pack(side="top", fill="x", padx=5, pady=5)

        self.banner_label = ttk.Label(banner_frame, text=banner_text,
                                      font=("Helvetica", 16, "bold"), foreground="#f0f0f0",
                                      background="#468B97")
        self.banner_label.pack(side="top", padx=10, pady=5)

        separator_below = ttk.Separator(banner_frame, orient="horizontal")
        separator_below.pack(side="bottom", fill="x", padx=5, pady=5)

    def update_banner(self, banner_text):
        self.banner_label.configure(text=self.banner_text)