from data_analysis.sleepers_processor import get_sleepers
import pandas as pd


class DraftManager:
    def __init__(self, par_table, config):
        self.config = config
        self.par_table = par_table
        self.draftable_players = par_table.copy()
        self.add_added_par_value_column()

        self.position_requirements = config['position_requirements']
        self.teams_in_draft_order = config['draft_order']
        self.num_of_teams = len(self.teams_in_draft_order)
        self.players_by_teams = {team: [] for team in self.teams_in_draft_order}

        self.current_drafter_index = 0
        self.snake_direction = 1
        self.current_round = 1
        self.current_overall_pick = 1

    def add_added_par_value_column(self):
        sleepers_df = get_sleepers(self.par_table, self.config)

        sleepers_with_added_par_value = sleepers_df[['Player', 'Added_PAR_Value']]

        self.draftable_players = pd.merge(
            self.draftable_players,
            sleepers_with_added_par_value,
            on='Player',
            how='left'
        )

        self.draftable_players['Added_PAR_Value'] = self.draftable_players['Added_PAR_Value'].fillna(0)

    def add_color_column(self):
        self.par_table['color'] = self.par_table.apply(self.calculate_color, axis=1)

    def calculate_color(self, row):
        # Here, define your logic for determining the color based on the row
        value = row['some_column']
        if value > 10:
            return 'green'
        else:
            return 'red'

    def get_draftable_players(self):
        return self.draftable_players

    def draft_player_data(self, player):
        current_team = self.teams_in_draft_order[self.current_drafter_index]
        self.players_by_teams[current_team].append(player)
        self.update_drafter_order()

        player_name = player[1]
        self.draftable_players = self.draftable_players[self.draftable_players['Player'] != player_name]

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

    def next_teams_up_to_draft(self):
        next_teams = []
        current_index = self.current_drafter_index
        direction = self.snake_direction
        for _ in range(self.num_of_teams):
            current_index += direction
            if current_index >= len(self.teams_in_draft_order) or current_index < 0:
                direction *= -1
                current_index += direction
            next_teams.append(self.teams_in_draft_order[current_index])
        return next_teams
