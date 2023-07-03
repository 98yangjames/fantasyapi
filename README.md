# fantasyapi

This repo documents pulling data from fantasy football with your league through an api and analyzing it using statistics.

For the espn api: https://github.com/cwendt94/espn-api

# How to run
****generate_fantasy_players.py**** - file that generates the general data with who drafted what and what round/pick they got them at. It should produce in the Data folder current_players.csv and drafted_players.csv. The current_players.csv is only relevant during the middle of the season, because rosters are gonna change. NOTE: You need to run this first as it is a foundational set of csvs.

****generate_fantasy_average_points_by_ownership.py** **- file that generates the average amount of points that players generate based on how long the team owner has owned that player. For example: You pick up Joe Mixon for weeks 15-18, the average points that he gets there is the calculated average and projected in this file. That number is going to be different than the previous owner of Joe Mixon who had him for weeks 1-14. (Because Joe mixon decided to throw a 55 point bomb towards the end of the season).

****generate_cool_plots.py**** - file that generates the cool plots in the Data folder. They are htmls that are interactive through plotly. 
