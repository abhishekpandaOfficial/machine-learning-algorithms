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

The book chapter also explains Gini impurity, information gain, tree complexity, class metrics and responsible interpretation.

## Project files

- `decision_tree_churn.ipynb`: theory, equations, EDA, commented training code, evaluation, outputs and interpretation.
- `decision_tree_churn.html`: self-contained browser export with embedded images and saved outputs.
- `decision_tree_churn.pdf`: reviewed printable export.
- `src/`: reusable data checks, training and evaluation.
- `artifacts/`: fitted pipeline and metadata created by the training workflow.
- `tests/`: preprocessing, prediction and artifact-loading tests.
- `app.py`: crimson-branded Streamlit prediction, batch-scoring and model-guide UI.
- `requirements.txt` and this README: reproducible setup and usage instructions.

## Planned evaluation

Use a stratified split and compare against a simple baseline. Report confusion matrix, precision, recall, F1, ROC-AUC and PR-AUC as appropriate; explain the trade-offs rather than presenting accuracy alone. Exclude identifiers from model inputs and check for leakage.

## Run the app

From the repository root:

```bash
source .venv/bin/activate
python -m pip install -r Supervised-ML/Classification/Decision-Tree/01-telecom-customer-churn/requirements.txt
streamlit run Supervised-ML/Classification/Decision-Tree/01-telecom-customer-churn/app.py
```

## Streamlit deployment

**Streamlit apps:** [![Streamlit](images/streamlit_logo.svg)](https://share.streamlit.io/user/abhishekpandaofficial)

Profile and app directory: [https://share.streamlit.io/user/abhishekpandaofficial](https://share.streamlit.io/user/abhishekpandaofficial)

## Book checklist

- [x] Decision Tree theory, Gini impurity and information gain are explained.
- [x] Dataset source, licensing cautions and leakage controls are documented.
- [x] HTML/PDF exports are stored in the root `Algo-HTMLs/` and `Algo-PDFs/` collections.
- [ ] Validate current data, fairness, governance and deployment monitoring.

## Status

The notebook executes successfully with Python 3.12 and its HTML/PDF exports are generated. The application, automated tests, dataset redistribution terms and public deployment still require separate verification.
