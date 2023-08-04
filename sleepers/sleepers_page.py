from tkinter import ttk
import tkinter as tk

from data_analysis.sleepers_processor import get_sleepers
from gui.player_view_controller import PlayerController


class SleepersPageApp:
    def __init__(self, root, par_table, config):
        self.bottom_frame = None
        self.data_table = get_sleepers(par_table, config)
        # self.par_table = par_table
        root.title("Sleepers Page")
        root.geometry("1200x800")
        root.configure(bg='#f0f0f0')  # Soft Gray Background

        style = ttk.Style(root)
        style.theme_use("clam")
        style.configure("TFrame", background="lightgray")

        self.create_top_frame(root)
        player_df_view = PlayerController(root, self.data_table)

    def create_top_frame(self, root):
        top_frame = ttk.Frame(root, padding="10")
        top_frame.pack(side="top", fill="both", expand=False)
        self.add_title(top_frame)

    def add_title(self, frame):
        title_label = ttk.Label(frame, text="Sleepers", font=("Helvetica", 24), foreground="#333333")
        title_label.pack(side="top", padx=5)