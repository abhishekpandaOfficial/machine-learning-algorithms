# Logistic Regression: Insurance Fraud Detection

## Goal

Teach binary classification with Logistic Regression using insurance claim data. This is an educational demonstration and must not be used as proof of fraud or for automated claim decisions.

## Project files

- `insurance_logistic_regression.ipynb` - Training workflow, explanations, evaluation and saved outputs.
- `insurance_logistic_regression.html` - Self-contained browser export.
- `insurance_logistic_regression.pdf` - Printable notebook export.
- `app.py` - Streamlit demonstration using the saved model artifacts.
- `artifacts/` - Saved pipeline, threshold and model metadata.
- `tests/` - Application contract tests.
- `requirements.txt` - Project dependencies.

## Run locally

From the repository root, activate the shared Python 3.12 environment and run the notebook or app:

```bash
source .venv/bin/activate
python -m pip install -r 01-logistic-regression/02-insurance-fraud-detection/requirements.txt
jupyter lab 01-logistic-regression/02-insurance-fraud-detection/insurance_logistic_regression.ipynb
streamlit run 01-logistic-regression/02-insurance-fraud-detection/app.py
```

Review the model limitations, data provenance and error trade-offs before sharing any result.
