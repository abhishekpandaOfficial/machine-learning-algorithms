# Machine Learning Algorithms

## Learning taxonomy

The repository is organized for expansion across learning paradigms:

- [Supervised ML](Supervised-ML/README.md)
  - [Classification](Supervised-ML/Classification/README.md)
  - [Regression](Supervised-ML/Regression/README.md)
- [Unsupervised ML](Unsupervised-ML/README.md)
- [Semi-Supervised ML](Semi-Supervised-ML/README.md)
- [Reinforcement Learning](Reinforcement-Learning/README.md)
- [Project templates](templates/README.md)

Existing numbered projects are preserved for compatibility and linked from the Classification track. New projects should use the taxonomy and templates above.

## Existing supervised classification projects

This directory contains two independent Logistic Regression projects in different domains.

## Projects

### 1. Credit Card Default Prediction — Finance

- **Folder:** `01-credit-card-default/`
- Predicts the probability of credit-card default.
- Includes the training notebook, Streamlit app, model artifacts and documentation.

### 2. Insurance Fraud Detection — Insurance

- **Folder:** `02-insurance-fraud-detection/`
- Educational binary-classification example using insurance claims data.
- Includes the training notebook, evaluation graphs, Streamlit app, tests and generated model artifacts.

## Project workflow

Each project has its own dependencies, saved pipeline, threshold, metadata and documentation. Run the relevant notebook to generate that project's model artifacts.

## Important

Both projects are educational demonstrations, not automated systems for making consequential decisions about customers or insurance claimants.


## Learning and notebook downloads

The notebooks are intended to teach the complete machine-learning lifecycle: problem definition, data understanding, preprocessing, train/validation/test splitting, model training, evaluation, experiment tracking, packaging, testing, deployment and monitoring.

For each project, the goal is to provide:
- An explanatory Jupyter notebook with theory, commented code, charts and saved outputs.
- HTML and PDF exports generated from an executed notebook.
- A reproducible training pipeline, tests and a Streamlit demonstration.
- MLflow experiment tracking; DVC when dataset or artifact versioning is warranted.

### Export notebooks to HTML and PDF

See [the notebook publishing guide](tools/README.md) and use the [export script](tools/export_notebook.py). Exports must be generated and reviewed in an environment with the project's dependencies and data available before they are committed as public downloads.

Centralized reviewed exports are also available in:

- [Algo-HTMLs/](Algo-HTMLs/) for browser-readable notebook exports.
- [Algo-PDFs/](Algo-PDFs/) for printable notebook exports.

## Local Python and math setup

Use the shared Python **3.12** environment at the repository root:

```bash
uv python install 3.12
uv venv --python 3.12 --seed .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Select the root `.venv` as your VS Code notebook kernel. Use `$...$` for inline equations and `$$...$$` for display equations. See the [VS Code setup guide](tools/VSCODE_AND_NOTEBOOK_PUBLISHING.md) for kernel registration and rendering instructions.
