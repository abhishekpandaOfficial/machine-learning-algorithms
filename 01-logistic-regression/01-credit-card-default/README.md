# Logistic Regression

**Goal:** Predict whether a customer will default on a credit card payment.

## Project files

- `logistic_regression_enterprise.ipynb` — Step-by-step explanation, mathematics, implementation, and evaluation.
- `logistic_regression_enterprise.html` — Self-contained browser export.
- `logistic_regression_enterprise.pdf` — Printable notebook export.
- `app.py` — Streamlit demonstration using the saved model artifacts.
- `artifacts/` — Saved pipeline, threshold and model metadata.
- `requirements.txt` — Project dependencies.

## Topics
- Logistic function and probability
- Binary cross-entropy loss
- Data preprocessing
- Model training and evaluation
- Coefficient interpretation
- Decision threshold tuning

## Dataset
UCI Default of Credit Card Clients dataset.

**Note:** This project is for educational purposes and is not a production credit decision system.

## Run the app

From the repository root:

```bash
source .venv/bin/activate
python -m pip install -r 01-logistic-regression/01-credit-card-default/requirements.txt
streamlit run 01-logistic-regression/01-credit-card-default/app.py
```
