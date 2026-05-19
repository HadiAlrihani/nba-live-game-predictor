import xgboost as xgb
import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix, recall_score, precision_score, log_loss

pregame_model = xgb.XGBClassifier()
pregame_model.load_model("pregame_model.json")

# get test data
games2526 = pd.read_csv("../pregame-data/games2526.csv")
games2526 = games2526.drop(columns=["SEASON", "GAME_ID", "TEAM_A", "TEAM_B"])

X_test = games2526.drop(columns=["TEAM_A_WIN"])
y_test = games2526["TEAM_A_WIN"]

predictions = pregame_model.predict_proba(X_test)[:, 1]
y_pred = (predictions > 0.58).astype(int)

# evaluate model
cm = confusion_matrix(y_test, y_pred)
print(cm)

print(f"Accuracy: {accuracy_score(y_test, y_pred):.3f}")
print(f"Precision: {precision_score(y_test, y_pred):.3f}")
print(f"Recall: {recall_score(y_test, y_pred):.3f}")
print(f"Log loss: {log_loss(y_test, predictions):.3f}")