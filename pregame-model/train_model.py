import xgboost as xgb
import pandas as pd
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, log_loss

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
    learning_rate=0.05,)

pregame_model.fit(X_train, y_train)

predictions = pregame_model.predict_proba(X_validate)[:, 1]
y_pred = (predictions >= 0.58).astype(int)


# evaluate model
cm = confusion_matrix(y_validate, y_pred)
print(cm)

print(f"Accuracy: {accuracy_score(y_validate, y_pred):.3f}")
print(f"Precision: {precision_score(y_validate, y_pred):.3f}")
print(f"Recall: {recall_score(y_validate, y_pred):.3f}")
print(f"Log loss: {log_loss(y_validate, predictions):.3f}")

pregame_model.save_model("pregame_model.json")