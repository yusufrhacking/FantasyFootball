import tkinter as tk
from tkinter import ttk

from gui.button_controller import ButtonController
# from gui.drafting import DraftingController
from gui.frame_controller import FrameController


class PositionalRankingsApp:
    def __init__(self, root, data_frames):
        root.title("Fantasy Football Projections")
        root.geometry("1200x800")
        root.configure(bg='lightgray')

        style = ttk.Style(root)
        style.theme_use("clam")
        style.configure("TFrame", background="lightgray")  # Set background color for ttk.Frame widgets

        container = ttk.Frame(root)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Unpack the list of data frames and titles using zip
        dfs, titles = zip(*data_frames)
        frame_controller = FrameController(container, zip(dfs, titles))
        button_controller = ButtonController(root, frame_controller, titles)
        # Initially show the first frame in the list
        frame_controller.frames[titles[0]].tkraise()
