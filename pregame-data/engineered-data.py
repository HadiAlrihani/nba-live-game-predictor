from nba_api.stats.static import teams
import pandas as pd
import math

# elo expected win probability formula for team1
def expected_win_prob(team1_elo, team2_elo):
    return 1 / (1 + 10 ** (-(team1_elo - team2_elo) / 400))

# update elo rating, using strength update = 20
def calculate_elo(team1_elo, team2_elo, actual, margin, k=20):
    expected = expected_win_prob(team1_elo, team2_elo)

    # margin-of-victory multiplier
    mov_multiplier = math.log(abs(margin) + 1) * (2.2 / ((team1_elo - team2_elo) * 0.001 + 2.2))

    new_elo = team1_elo + k * mov_multiplier * (actual - expected)

    return int(new_elo)

# modify each game in a season
def clean_season_games(season_games):
    cleaned_season = []
    prev_season_game = 2021

    for game in season_games.itertuples():
        game_season = game.SEASON_ID
        if str(game_season)[-4:] != str(prev_season_game)[-4:]:
            prev_season_game = game_season
            team_stats[
                ["Wins", "Losses", "FGA", "FGM", "FG3A", "FG3M", "FTA", "FTM", "OREB", 
                        "DREB", "AST", "STL", "BLK", "TOV", "PF", "PLUS_MINUS"
                        ]] = 0.0
        
        game_id = game.GAME_ID

        # get team names
        team1 = game.TEAM_ABBREVIATION_A
        team2 = game.TEAM_ABBREVIATION_B

        #get stats coming into the game
        team1_wins = team_stats.loc[team1, "Wins"]
        team1_losses = team_stats.loc[team1, "Losses"]

        team1_gp = team1_wins + team1_losses

        team2_wins = team_stats.loc[team2, "Wins"]
        team2_losses = team_stats.loc[team2, "Losses"]

        team2_gp = team2_wins + team2_losses

        team1_fga = team_stats.loc[team1, "FGA"]
        team1_fgm = team_stats.loc[team1, "FGM"]

        team2_fga = team_stats.loc[team2, "FGA"]
        team2_fgm = team_stats.loc[team2, "FGM"]

        team1_fg3a = team_stats.loc[team1, "FG3A"]
        team1_fg3m = team_stats.loc[team1, "FG3M"]

        team2_fg3a = team_stats.loc[team2, "FG3A"]
        team2_fg3m = team_stats.loc[team2, "FG3M"]

        team1_fta = team_stats.loc[team1, "FTA"]
        team1_ftm = team_stats.loc[team1, "FTM"]

        team2_fta = team_stats.loc[team2, "FTA"]
        team2_ftm = team_stats.loc[team2, "FTM"]

        team1_oreb = team_stats.loc[team1, "OREB"]
        team1_dreb = team_stats.loc[team1, "DREB"]

        team2_oreb = team_stats.loc[team2, "OREB"]
        team2_dreb = team_stats.loc[team2, "DREB"]

        team1_ast = team_stats.loc[team1, "AST"]
        team2_ast = team_stats.loc[team2, "AST"]

        team1_stl = team_stats.loc[team1, "STL"]
        team2_stl = team_stats.loc[team2, "STL"]

        team1_blk = team_stats.loc[team1, "BLK"]
        team2_blk = team_stats.loc[team2, "BLK"]

        team1_tov = team_stats.loc[team1, "TOV"]
        team2_tov = team_stats.loc[team2, "TOV"]

        team1_pf = team_stats.loc[team1, "PF"]
        team2_pf = team_stats.loc[team2, "PF"]

        team1_margin = team_stats.loc[team1, "PLUS_MINUS"]
        team2_margin = team_stats.loc[team2, "PLUS_MINUS"]

        team1_elo = team_stats.loc[team1, "ELO"]
        team2_elo = team_stats.loc[team2, "ELO"]

        # add season stats to cleaned list
        # each row represents: stats coming into the game + the result of the game itself
        cleaned_season.append({
            "SEASON": game_season,
            "GAME_ID": game_id,
            
            # TEAM A
            "TEAM_A": team1,
            "TEAM_A_W": team1_wins,
            "TEAM_A_L": team1_losses,

            "TEAM_A_FGA": team1_fga / team1_gp if team1_gp != 0 else 0,
            "TEAM_A_FGM": team1_fgm / team1_gp if team1_gp != 0 else 0,
            "TEAM_A_FG_PCT": (team1_fgm / team1_fga) if team1_fga != 0 else 0,

            "TEAM_A_FG3A": team1_fg3a / team1_gp if team1_gp != 0 else 0,
            "TEAM_A_FG3M": team1_fg3m / team1_gp if team1_gp != 0 else 0,
            "TEAM_A_FG3_PCT": (team1_fg3m / team1_fg3a) if team1_fg3a != 0 else 0,

            "TEAM_A_FTA": team1_fta / team1_gp if team1_gp != 0 else 0,
            "TEAM_A_FTM": team1_ftm / team1_gp if team1_gp != 0 else 0,
            "TEAM_A_FT_PCT": (team1_ftm / team1_fta) if team1_fta != 0 else 0,

            "TEAM_A_OREB": team1_oreb / team1_gp if team1_gp != 0 else 0,
            "TEAM_A_DREB": team1_dreb / team1_gp if team1_gp != 0 else 0,
            "TEAM_A_REB": (team1_oreb + team1_dreb) / team1_gp if team1_gp != 0 else 0,

            "TEAM_A_AST": team1_ast / team1_gp if team1_gp != 0 else 0,
            "TEAM_A_STL": team1_stl / team1_gp if team1_gp != 0 else 0,
            "TEAM_A_BLK": team1_blk / team1_gp if team1_gp != 0 else 0,
            "TEAM_A_TOV": team1_tov / team1_gp if team1_gp != 0 else 0,
            "TEAM_A_PF": team1_pf / team1_gp if team1_gp != 0 else 0,

            "TEAM_A_PLUS_MINUS": team1_margin / team1_gp if team1_gp != 0 else 0,
            "TEAM_A_ELO": team1_elo,

            # TEAM B
            "TEAM_B": team2,
            "TEAM_B_W": team2_wins,
            "TEAM_B_L": team2_losses,

            "TEAM_B_FGA": team2_fga / team2_gp if team2_gp != 0 else 0,
            "TEAM_B_FGM": team2_fgm / team2_gp if team2_gp != 0 else 0,
            "TEAM_B_FG_PCT": (team2_fgm / team2_fga) if team2_fga != 0 else 0,

            "TEAM_B_FG3A": team2_fg3a / team2_gp if team2_gp != 0 else 0,
            "TEAM_B_FG3M": team2_fg3m / team2_gp if team2_gp != 0 else 0,
            "TEAM_B_FG3_PCT": (team2_fg3m / team2_fg3a) if team2_fg3a != 0 else 0,

            "TEAM_B_FTA": team2_fta / team2_gp if team2_gp != 0 else 0,
            "TEAM_B_FTM": team2_ftm / team2_gp if team2_gp != 0 else 0,
            "TEAM_B_FT_PCT": (team2_ftm / team2_fta) if team2_fta != 0 else 0,

            "TEAM_B_OREB": team2_oreb / team2_gp if team2_gp != 0 else 0,
            "TEAM_B_DREB": team2_dreb / team2_gp if team2_gp != 0 else 0,
            "TEAM_B_REB": (team2_oreb + team2_dreb) / team2_gp if team2_gp != 0 else 0,

            "TEAM_B_AST": team2_ast / team2_gp if team2_gp != 0 else 0,
            "TEAM_B_STL": team2_stl / team2_gp if team2_gp != 0 else 0,
            "TEAM_B_BLK": team2_blk / team2_gp if team2_gp != 0 else 0,
            "TEAM_B_TOV": team2_tov / team2_gp if team2_gp != 0 else 0,
            "TEAM_B_PF": team2_pf / team2_gp if team2_gp != 0 else 0,

            "TEAM_B_PLUS_MINUS": team2_margin / team2_gp if team2_gp != 0 else 0,
            "TEAM_B_ELO": team2_elo,

            # TARGET VARIABLE
            "TEAM_A_WIN": game.WL_A
        })

        # update season stats including the game
        team_stats.loc[team1, "ELO"] = calculate_elo(team1_elo, team2_elo, game.WL_A, game.PLUS_MINUS_A)
        team_stats.loc[team2, "ELO"] = calculate_elo(team2_elo, team1_elo, game.WL_B, game.PLUS_MINUS_B)
        
        team_stats.loc[team1, "Wins"] += game.WL_A
        team_stats.loc[team1, "Losses"] += game.WL_B

        team_stats.loc[team2, "Wins"] += game.WL_B
        team_stats.loc[team2, "Losses"] += game.WL_A

        team_stats.loc[team1, "FGA"] += game.FGA_A
        team_stats.loc[team1, "FGM"] += game.FGM_A

        team_stats.loc[team2, "FGA"] += game.FGA_B
        team_stats.loc[team2, "FGM"] += game.FGM_B

        team_stats.loc[team1, "FG3A"] += game.FG3A_A
        team_stats.loc[team1, "FG3M"] += game.FG3M_A

        team_stats.loc[team2, "FG3A"] += game.FG3A_B
        team_stats.loc[team2, "FG3M"] += game.FG3M_B

        team_stats.loc[team1, "FTA"] += game.FTA_A
        team_stats.loc[team1, "FTM"] += game.FTM_A

        team_stats.loc[team2, "FTA"] += game.FTA_B
        team_stats.loc[team2, "FTM"] += game.FTM_B

        team_stats.loc[team1, "OREB"] += game.OREB_A
        team_stats.loc[team1, "DREB"] += game.DREB_A

        team_stats.loc[team2, "OREB"] += game.OREB_B
        team_stats.loc[team2, "DREB"] += game.DREB_B

        team_stats.loc[team1, "AST"] += game.AST_A
        team_stats.loc[team2, "AST"] += game.AST_B

        team_stats.loc[team1, "STL"] += game.STL_A
        team_stats.loc[team2, "STL"] += game.STL_B

        team_stats.loc[team1, "BLK"] += game.BLK_A
        team_stats.loc[team2, "BLK"] += game.BLK_B

        team_stats.loc[team1, "TOV"] += game.TOV_A
        team_stats.loc[team2, "TOV"] += game.TOV_B

        team_stats.loc[team1, "PF"] += game.PF_A
        team_stats.loc[team2, "PF"] += game.PF_B

        team_stats.loc[team1, "PLUS_MINUS"] += game.PLUS_MINUS_A
        team_stats.loc[team2, "PLUS_MINUS"] += game.PLUS_MINUS_B


    return pd.DataFrame(cleaned_season)


#get teams
nba_teams = teams.get_teams()
nba_teams = [team['abbreviation'] for team in nba_teams]

#create dataframe/list for each team and their season stats + w/l record
team_stats = pd.DataFrame(nba_teams, columns=["Team"]).set_index("Team")
team_stats[["ELO"]] = 1500 # default starting elo
team_stats[
    ["Wins", "Losses", "FGA", "FGM", "FG3A", "FG3M", "FTA", "FTM", "OREB", 
            "DREB", "AST", "STL", "BLK", "TOV", "PF", "PLUS_MINUS"
            ]] = 0.0

# get all games
games2124 = pd.read_csv("games2124_raw.csv")
games2425 = pd.read_csv("games2425_raw.csv")
games2526 = pd.read_csv("games2526_raw.csv")

# Change Win/Loss categories to binary mapping
games2124["WL_A"] = games2124["WL_A"].map({"W": 1, "L": 0})
games2124["WL_B"] = games2124["WL_B"].map({"W": 1, "L": 0})

games2425["WL_A"] = games2425["WL_A"].map({"W": 1, "L": 0})
games2425["WL_B"] = games2425["WL_B"].map({"W": 1, "L": 0})

games2526["WL_A"] = games2526["WL_A"].map({"W": 1, "L": 0})
games2526["WL_B"] = games2526["WL_B"].map({"W": 1, "L": 0})

#for each game, add per game stats + each teams elo + w/l record into a new df
games2124 = clean_season_games(games2124)
games2425 = clean_season_games(games2425)
games2526 = clean_season_games(games2526)

# save engineered games to csv
games2124.to_csv("games2124.csv", index=False)
games2425.to_csv("games2425.csv", index=False)
games2526.to_csv("games2526.csv", index=False)