from espn_api.football import League
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.neighbors import NearestNeighbors

#---- Helper functions ---#
def create_league(league_id, year):
    return League(league_id = league_id, year = year)

def combine(league, num_weeks):
    teams = []
    players = []
    projected = []
    actual = []
    stats = []
    ranks = []
    weeks = []
    position = []
    current_df = pd.DataFrame()
    for i in range(1, num_weeks):
        league.load_roster_week(i)
        for team in league.teams:
            for player in team.roster:
                weeks.append(i)
                teams.append(team.team_name)
                players.append(player.name)
                projected.append(player.projected_total_points)
                actual.append(player.total_points)
                ranks.append(player.posRank)
                position.append(player.position)
                

    current_df['Team'] = teams
    current_df['Player'] = players
    current_df['Week'] = weeks
    current_df['Rank'] = ranks
    current_df['Expected_Points'] = projected
    current_df['Actual_Points'] = actual
    current_df['Week'] = weeks
    current_df['Difference'] = current_df['Actual_Points'] - current_df['Expected_Points']
    current_df['Position'] = position
    current_df.to_csv('Data/current_players.csv')
    return current_df

def get_lineups_teams_projected(league):
    df = pd.DataFrame()
    lineups = []
    teams = []
    projected = []
    for i in range(1, 12):
        box_scores = league.box_scores(i)
        for j in range(len(box_scores)):
            lineups.append(box_scores[j].home_lineup)
            teams.append(box_scores[j].home_team)
            projected.append(box_scores[j].home_projected)

            lineups.append(box_scores[j].away_lineup)
            teams.append(box_scores[j].away_team)
            projected.append(box_scores[j].away_projected)

    # df['Lineups'] = lineups
    # df['Teams'] = teams
    # df['Projected'] = projected
    return lineups, teams, projected

def get_all_players(lineups):
    all_players = pd.DataFrame()

    names = []
    project = []
    actual = []
    ranks = []
    position = []
    for players in lineups:
        for player in players:
            names.append(player.name)
            project.append(player.projected_points)
            actual.append(player.points)
            ranks.append(player.pro_pos_rank)
            position.append(player.position)
            
            
    all_players['Player'] = names
    all_players['Projected_Points'] = project
    all_players['Actual_Points'] = actual
    all_players['Rank'] = ranks
    all_players['Position'] = position

    return all_players

def insert_week_count(all_players):
    total_df = pd.DataFrame()
    for player in all_players['Player'].unique():
        df = all_players[all_players['Player'] == player]
        df.insert(0, 'Week', range(1, 1 + len(all_players[all_players['Player'] == player])))
        total_df = pd.concat([total_df, df])

    return total_df
# -------------------------#



def data_pull():
    #fan's - 42936131
    #mine - 829963546
    league_id = 829963546
    year = 2022
    league = create_league(league_id, year)
    
    teams = combine(league, 13)
    
    lineups, teams, projected = get_lineups_teams_projected(league)
    players = get_all_players(lineups)
    players = insert_week_count(players)
    

def generate_projected_vs_expected(dataframe, name):    
    hovertemplate = "Player: %{customdata[0]} <br>Actual Avg Points:%{customdata[1]}: <br>Projected Points: %{customdata[2]} <br>Point Residuals: %{customdata[3]} <br>Team: %{customdata[4]} </br>"
    plot = px.scatter(dataframe, x = 'Actual_Points', y = 'Point-Residuals', color = 'Team', title = 'Projected vs. Distance from Expectation for ' + name, custom_data=['Player', 'Actual_Points','Expected_Points','Point-Residuals', 'Team'], color_discrete_sequence=px.colors.qualitative.Dark24)
    plot.update_layout(xaxis_title = 'Actual Avg Points', yaxis_title = 'Point Residuals', plot_bgcolor = 'grey')
    plot.update_traces(hovertemplate = hovertemplate)
    # plot.update_xaxes(showgrid = False)
    # plot.update_yaxes(showgrid = False)
    plot.add_hline(y=dataframe['Point-Residuals'].mean(), line_color = 'red')
    # plot.add_hline(y=rb_df['Projected_Points'].mean(), line_color = 'yellow')
    plot.write_html("Data/" + name + ".html")
    plot.show()

def k_nearest_neighbor_plot(y_pred):
    plot = px.scatter(y_pred)
    plot.show()

def add_point_residuals(dataframe):
    dataframe['Point-Residuals'] = dataframe['Actual_Points'] - dataframe['Expected_Points']
    dataframe.loc[dataframe['Point-Residuals'] >= dataframe['Point-Residuals'].mean(), 'label'] = 1
    dataframe.loc[dataframe['Point-Residuals'] < dataframe['Point-Residuals'].mean(), 'label'] = 0
    dataframe['normalized_label'] = dataframe['Point-Residuals'] /dataframe['Point-Residuals'].abs().max()
    return dataframe

def k_nearest_neighbor(players):
    # Import LabelEncoder
    from sklearn import preprocessing
    #creating labelEncoder
    le = preprocessing.LabelEncoder()
    
    # Converting string labels into numbers. Predicting Actual Points based on Position and Player
    position_encoded=le.fit_transform(players['Position'])
    players_encoded = le.fit_transform(players['Player'])
    rank_encoded = le.fit_transform(players['Rank'])
    labels = le.fit_transform(players['Actual_Points'])
    
    # --- features being used ---#  
    features = list(zip(players_encoded, position_encoded, rank_encoded))
    from sklearn.neighbors import KNeighborsClassifier

    from sklearn.model_selection import train_test_split
    
    # Split dataset into training set and test set

    X_train, X_test, y_train, y_test = train_test_split(features, labels,test_size=0.3) # 70% training and 30% test
    knn = KNeighborsClassifier(n_neighbors=3)
    knn.fit(X_train, y_train)
    y_pred = knn.predict(X_test)
    from sklearn import metrics
    # Model Accuracy, how often is the classifier correct?
    print("Accuracy:",metrics.accuracy_score(y_test, y_pred))
    k_nearest_neighbor_plot(y_pred)

def main():
    # data_pull()
    players = pd.read_csv('Data/current_players.csv')
    # print(players)
    print(players.groupby(['Team', 'Week', 'Player', 'Position'], as_index=False).mean())

    players = add_point_residuals(players)
    players = players.groupby(['Team', 'Week', 'Player', 'Position'], as_index=False).mean().round(2)

    #--- this generates the unique player vs expected graph ---#
    # for position in players['Position'].unique():
    #     generate_projected_vs_expected(players[players['Position'] == position], position)

    #--- run a k-nearest neighbor ---#
    k_nearest_neighbor(players)


main()