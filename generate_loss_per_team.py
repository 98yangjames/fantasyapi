import pandas as pd

stats_of_players_df = pd.read_csv('Data/fantasy_league_data/Average_Points_By_Ownership.csv')

stats_of_players_df['Weight of Ownership'] = stats_of_players_df['Length of Ownership'] / 17
stats_of_players_df['Weighted Residual'] = stats_of_players_df['Residual'] * stats_of_players_df['Weight of Ownership']

team_and_weighted_residual = []
for team in stats_of_players_df['Team'].unique():    
    team_and_weighted_residual.append([team, stats_of_players_df[stats_of_players_df['Team'] == team]['Weighted Residual'].sum()])

output_df = pd.DataFrame(team_and_weighted_residual)
output_df.columns = ['Team', 'Weighted Sum']
output_df.to_csv('Data/fantasy_league_data/weighted_sum_of_residuals.csv')