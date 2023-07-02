# Author: James Yang
# Generate proprietary fantasy players drafted in 2022 league. 

# API pulled from https://github.com/cwendt94/espn-api
from espn_api.football import League
import pandas as pd

league_id = 42936131 #Example: https://fantasy.espn.com/football/team?leagueId=829963546&seasonId=2022&teamId=1&fromTeamId=1 #42936131
year = 2022
league = League(league_id=league_id, year=year)


# Goes through espn API, and recieves the draft picks and places them in a csv.
def get_draft_picks():
    df = pd.DataFrame()

    teams = []
    players = []
    id = []
    round_num = []
    round_pick = []


    for pick in league.draft:
        teams.append(pick.team.team_name)
        players.append(pick.playerName)
        round_num.append(pick.round_num)
        round_pick.append(pick.round_pick)
        id.append(pick.playerId)
        
    df['Team'] = teams
    df['Player'] = players
    df['ID'] = id
    df['RoundPick'] = round_pick
    df['RoundNum'] = round_num
    df.to_csv('data/fantasy_league_data/drafted_players.csv')
    print("Sample output of Draft Picks: ")
    print(df.head(10))

# We need to get weekly owned players because teams switch up their roster so their players can alter from week to week.
def get_weekly_owned_players():
    teams = []
    players = []
    projected = []
    actual = []
    ranks = []
    weeks = []
    current_df = pd.DataFrame()
    for i in range(1, 18):
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
    current_df.to_csv('data/fantasy_league_data/current_players.csv')

# Get all of the teams' player stats for each week.
def get_player_stats():

    #1. Get the lineups that each team plays.
    lineups = []
    for i in range(1, 18):
        box_scores = league.box_scores(i)
        for j in range(len(box_scores)):
            lineups.append(box_scores[j].away_lineup)

    #2. Get all of the players and their associated stats
    all_players = pd.DataFrame()
    names = []
    project = []
    actual = []
    ranks = []
    position = []
    for i in range(18):
        league.current_week = i
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

    #3. Append a week with the players
    total_df = pd.DataFrame()
    for player in all_players['Player'].unique():
        df = all_players[all_players['Player'] == player]
        df.insert(0, 'Week', range(1, 1 + len(all_players[all_players['Player'] == player])))
        total_df = pd.concat([total_df, df])


    #4. Get the weekly owned players. Teams will switch up the players that they own, they will be different from their draft picks so we need to get those and put them in a 
    # csv called current_players.csv
    get_weekly_owned_players()

    #Merge the df with the player stats
    merged_df = pd.merge(total_df, pd.read_csv('data/fantasy_league_data/current_players.csv'), on=['Week', 'Player'])
    #Rename the stuff to make it interpretable.
    merged_df = merged_df.rename(columns={"Rank_x": "Rank", "Actual_Points_x": "Actual_Points", "Expected_Points": "Total_Expected", "Actual_Points_y": "Total_Actual"})
    print("Sample Output of Total DF: ")
    print(merged_df[['Week', 'Team', 'Player', 'Projected_Points', 'Actual_Points', 'Rank', "Position"]].head(10))
    return merged_df[['Week', 'Team', 'Player', 'Projected_Points', 'Actual_Points', 'Rank', "Position"]]



def main():
    # Get draft picks and place them in data/fantasy_league_data/drafted_players.csv
    get_draft_picks()

    # Get the players stats for each week from the API.
    all_players_stats = get_player_stats()

    #Export to csv
    all_players_stats.to_csv('Data/fantasy_league_data/players_teams_stats.csv')
    

main()