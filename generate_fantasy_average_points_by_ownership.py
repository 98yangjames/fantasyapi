import pandas as pd


df = pd.read_csv('Data/fantasy_league_data/players_teams_stats.csv')
stats_of_players = []
for team in df.Team.unique():
    team_df = df[df['Team'] == team]
    for player in team_df.Player.unique():
        player_stats = team_df[team_df['Player'] == player]
        stats_of_players.append([team, player, player_stats.Actual_Points.mean(), player_stats.Projected_Points.mean(), player_stats.Position.values[0], len(player_stats)])


stats_of_players_df = pd.DataFrame(stats_of_players)
stats_of_players_df.columns = ['Team', 'Player', 'Average Scored Points', 'Average Projected Points', 'Position', 'Length of Ownership']
stats_of_players_df['Residual'] = stats_of_players_df['Average Scored Points'] - stats_of_players_df['Average Projected Points']
stats_of_players_df.to_csv('Data/fantasy_league_data/Average_Points_By_Ownership.csv')
print(stats_of_players_df)

