import tkinter as tk
from tkinter import ttk


class DataFrameView:
    def __init__(self, container, df, title="", on_enter=None, shade_rows=False):
        self.container = ttk.Frame(container)
        self.container.grid(row=0, column=0, sticky="nsew")

        self.df = df

        self.on_enter = on_enter
        self.shade_rows = shade_rows

        self._add_header(title)
        self._create_tree_view(df)
        self._populate_tree_view(df)

        self.sorting_column = None  # Keep track of the column currently being sorted
        self.sorting_order = False  # Keep track of the sorting order (True for ascending, False for descending)

    def _add_header(self, title):
        header_label = ttk.Label(self.container, text=title, font=('Helvetica', 16, 'bold'))
        header_label.pack(side=tk.TOP, pady=10, padx=20)

    def _create_tree_view(self, df):
        columns = tuple(df.columns)
        self.tree = ttk.Treeview(self.container, columns=columns, show="headings")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self._sort_tree(c))
            self.tree.column(col, width=100)

        if self.on_enter:
            self.tree.bind('<Return>', self.on_enter)

        scrollbar = ttk.Scrollbar(self.container, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)

    def _populate_tree_view(self, df):
        for index, row in df.iterrows():
            if self.shade_rows:
                tag, color_shade = self.get_color_tag(index, row)
                self.tree.tag_configure(tag, background=color_shade)

                self.tree.insert("", index, values=list(row), tags=(tag,))
            else:
                self.tree.insert("", tk.END, values=tuple(row))

    def _sort_tree(self, col):
        if col == self.sorting_column:
            self.sorting_order = not self.sorting_order
        else:
            self.sorting_order = True

        self.df.sort_values(by=col, ascending=self.sorting_order, inplace=True)
        self.df.reset_index(drop=True, inplace=True)
        self.tree.delete(*self.tree.get_children())
        self._populate_tree_view(self.df)
        self.sorting_column = col

    def update_on_query(self, query, new_df_to_show):
        self.df = new_df_to_show
        self.tree.delete(*self.tree.get_children())

        first_child = None

        for row in self.df.itertuples():
            if query in str(row).lower():
                child_id = self.tree.insert("", "end", values=row[1:])
                if first_child is None:
                    first_child = child_id

        if first_child:
            self.tree.selection_set(first_child)

    def pop_selected_player_data(self):
        selected_item = self.tree.selection()[0]
        player_data = self.tree.item(selected_item)['values']
        self.tree.delete(selected_item)
        return player_data

    def get_color_tag(self, index, row):
        added_par_value = row['Added_PAR_Value']
        color_shade = self.get_color_shade(added_par_value)

        tag = 'color' + str(index)
        return tag, color_shade

    def get_color_shade(self, value):
        normalized_value = max(-1.0, min(1.0, value / 50.0))  # Clamping the value between -1 and 1

        if normalized_value > 0:
            # For negative values, linear interpolation between red and white
            red = 255
            green = int(255 * (1 - normalized_value))
        else:
            # For positive values, linear interpolation between white and green
            red = int(255 * (normalized_value + 1))
            green = 255

        # Create the color in RGB format

        color = (red, green, 255)  # Red and green values, with blue set to 0

        color_hash = f'#{color[0]:02x}{color[1]:02x}{color[2]:02x}'
        return color_hash