class RankingsProcessor:
    def __init__(self, overall_rankings, position_requirements, number_of_teams):
        self.overall_rankings = overall_rankings
        self.position_requirements = position_requirements
        self.number_of_teams = number_of_teams
        self.replacement_player_multiplier = 1.5

    def calculate_players_used_at_positions(self):
        players_used_at_position = {}
        for position, requirement in self.position_requirements.items():
            players_used_at_position[position] = int(
                requirement * self.number_of_teams * self.replacement_player_multiplier)
        return players_used_at_position

    def find_positional_replacement_level_players(self):
        players_used_at_position = self.calculate_players_used_at_positions()

        replacement_players = {}
        for position, number_of_players in players_used_at_position.items():
            players_in_position = self.overall_rankings[self.overall_rankings['Position'].isin(position.split('/'))]
            if len(players_in_position) > number_of_players:
                replacement_players[position] = players_in_position.iloc[number_of_players]
            else:
                replacement_players[position] = None

        return replacement_players

    def calculate_par_table(self):
        # Calculate the replacement level points for each position
        replacement_level_points = {}
        for position, player in self.find_positional_replacement_level_players().items():
            replacement_level_points[position] = player['Avg Proj Pts'] if player is not None else 0

        # Special handling for FLEX: use the same replacement level points for RB, WR, and TE
        flex_replacement_level = replacement_level_points['RB/WR/TE']
        replacement_level_points['RB'] = flex_replacement_level
        replacement_level_points['WR'] = flex_replacement_level
        replacement_level_points['TE'] = flex_replacement_level

        print("Replacement level players: ", self.find_positional_replacement_level_players())

        # Calculate PAR for each player
        self.overall_rankings['PAR'] = self.overall_rankings.apply(
            lambda row: row['Avg Proj Pts'] - replacement_level_points.get(row['Position'], 0),
            axis=1
        )

        par_table = self.overall_rankings[self.overall_rankings['Position'].isin(['QB', 'RB', 'WR', 'TE'])]

        desired_columns = ['Ranking', 'Player', 'Position', 'ADP', 'PAR']
        par_table = par_table.loc[:, desired_columns]

        par_table['PAR'] = par_table['PAR'].round(1)

        par_table = par_table.sort_values(by='PAR', ascending=False).reset_index(drop=True)

        par_table['Ranking'] = par_table['PAR'].rank(ascending=False, method='first').astype(int)

        return par_table
