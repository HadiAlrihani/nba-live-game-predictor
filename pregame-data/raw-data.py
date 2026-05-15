from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguegamefinder
import pandas as pd

## FUNCTION COPIED FROM nba_api DOCS
def combine_team_games(df, keep_method="home"):
    """Combine a TEAM_ID-GAME_ID unique table into rows by game. Slow.

    Parameters
    ----------
    df : Input DataFrame.
    keep_method : {'home', 'away', 'winner', 'loser', ``None``}, default 'home'
        - 'home' : Keep rows where TEAM_A is the home team.
        - 'away' : Keep rows where TEAM_A is the away team.
        - 'winner' : Keep rows where TEAM_A is the losing team.
        - 'loser' : Keep rows where TEAM_A is the winning team.
        - ``None`` : Keep all rows. Will result in an output DataFrame the same
            length as the input DataFrame.

    Returns
    -------
    result : DataFrame
    """
    # Join every row to all others with the same game ID.
    joined = pd.merge(
        df, df, suffixes=["_A", "_B"], on=["SEASON_ID", "GAME_ID", "GAME_DATE"]
    )
    # Filter out any row that is joined to itself.
    result = joined[joined.TEAM_ID_A != joined.TEAM_ID_B]
    # Take action based on the keep_method flag.
    if keep_method is None:
        # Return all the rows.
        pass
    elif keep_method.lower() == "home":
        # Keep rows where TEAM_A is the home team.
        result = result[result.MATCHUP_A.str.contains(" vs. ")]
    elif keep_method.lower() == "away":
        # Keep rows where TEAM_A is the away team.
        result = result[result.MATCHUP_A.str.contains(" @ ")]
    elif keep_method.lower() == "winner":
        result = result[result.WL_A == "W"]
    elif keep_method.lower() == "loser":
        result = result[result.WL_A == "L"]
    else:
        raise ValueError(f"Invalid keep_method: {keep_method}")
    return result


#get all games for each season
#2021/2022 - 2023/2024 -> training
# Regular season
regular_games = leaguegamefinder.LeagueGameFinder(
    player_or_team_abbreviation="T",
    season_nullable="2021-22",
    season_type_nullable="Regular Season"
).get_data_frames()[0]

# Playoffs
playoff_games = leaguegamefinder.LeagueGameFinder(
    player_or_team_abbreviation="T",
    season_nullable="2021-22",
    season_type_nullable="Playoffs"
).get_data_frames()[0]

# Combine
games2122 = pd.concat(
    [regular_games, playoff_games],
    ignore_index=True
)

# Sort chronologically
games2122 = games2122.sort_values("GAME_DATE").reset_index(drop=True)


# Regular season
regular_games = leaguegamefinder.LeagueGameFinder(
    player_or_team_abbreviation="T",
    season_nullable="2022-23",
    season_type_nullable="Regular Season"
).get_data_frames()[0]

# Playoffs
playoff_games = leaguegamefinder.LeagueGameFinder(
    player_or_team_abbreviation="T",
    season_nullable="2022-23",
    season_type_nullable="Playoffs"
).get_data_frames()[0]

# Combine
games2223 = pd.concat(
    [regular_games, playoff_games],
    ignore_index=True
)

# Sort chronologically
# Regular season
regular_games = leaguegamefinder.LeagueGameFinder(
    player_or_team_abbreviation="T",
    season_nullable="2023-24",
    season_type_nullable="Regular Season"
).get_data_frames()[0]

# Playoffs
playoff_games = leaguegamefinder.LeagueGameFinder(
    player_or_team_abbreviation="T",
    season_nullable="2023-24",
    season_type_nullable="Playoffs"
).get_data_frames()[0]

# Combine
games2324 = pd.concat(
    [regular_games, playoff_games],
    ignore_index=True
)

# Sort chronologically
games2324 = games2324.sort_values("GAME_DATE").reset_index(drop=True)

#2024/25 -> validation
# Regular season
regular_games = leaguegamefinder.LeagueGameFinder(
    player_or_team_abbreviation="T",
    season_nullable="2024-25",
    season_type_nullable="Regular Season"
).get_data_frames()[0]

# Playoffs
playoff_games = leaguegamefinder.LeagueGameFinder(
    player_or_team_abbreviation="T",
    season_nullable="2024-25",
    season_type_nullable="Playoffs"
).get_data_frames()[0]

# Combine
games2425 = pd.concat(
    [regular_games, playoff_games],
    ignore_index=True
)

# Sort chronologically
games2425 = games2425.sort_values("GAME_DATE").reset_index(drop=True)

#2025/2026 -> testing
# Regular season
regular_games = leaguegamefinder.LeagueGameFinder(
    player_or_team_abbreviation="T",
    season_nullable="2025-26",
    season_type_nullable="Regular Season"
).get_data_frames()[0]

# Playoffs
playoff_games = leaguegamefinder.LeagueGameFinder(
    player_or_team_abbreviation="T",
    season_nullable="2025-26",
    season_type_nullable="Playoffs"
).get_data_frames()[0]

# Combine
games2526 = pd.concat(
    [regular_games, playoff_games],
    ignore_index=True
)

# Sort chronologically
games2526 = games2526.sort_values("GAME_DATE").reset_index(drop=True)


#all games for training
games2124 = pd.concat(
    [games2122, games2223, games2324],
    ignore_index=True   
)

# join duplicate game entries
games2124 = combine_team_games(games2124)
games2425 = combine_team_games(games2425)
games2526 = combine_team_games(games2526)

# save game data to csv
games2124.to_csv("games2124.csv", index=False)
games2425.to_csv("games2425.csv", index=False)
games2526.to_csv("games2526.csv", index=False)