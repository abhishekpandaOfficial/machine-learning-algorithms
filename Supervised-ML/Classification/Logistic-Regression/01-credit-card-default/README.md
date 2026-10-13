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

Dataset link: [UCI Default of Credit Card Clients](https://archive.ics.uci.edu/dataset/350/defaultofcreditcardclients).

Review the UCI terms before redistributing the data or presenting model results outside this educational project.

**Note:** This project is for educational purposes and is not a production credit decision system.

## Run the app

From the repository root:

```bash
source .venv/bin/activate
python -m pip install -r Supervised-ML/Classification/Logistic-Regression/01-credit-card-default/requirements.txt
streamlit run Supervised-ML/Classification/Logistic-Regression/01-credit-card-default/app.py
```

## Streamlit deployment

**Streamlit apps:** [![Streamlit](assets/streamlit_logo.svg)](https://share.streamlit.io/user/abhishekpandaofficial)

Profile and app directory: [https://share.streamlit.io/user/abhishekpandaofficial](https://share.streamlit.io/user/abhishekpandaofficial)

## Book checklist

- [x] Logistic function, log-odds and cross-entropy are explained.
- [x] Dataset source, evaluation metrics and threshold limitations are documented.
- [x] HTML/PDF exports are stored in the root `Algo-HTMLs/` and `Algo-PDFs/` collections.
- [ ] Validate current data, fairness, governance and deployment monitoring.
