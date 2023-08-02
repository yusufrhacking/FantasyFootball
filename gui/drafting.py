# import tkinter as tk
# from tkinter import ttk
#
#
# class DraftingView:
#     def __init__(self, container, players, on_draft_callback):
#         self.container = ttk.Frame(container)
#         self.container.grid(row=0, column=1, sticky="nsew")
#         self.on_draft_callback = on_draft_callback
#
#         self.listbox = tk.Listbox(self.container)
#         self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
#
#         for player in players:
#             self.listbox.insert(tk.END, player)
#
#         draft_button = ttk.Button(self.container, text="Draft", command=self.draft_player)
#         draft_button.pack(side=tk.LEFT, padx=5, pady=5)
#
#     def draft_player(self):
#         selected_index = self.listbox.curselection()
#         if selected_index:
#             player = self.listbox.get(selected_index)
#             self.listbox.delete(selected_index)
#             self.on_draft_callback(player)
#
#
# class DraftingController:
#     def __init__(self, root, players, on_draft_callback):
#         self.drafting_view = DraftingView(root, players, on_draft_callback)
