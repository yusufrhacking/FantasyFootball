from gui.multi_tab_view import DataFrameView


class FrameController:
    def __init__(self, container, df_title_pairs):
        self.frames = {}
        for df, title in df_title_pairs:
            frame = DataFrameView(container, df, title)
            self.frames[title] = frame.container
