import tkinter as tk
from tkinter import ttk


class ButtonController:
    def __init__(self, root, frame_controller, button_texts):
        button_frame = ttk.Frame(root)
        button_frame.pack(side=tk.TOP, fill=tk.X)
        for text in button_texts:
            button = ttk.Button(button_frame, text=text, command=lambda f=frame_controller.frames[text]: f.tkraise())
            button.pack(side=tk.LEFT, padx=5, pady=5)
