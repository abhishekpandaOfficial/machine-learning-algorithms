"""Checks that the churn artifact and deployment dependencies stay compatible."""
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_requirements_pin_artifact_sklearn_version():
    requirements = (ROOT / "requirements.txt").read_text(encoding="utf-8")
    metadata = json.loads(
        (ROOT / "artifacts" / "model_metadata.json").read_text(encoding="utf-8")
    )

    assert f"scikit-learn=={metadata['sklearn_version']}" in requirements
