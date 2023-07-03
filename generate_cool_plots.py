import pandas as pd
import plotly.express as px

df = pd.read_csv('Data/fantasy_league_data/Average_Points_By_Ownership.csv')
df = df.round(2)
df.head(10)

fig = px.scatter(df, x=df['Team'], y=df['Average Scored Points'], color=df['Average Scored Points'], hover_data=['Average Projected Points', 'Length of Ownership','Player'], title='Best Players for each Team by Ownership (in weeks)')
fig.add_hline(df['Average Scored Points'].mean(), line_color='Red', line_dash = 'dash')
fig.write_html('Data/cool_plots/best_players_for_each_team_by_ownership.html')
fig.show()

fig = px.scatter(df, x=df['Average Projected Points'], y=df['Average Scored Points'], color=df['Residual'], hover_data=['Average Projected Points', 'Length of Ownership','Player', 'Team'], title='Average Points vs. Projected Points by Ownership (in weeks)')
fig.add_hline(df['Average Scored Points'].mean(), line_color='Red', line_dash = 'dash')
fig.add_vline(df['Average Projected Points'].mean(), line_color='Red', line_dash = 'dash')
fig.write_html('Data/cool_plots/average_points_vs_projected_points_by_ownership.html')
fig.show()

fig = px.scatter(df, y=df['Residual'], x=df['Average Scored Points'], color=df['Residual'], hover_data=['Average Projected Points', 'Length of Ownership','Player', 'Team'], title='Over/Under Rated Players by Ownership (in weeks) (residual = difference in projected and actual points)')
fig.add_vline(df['Average Scored Points'].mean(), line_color='Red', line_dash = 'dash')
fig.add_hline(df['Residual'].mean(), line_color='Red', line_dash = 'dash')
fig.write_html('Data/cool_plots/over_under_rated_players_by_ownership.html')
fig.show()