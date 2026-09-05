"""Train dropout prediction model for Jaya Jaya Institut.

Binary classification: Dropout (1) vs Graduate (0).
'Enrolled' students are excluded from training (their final outcome is
unknown) — they are exactly the population the model will score in production.
"""
import json

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, f1_score, precision_score,
                             recall_score, roc_auc_score)
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

RANDOM_STATE = 42

df = pd.read_csv("data.csv", sep=";")

train_df = df[df["Status"].isin(["Dropout", "Graduate"])].copy()
train_df["target"] = (train_df["Status"] == "Dropout").astype(int)

X = train_df.drop(columns=["Status", "target"])
y = train_df["target"]
feature_names = X.columns.tolist()

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=RANDOM_STATE
)

candidates = {
    "LogisticRegression": Pipeline([
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression(max_iter=2000, random_state=RANDOM_STATE)),
    ]),
    "RandomForest": Pipeline([
        ("scaler", StandardScaler()),
        ("clf", RandomForestClassifier(
            n_estimators=300, max_depth=None, min_samples_leaf=2,
            class_weight="balanced", random_state=RANDOM_STATE, n_jobs=-1)),
    ]),
}

results = {}
for name, pipe in candidates.items():
    cv = cross_val_score(pipe, X_train, y_train, cv=5, scoring="f1")
    pipe.fit(X_train, y_train)
    proba = pipe.predict_proba(X_test)[:, 1]
    pred = pipe.predict(X_test)
    results[name] = {
        "cv_f1_mean": round(cv.mean(), 4),
        "accuracy": round(accuracy_score(y_test, pred), 4),
        "precision": round(precision_score(y_test, pred), 4),
        "recall": round(recall_score(y_test, pred), 4),
        "f1": round(f1_score(y_test, pred), 4),
        "roc_auc": round(roc_auc_score(y_test, proba), 4),
    }
    print(name, results[name])

best_name = max(results, key=lambda k: results[k]["f1"])
best_model = candidates[best_name]
print("Best model:", best_name)

# Feature importance (from RF) for reporting
rf = candidates["RandomForest"].named_steps["clf"]
importances = (
    pd.Series(rf.feature_importances_, index=feature_names)
    .sort_values(ascending=False)
)
print(importances.head(12))

joblib.dump(best_model, "model/model.joblib")
meta = {
    "best_model": best_name,
    "metrics": results,
    "feature_names": feature_names,
    "top_features": importances.head(12).round(4).to_dict(),
}
with open("model/metadata.json", "w") as f:
    json.dump(meta, f, indent=2)
print("Saved model/model.joblib and model/metadata.json")
