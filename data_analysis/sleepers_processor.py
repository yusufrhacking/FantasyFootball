import pandas as pd

def get_sleepers(par_table, config):
    sleepers = []

    number_of_teams = config["number_of_teams"]

    position_requirements = config["position_requirements"]
    total_positions_used = sum(position_requirements.values())

    par_cutoff = number_of_teams * total_positions_used

    for index, row in par_table.iterrows():
        par_ranking = row['Ranking']
        yahoo_adp = row['ADP']
        player_par = row['PAR']

        if yahoo_adp == "-":
            continue
        if pd.isna(yahoo_adp):
            continue

        adj_yahoo_adp = max(0, int(yahoo_adp)-1)

        par_column = par_table['PAR']

        adp_par = max(0, par_column[adj_yahoo_adp])

        if player_par > 0:
            added_par_value = player_par - adp_par
            if par_ranking <= par_cutoff:
                sleepers.append({
                    'Player': row['Player'],
                    'Position': row['Position'],
                    'Added_PAR_Value': added_par_value,
                    'PAR_Ranking': par_ranking,
                    'Yahoo_ADP': yahoo_adp,
                    'ADP_PAR': adp_par,
                    'PAR': player_par
                })

    sleepers_df = pd.DataFrame(sleepers)

    sleepers_df = sleepers_df.sort_values(by='Added_PAR_Value', ascending=False)
    sleepers_df['Added_PAR_Value'] = sleepers_df['Added_PAR_Value'].apply(lambda x: round(x, 1))

    sleepers_df = sleepers_df.reset_index(drop=True)

    return sleepers_df
