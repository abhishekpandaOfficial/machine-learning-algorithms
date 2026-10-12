"""Lightweight tests for the Streamlit app's input-validation contract."""
import importlib.util
from pathlib import Path
import pandas as pd
import pytest

APP_PATH = Path(__file__).resolve().parents[1] / "app.py"

def test_app_file_exists():
    assert APP_PATH.exists()

def test_requirements_pin_training_sklearn_version():
    req = (APP_PATH.parent / "requirements.txt").read_text()
    assert "scikit-learn==1.6.1" in req

def test_metadata_schema_when_artifacts_exist():
    metadata_path = APP_PATH.parent / "artifacts" / "model_metadata.json"
    if not metadata_path.exists():
        pytest.skip("Run the notebook first to generate artifacts.")
    import json
    metadata = json.loads(metadata_path.read_text())
    assert metadata["target_column"] == "fraud_reported"
    assert metadata["feature_columns"]
    assert metadata["educational_only"] is True
