from nba_api.stats.static import teams
import pandas as pd

# elo expected win probability formula for team1
def expected_win_prob(team1_elo, team2_elo):
    return 1 / (1 + 10 ** (-(team1_elo - team2_elo) / 400))

# update elo rating, using strength update = 20
def calculate_elo(team1_elo, team2_elo, actual, k=20):
    expected = expected_win_prob(team1_elo, team2_elo)
    new_elo = team1_elo + k * (actual - expected)
    return new_elo

# modify each game in a season
def clean_season_games(season_games):
    pass


#get teams
nba_teams = teams.get_teams()
nba_teams = [team['full_name'] for team in nba_teams]

#create dataframe/list for each team and their season stats + w/l record
team_stats = pd.DataFrame(nba_teams, columns=["Team"])
team_stats[["ELO"]] = 1500
team_stats[
    ["Wins", "Losses", "FGA", "FGM", "FG3A", "FG3M", "FTA", "FTM", "OREB", 
            "DREB", "REB", "AST", "STL", "BLK", "TOV", "PLUS_MINUS"
            ]] = 0

#get all games
games2124 = pd.read_csv("games2124_raw.csv")
games2425 = pd.read_csv("games2425_raw.csv")
games2526 = pd.read_csv("games2526_raw.csv")

all_games = pd.concat(
    [games2124, games2425, games2526],
    ignore_index=True
)

#for each game, add per game stats + each teams elo + w/l record, then remove unwanted data

#separate label (home team w/l) from data