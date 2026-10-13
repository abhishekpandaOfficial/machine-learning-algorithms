# Transaction Fraud Lab dataset

This project uses the **Credit Card Fraud Detection** dataset published by the
ULB Machine Learning Group through Kaggle:

<https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud>

The dataset contains anonymised PCA features (`V1`–`V28`), transaction time,
amount, and the binary `Class` target. It is a real historical dataset, not a
synthetic generator. The fraud class is highly imbalanced, so the project uses
a time-ordered holdout and reports PR-AUC in addition to ROC-AUC.

## Download

```bash
curl -L -o /tmp/creditcard.zip \
  https://www.kaggle.com/api/v1/datasets/download/mlg-ulb/creditcardfraud
unzip -o /tmp/creditcard.zip -d \
  Supervised-ML/Classification/Decision-Tree/02-transaction-fraud-classification/data
```

The raw CSV is intentionally ignored by Git because it is large and must be
obtained under the dataset publisher's current access and redistribution terms.
After downloading, verify the SHA-256 recorded in `artifacts/model_metadata.json`
when reproducing the published model.
