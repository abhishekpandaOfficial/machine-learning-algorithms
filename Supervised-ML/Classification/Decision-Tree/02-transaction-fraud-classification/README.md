# 💸 Decision Tree: Transaction Fraud Classification

## Goal

Build a book-ready, reproducible Decision Tree classification workflow for transaction-level fraud labels, with particular attention to class imbalance, leakage prevention, threshold policy and precision-recall trade-offs.

![Transaction Fraud Classification hero](assets/transaction_fraud_hero.svg)

## Real dataset and provenance

The notebook and serving app now use the real [Credit Card Fraud Detection
dataset](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud) published by
the ULB Machine Learning Group. It contains 284,807 historical transactions,
anonymised PCA features `V1`–`V28`, `Time`, `Amount`, and the binary `Class`
target. The fraud rate is below 0.2%, so PR-AUC, recall, precision and
threshold analysis are more informative than accuracy alone.

The raw 144 MB CSV is deliberately ignored by Git. Download instructions,
publisher attribution and redistribution guidance are in [`data/README.md`](data/README.md).

## Project files

- `decision_tree_fraud.ipynb`: complete theory, mathematics, real-data audit, time-ordered training, evaluation and deployment walkthrough.
- `train_model.py`: repeatable training entry point that records the dataset SHA-256 and holdout metrics.
- `decision_tree_fraud.html`: browser export of the executed notebook.
- `decision_tree_fraud.pdf`: printable export of the executed notebook.
- `artifacts/`: fitted pipeline and metadata created by the notebook.
- `app.py`: crimson-branded serving interface using the saved real-data model and explicit human-review disclaimer.
- `requirements.txt` and this README: setup and usage instructions.

## Evaluation covered

The notebook covers stratified splitting, a majority-class baseline, Gini impurity, confusion matrix, accuracy, precision, recall, F1, ROC-AUC, PR-AUC, threshold analysis and an illustrative false-negative/false-positive cost policy. It saves and reloads the complete preprocessing-and-model pipeline.

## Train and run the real-data app

From the repository root:

```bash
source .venv/bin/activate
python -m pip install -r Supervised-ML/Classification/Decision-Tree/02-transaction-fraud-classification/requirements.txt
streamlit run Supervised-ML/Classification/Decision-Tree/02-transaction-fraud-classification/app.py
```

To retrain after downloading the dataset:

```bash
python Supervised-ML/Classification/Decision-Tree/02-transaction-fraud-classification/train_model.py
```

## Streamlit deployment

The serving app loads a trained artifact and displays a review signal. Add the deployed URL here after deployment:

**Streamlit apps:** [![Streamlit](assets/streamlit_logo.svg)](https://share.streamlit.io/user/abhishekpandaofficial)

Profile and app directory: [https://share.streamlit.io/user/abhishekpandaofficial](https://share.streamlit.io/user/abhishekpandaofficial)

The app is an educational demonstration. Its anonymised PCA inputs are not a substitute for a production feature contract or transaction-governance process.

## Final review checklist

- [x] Theory and Decision Tree mathematics are explained.
- [x] Real ULB/Kaggle dataset provenance and download instructions are documented.
- [x] Dataset checksum and time-ordered holdout are recorded in model metadata.
- [x] Leakage prevention and stratified splitting are demonstrated.
- [x] Baseline and rare-event metrics are reported.
- [x] Threshold and cost assumptions are explicit.
- [x] Model and metadata artifacts are saved and reloaded.
- [x] Train and validate a Decision Tree on the approved real dataset.
- [ ] Complete privacy, fairness, governance and security review.
- [ ] Add the deployed Streamlit URL.
