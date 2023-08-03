class DraftManager:
    def __init__(self, config):
        self.position_requirements = config['position_requirements']
        self.teams_in_draft_order = config['draft_order']
        self.players_by_teams = {team: [] for team in self.teams_in_draft_order}

        self.current_drafter_index = 0
        self.snake_direction = 1
        self.current_round = 1
        self.current_overall_pick = 1

    def draft_player(self, draft_callback):
        drafted_player = draft_callback()
        current_team = self.teams_in_draft_order[self.current_drafter_index]
        self.players_by_teams[current_team].append(drafted_player)
        self.update_drafter_order()

    def update_drafter_order(self):
        self.current_drafter_index += self.snake_direction
        self.current_overall_pick += 1
        if self.current_drafter_index >= len(self.teams_in_draft_order) or self.current_drafter_index < 0:
            self.current_round += 1
            self.snake_direction *= -1
            self.current_drafter_index += self.snake_direction


    def get_players_from_team(self, selected_team):
        return self.players_by_teams.get(selected_team, [])

    def current_drafter_text(self):
        text = f"Round {self.current_round}, Pick #{self.current_drafter_index + 1}\nOverall: #{self.current_overall_pick}\n"
        text += f"Up to draft: {self.teams_in_draft_order[self.current_drafter_index]}"
        return text

    def next_teams_up_to_draft(self, count=16):
            next_teams = []
            current_index = self.current_drafter_index
            direction = self.snake_direction
            for _ in range(count):
                current_index += direction
                if current_index >= len(self.teams_in_draft_order) or current_index < 0:
                    direction *= -1
                    current_index += direction * 2
                next_teams.append(self.teams_in_draft_order[current_index])
            return next_teams
