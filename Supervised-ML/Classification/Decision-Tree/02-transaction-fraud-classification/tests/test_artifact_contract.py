import json
from pathlib import Path

import joblib


ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "artifacts" / "transaction_fraud_tree_pipeline.joblib"
METADATA_PATH = ROOT / "artifacts" / "model_metadata.json"


def test_real_dataset_metadata_contract():
    metadata = json.loads(METADATA_PATH.read_text(encoding="utf-8"))

    assert metadata["dataset"]["publisher"] == "ULB Machine Learning Group"
    assert metadata["dataset"]["name"] == "Credit Card Fraud Detection"
    assert metadata["split_strategy"].startswith("first 80% by Time")
    assert metadata["train_rows"] > 200_000
    assert metadata["test_rows"] > 50_000
    assert 0 < metadata["holdout_pr_auc"] < 1
    assert 0 < metadata["holdout_roc_auc"] < 1


def test_real_data_artifact_round_trip():
    model = joblib.load(MODEL_PATH)
    metadata = json.loads(METADATA_PATH.read_text(encoding="utf-8"))

    assert list(model.classes_) == metadata["classes"]
    assert len(metadata["input_features"]) == 30
