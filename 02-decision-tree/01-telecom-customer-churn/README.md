# Decision Tree: Telecom Customer Churn

## Goal

Teach a Decision Tree Classifier using a public telecom customer churn sample. The model predicts the historical churn label in the dataset; it is an educational classification exercise, not a guarantee of future customer behaviour.

## Candidate dataset

- Publisher/source: IBM sample data repository.
- Dataset description: [IBM telecommunications churn tutorial](https://www.ibm.com/docs/en/ws-and-kc?topic=tutorials-predict-telecommunications-churn)
- Candidate CSV: [Telco-Customer-Churn.csv](https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv)
- Expected target: `Churn` (Yes/No).
- Dataset size commonly described by the source copy: 7,043 customer records and 21 columns.

**Terms check:** The IBM repository describes the code pattern's licence, but that does not automatically establish a separate licence for the dataset. Before redistributing the CSV, verify applicable data terms. The raw dataset will not be committed to this repository by default; the notebook will document how to obtain it from the source.

## Planned deliverables

- `notebooks/decision_tree_churn.ipynb`: theory, equations, EDA, commented training code, evaluation, outputs and interpretation.
- `src/`: reusable data checks, training and evaluation.
- `artifacts/`: fitted pipeline and metadata created by the training workflow.
- `tests/`: preprocessing, prediction and artifact-loading tests.
- `app.py`: polished Streamlit prediction and model-explanation UI.
- `docs/`: reviewed HTML and PDF exports of the executed notebook.
- `requirements.txt` and this README: reproducible setup and usage instructions.

## Planned evaluation

Use a stratified split and compare against a simple baseline. Report confusion matrix, precision, recall, F1, ROC-AUC and PR-AUC as appropriate; explain the trade-offs rather than presenting accuracy alone. Exclude identifiers from model inputs and check for leakage.

## Status

Planning only. Dataset terms, implementation, model metrics, tests, exports and deployment must be verified before this project is marked complete.
