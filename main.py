from espn_api.football import League
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


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

    current_df['Team'] = teams
    current_df['Player'] = players
    current_df['Week'] = weeks
    current_df['Rank'] = ranks
    current_df['Expected_Points'] = projected
    current_df['Actual_Points'] = actual
    current_df['Week'] = weeks
    current_df['Difference'] = current_df['Actual_Points'] - current_df['Expected_Points']
    current_df.to_csv('Data/current_players.csv')
    return current_df


def get_lineups_teams_projected(league):
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

    return lineups, teams, projected

def get_all_players(lineups):
    all_players = pd.DataFrame()

    names = []
    project = []
    actual = []
    ranks = []

    for players in lineups:
        for player in players:
            names.append(player.name)
            project.append(player.projected_points)
            actual.append(player.points)
            ranks.append(player.pro_pos_rank)
            
            
    all_players['Player'] = names
    all_players['Projected_Points'] = project
    all_players['Actual_Points'] = actual
    all_players['Rank'] = ranks

    return all_players

def insert_week_count(all_players):
    total_df = pd.DataFrame()
    for player in all_players['Player'].unique():
        df = all_players[all_players['Player'] == player]
        df.insert(0, 'Week', range(1, 1 + len(all_players[all_players['Player'] == player])))
        total_df = pd.concat([total_df, df])

    return total_df
def main():
    #fan's - 42936131
    #mine - 829963546
    league_id = 829963546
    year = 2022
    league = create_league(league_id, year)
    
    teams = combine(league, 13)
    lineups, teams, projected = get_lineups_teams_projected(league)
    players = get_all_players(lineups)
    players = insert_week_count(players)
    merged_df = pd.merge(players, teams, on=['Week', 'Player'])
    print(merged_df)

main()