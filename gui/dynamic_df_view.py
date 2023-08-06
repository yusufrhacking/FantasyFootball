from gui.df_view import DataFrameView


class DynamicDfView(DataFrameView):
    def __init__(self, container, df, title="", shade_rows=False, on_enter=None):
        super().__init__(container, df, shade_rows=shade_rows, on_enter=on_enter)

