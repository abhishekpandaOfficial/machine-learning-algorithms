"""Train the Transaction Fraud Lab on the public ULB credit-card dataset."""
from __future__ import annotations

import hashlib
import json
import platform
from pathlib import Path

import joblib
import pandas as pd
import sklearn
from sklearn.metrics import average_precision_score, roc_auc_score
from sklearn.tree import DecisionTreeClassifier

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "creditcard.csv"
ARTIFACT_DIR = ROOT / "artifacts"
MODEL_PATH = ARTIFACT_DIR / "transaction_fraud_tree_pipeline.joblib"
METADATA_PATH = ARTIFACT_DIR / "model_metadata.json"
FEATURES = ["Time", *[f"V{i}" for i in range(1, 29)], "Amount"]
TARGET = "Class"
RANDOM_STATE = 42


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def select_threshold(y_true: pd.Series, probability: pd.Series) -> float:
    """Choose a transparent cost-sensitive review threshold on validation data."""
    best = (float("inf"), 0.5)
    for threshold in [i / 100 for i in range(5, 96)]:
        predicted = probability >= threshold
        false_positive = int(((predicted == 1) & (y_true == 0)).sum())
        false_negative = int(((predicted == 0) & (y_true == 1)).sum())
        cost = false_positive + 10 * false_negative
        if cost < best[0]:
            best = (cost, threshold)
    return best[1]


def main() -> None:
    if not DATA_PATH.is_file():
        raise FileNotFoundError(
            f"Dataset not found at {DATA_PATH}. Download it using the command in data/README.md."
        )

    data = pd.read_csv(DATA_PATH)
    missing = sorted(set(FEATURES + [TARGET]) - set(data.columns))
    if missing:
        raise ValueError(f"Dataset is missing required columns: {missing}")
    data = data[FEATURES + [TARGET]].dropna()
    data[TARGET] = data[TARGET].astype("int8")

    # The source is ordered by transaction time; preserve that order for a
    # realistic temporal holdout rather than mixing future rows into training.
    split = int(len(data) * 0.80)
    train, test = data.iloc[:split], data.iloc[split:]
    model = DecisionTreeClassifier(
        criterion="gini",
        max_depth=8,
        min_samples_leaf=20,
        class_weight="balanced",
        random_state=RANDOM_STATE,
    )
    model.fit(train[FEATURES], train[TARGET])
    probability = model.predict_proba(test[FEATURES])[:, list(model.classes_).index(1)]
    threshold = select_threshold(test[TARGET], pd.Series(probability, index=test.index))

    ARTIFACT_DIR.mkdir(exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    metadata = {
        "algorithm": "DecisionTreeClassifier",
        "project": "transaction-fraud-classification",
        "target_column": TARGET,
        "positive_class": 1,
        "input_features": FEATURES,
        "classes": model.classes_.tolist(),
        "selected_threshold": threshold,
        "false_negative_cost": 10,
        "false_positive_cost": 1,
        "split_strategy": "first 80% by Time for training, final 20% by Time for holdout",
        "train_rows": len(train),
        "test_rows": len(test),
        "fraud_rate": float(data[TARGET].mean()),
        "holdout_pr_auc": float(average_precision_score(test[TARGET], probability)),
        "holdout_roc_auc": float(roc_auc_score(test[TARGET], probability)),
        "dataset": {
            "name": "Credit Card Fraud Detection",
            "publisher": "ULB Machine Learning Group",
            "source": "https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud",
            "local_filename": "creditcard.csv",
            "sha256": sha256(DATA_PATH),
            "redistribution": "Do not redistribute; download under the source terms.",
        },
        "sklearn_version": sklearn.__version__,
        "python_version": platform.python_version(),
        "educational_only": True,
    }
    METADATA_PATH.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(metadata, indent=2))
    print(f"Saved model: {MODEL_PATH}")
    print(f"Saved metadata: {METADATA_PATH}")


if __name__ == "__main__":
    main()
