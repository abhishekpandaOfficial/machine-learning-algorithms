# Logistic Regression: Insurance Fraud Detection

## Goal

Teach binary classification with Logistic Regression using insurance claim data. This is an educational demonstration and must not be used as proof of fraud or for automated claim decisions.

Dataset links: [Mendeley insurance claims record](https://data.mendeley.com/datasets/992mh7dk9y/2) and [linked CSV repository](https://github.com/mwitiderrick/insurancedata/blob/master/insurance_claims.csv).

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

## Streamlit deployment

**Streamlit app:** `[Add deployed Streamlit URL here]`

## Book checklist

- [x] Logistic regression mathematics, metrics and threshold trade-offs are explained.
- [x] Data provenance, licensing and leakage cautions are documented.
- [x] HTML/PDF exports are stored in the root `Algo-HTMLs/` and `Algo-PDFs/` collections.
- [ ] Validate current data, fairness, governance and deployment monitoring.
