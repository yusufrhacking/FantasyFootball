class DraftingLogic:
    def __init__(self, draft_order):
        self.current_drafter_index = 0
        self.snake_direction = 1
        self.draft_order = draft_order

    def update_drafter_order(self):
        self.current_drafter_index += self.snake_direction
        if self.current_drafter_index >= len(self.draft_order) or self.current_drafter_index < 0:
            self.snake_direction *= -1
            self.current_drafter_index += self.snake_direction
