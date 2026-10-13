# 💸 Decision Tree: Transaction Fraud Classification

## Goal

Build a book-ready, reproducible Decision Tree classification workflow for transaction-level fraud labels, with particular attention to class imbalance, leakage prevention, threshold policy and precision-recall trade-offs.

![Transaction Fraud Classification hero](assets/transaction_fraud_hero.svg)

## Dataset strategy and links

The notebook uses a deterministic synthetic transaction dataset by default so the HTML/PDF exports run without gated downloads. Synthetic labels make this a controlled learning exercise; they are not evidence of real-world fraud-detection performance.

Public datasets for a later, separately reviewed extension:

- [ULB/Kaggle Credit Card Fraud Detection](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud)
- [IEEE-CIS Fraud Detection](https://www.kaggle.com/competitions/ieee-fraud-detection)
- [Fraud Detection Handbook](https://fraud-detection-handbook.github.io/fraud-detection-handbook/)

Before downloading or redistributing any external dataset, verify its provenance, target definition, licence/terms, access requirements and feature leakage risks.

## Project files

- `decision_tree_fraud.ipynb`: complete theory, mathematics, synthetic data generation, EDA, training, evaluation and deployment walkthrough.
- `decision_tree_fraud.html`: browser export of the executed notebook.
- `decision_tree_fraud.pdf`: printable export of the executed notebook.
- `artifacts/`: fitted pipeline and metadata created by the notebook.
- `app.py`: crimson-branded planning interface with guided synthetic-transaction controls and clear no-model disclaimer.
- `requirements.txt` and this README: setup and usage instructions.

## Evaluation covered

The notebook covers stratified splitting, a majority-class baseline, Gini impurity, confusion matrix, accuracy, precision, recall, F1, ROC-AUC, PR-AUC, threshold analysis and an illustrative false-negative/false-positive cost policy. It saves and reloads the complete preprocessing-and-model pipeline.

## Run the planning app

From the repository root:

```bash
source .venv/bin/activate
python -m pip install -r Supervised-ML/Classification/Decision-Tree/02-transaction-fraud-classification/requirements.txt
streamlit run Supervised-ML/Classification/Decision-Tree/02-transaction-fraud-classification/app.py
```

## Streamlit deployment

The notebook artifact is ready for a reviewed serving layer. Add the deployed URL here after deployment:

**Streamlit apps:** [![Streamlit](assets/streamlit_logo.svg)](https://share.streamlit.io/user/abhishekpandaofficial)

Profile and app directory: [https://share.streamlit.io/user/abhishekpandaofficial](https://share.streamlit.io/user/abhishekpandaofficial)

The current `app.py` remains planning-only until its input contract, artifact loading, safety copy and tests are updated for the saved model.

## Final review checklist

- [x] Theory and Decision Tree mathematics are explained.
- [x] Synthetic dataset generation is deterministic and reproducible.
- [x] Public dataset links and licensing cautions are documented.
- [x] Leakage prevention and stratified splitting are demonstrated.
- [x] Baseline and rare-event metrics are reported.
- [x] Threshold and cost assumptions are explicit.
- [x] Model and metadata artifacts are saved and reloaded.
- [ ] Validate on an approved real dataset with time-based evaluation.
- [ ] Complete privacy, fairness, governance and security review.
- [ ] Add and test the deployed Streamlit URL.
