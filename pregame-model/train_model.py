import xgboost as xgb
import pandas as pd
from sklearn.calibration import CalibratedClassifierCV

# get training data
games2124 = pd.read_csv("../pregame-data/games2124.csv")
games2124 = games2124.drop(columns=["SEASON", "GAME_ID", "TEAM_A", "TEAM_B"])

X_train = games2124.drop(columns=["TEAM_A_WIN"])
y_train = games2124["TEAM_A_WIN"]

# get validation data
games2425 = pd.read_csv("../pregame-data/games2425.csv")
games2425 = games2425.drop(columns=["SEASON", "GAME_ID", "TEAM_A", "TEAM_B"])

X_validate = games2425.drop(columns=["TEAM_A_WIN"])
y_validate = games2425["TEAM_A_WIN"]

pregame_model = xgb.XGBClassifier(
    n_estimators=100,
    max_depth=2,
    learning_rate=0.05,
    eval_metric="logloss",
    early_stopping_rounds=50
)

pregame_model.fit(
    X_train,
    y_train,
    eval_set=[(X_validate, y_validate)],
    verbose=True
)