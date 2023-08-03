class RankingsProcessor:
    def __init__(self, overall_rankings, position_requirements, number_of_teams):
        self.overall_rankings = overall_rankings
        self.position_requirements = position_requirements
        self.number_of_teams = number_of_teams

    def calculate_in_use_players(self):
        in_use_players = {}
        for position, requirement in self.position_requirements.items():
            in_use_players[position] = int(requirement * self.number_of_teams * 1.5)
        return in_use_players

    def find_replacement_level_players(self):
        """Finds the replacement level player for each position."""
        in_use_players = self.calculate_in_use_players()

        replacement_players = {}
        for position, number_of_players in in_use_players.items():
            players_in_flex = {}
            players_in_position = {}
            if position == "FLEX":
                players_in_flex = self.overall_rankings[self.overall_rankings['Position'].isin(['RB', 'WR', 'TE'])]
            else:
                players_in_position = self.overall_rankings[self.overall_rankings['Position'] == position]

            relevant_players = players_in_flex if position == "FLEX" else players_in_position

            if len(relevant_players) > number_of_players:
                replacement_players[position] = relevant_players.iloc[number_of_players]
            else:
                replacement_players[position] = None

        return replacement_players


