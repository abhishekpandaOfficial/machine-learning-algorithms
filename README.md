<div align="center">

<img src="assets/ml-algorithms-logo.svg" alt="Machine Learning Algorithms" width="900">

# Machine Learning Algorithms

### A structured, reproducible learning laboratory for machine learning

<p>
  <a href="https://github.com/abhishekpandaOfficial/machine-learning-algorithms/stargazers"><img src="https://img.shields.io/github/stars/abhishekpandaOfficial/machine-learning-algorithms?style=for-the-badge&logo=github&label=Stars" alt="GitHub stars"></a>
  <a href="https://github.com/abhishekpandaOfficial/machine-learning-algorithms/network/members"><img src="https://img.shields.io/github/forks/abhishekpandaOfficial/machine-learning-algorithms?style=for-the-badge&logo=github&label=Forks" alt="GitHub forks"></a>
  <a href="https://github.com/abhishekpandaOfficial/machine-learning-algorithms"><img src="https://img.shields.io/badge/status-active-16a34a?style=for-the-badge" alt="Repository status"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-educational-blue?style=for-the-badge" alt="Educational license"></a>
</p>

<p>
  <a href="https://colab.research.google.com/github/abhishekpandaOfficial/machine-learning-algorithms"><img src="https://img.shields.io/badge/Open%20in-Colab-F9AB00?style=for-the-badge&logo=googlecolab&logoColor=white" alt="Open repository in Google Colab"></a>
  <a href="https://share.streamlit.io/user/abhishekpandaofficial"><img src="https://img.shields.io/badge/Streamlit-Demos-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit demos"></a>
  <a href="#mlflow-experiment-links"><img src="https://img.shields.io/badge/MLflow-Tracking%20Links-0194E2?style=for-the-badge&logo=mlflow&logoColor=white" alt="MLflow tracking links"></a>
</p>

</div>

> **Repository mission:** explain the mathematics, implement the algorithms, measure model behaviour, package reusable artifacts, and document the path from notebook to application.

## Table of contents

- [Repository at a glance](#repository-at-a-glance)
- [Learning map](#learning-map)
- [Algorithm catalogue](#algorithm-catalogue)
- [Completed projects](#completed-projects)
- [Project deliverables](#project-deliverables)
- [Notebook and platform links](#notebook-and-platform-links)
- [Technology stack](#technology-stack)
- [Reproducible setup](#reproducible-setup)
- [Quality and engineering standards](#quality-and-engineering-standards)
- [MLflow experiment links](#mlflow-experiment-links)
- [Responsible use](#responsible-use)
- [Roadmap](#roadmap)
- [Contributing](#contributing)

## Repository at a glance

| Area | Purpose | Status |
|---|---|---|
| [Supervised ML](Supervised-ML/README.md) | Learn from labelled examples | Active |
| [Classification](Supervised-ML/Classification/README.md) | Predict classes or class probabilities | Active |
| [Regression](Supervised-ML/Regression/README.md) | Predict continuous outcomes | Foundation |
| [Unsupervised ML](Unsupervised-ML/README.md) | Discover structure without labels | Planned |
| [Semi-Supervised ML](Semi-Supervised-ML/README.md) | Combine labelled and unlabelled data | Planned |
| [Reinforcement Learning](Reinforcement-Learning/README.md) | Learn policies from rewards | Planned |
| [HTML and PDF library](Algo-HTMLs/README.md) · [PDFs](Algo-PDFs/README.md) | Read and print executed chapters | Published |

## Learning map

```text
Machine Learning Algorithms
├── Supervised-ML
│   ├── Classification
│   │   ├── Logistic-Regression
│   │   └── Decision-Tree
│   └── Regression
├── Unsupervised-ML
├── Semi-Supervised-ML
└── Reinforcement-Learning
```

The folder structure is intentionally modular: each algorithm track owns its domain projects, notebooks, applications, artifacts, tests, and learning exports. Future algorithms can be added without moving existing projects or breaking links.

## Algorithm catalogue

### Supervised learning

| Family | Algorithms | Track |
|---|---|---|
| Classification | Logistic Regression, Decision Tree, k-Nearest Neighbors, Naive Bayes, Support Vector Machine, Random Forest, Gradient Boosting | [Classification](Supervised-ML/Classification/README.md) |
| Regression | Linear Regression, Ridge, Lasso, Elastic Net, Decision Tree Regressor, Random Forest Regressor, Gradient Boosting Regressor | [Regression](Supervised-ML/Regression/README.md) |

### Unsupervised learning

| Family | Algorithms and methods | Track |
|---|---|---|
| Clustering | k-Means, Hierarchical Clustering, DBSCAN, Gaussian Mixture Models | [Unsupervised ML](Unsupervised-ML/README.md) |
| Representation | PCA, factor analysis, manifold learning | [Unsupervised ML](Unsupervised-ML/README.md) |
| Anomaly detection | Isolation Forest, Local Outlier Factor, autoencoders | [Unsupervised ML](Unsupervised-ML/README.md) |
| Association | Apriori and association-rule mining | [Unsupervised ML](Unsupervised-ML/README.md) |

### Semi-supervised learning

Self-training, pseudo-labelling, label propagation, label spreading, consistency regularisation, and semi-supervised SVM are catalogued in [Semi-Supervised-ML](Semi-Supervised-ML/README.md).

### Reinforcement learning

Multi-armed bandits, Q-Learning, SARSA, Deep Q-Networks, policy gradients, and actor-critic methods are catalogued in [Reinforcement-Learning](Reinforcement-Learning/README.md).

## Completed projects

| Algorithm | Project | Notebook | Colab | App and tracking |
|---|---|---|---|---|
| Logistic Regression | [Credit Card Default](Supervised-ML/Classification/Logistic-Regression/01-credit-card-default/README.md) | [Notebook](Supervised-ML/Classification/Logistic-Regression/01-credit-card-default/logistic_regression_enterprise.ipynb) | [Open](https://colab.research.google.com/github/abhishekpandaOfficial/machine-learning-algorithms/blob/master/Supervised-ML/Classification/Logistic-Regression/01-credit-card-default/logistic_regression_enterprise.ipynb) | [Streamlit profile](https://share.streamlit.io/user/abhishekpandaofficial) · [MLflow placeholder](#mlflow-experiment-links) |
| Logistic Regression | [Insurance Fraud Detection](Supervised-ML/Classification/Logistic-Regression/02-insurance-fraud-detection/README.md) | [Notebook](Supervised-ML/Classification/Logistic-Regression/02-insurance-fraud-detection/insurance_logistic_regression.ipynb) | [Open](https://colab.research.google.com/github/abhishekpandaOfficial/machine-learning-algorithms/blob/master/Supervised-ML/Classification/Logistic-Regression/02-insurance-fraud-detection/insurance_logistic_regression.ipynb) | [Streamlit profile](https://share.streamlit.io/user/abhishekpandaofficial) · [MLflow placeholder](#mlflow-experiment-links) |
| Decision Tree | [Telecom Customer Churn](Supervised-ML/Classification/Decision-Tree/01-telecom-customer-churn/README.md) | [Notebook](Supervised-ML/Classification/Decision-Tree/01-telecom-customer-churn/decision_tree_churn.ipynb) | [Open](https://colab.research.google.com/github/abhishekpandaOfficial/machine-learning-algorithms/blob/master/Supervised-ML/Classification/Decision-Tree/01-telecom-customer-churn/decision_tree_churn.ipynb) | [Streamlit profile](https://share.streamlit.io/user/abhishekpandaofficial) · [MLflow placeholder](#mlflow-experiment-links) |
| Decision Tree | [Transaction Fraud Classification](Supervised-ML/Classification/Decision-Tree/02-transaction-fraud-classification/README.md) | [Notebook](Supervised-ML/Classification/Decision-Tree/02-transaction-fraud-classification/decision_tree_fraud.ipynb) | [Open](https://colab.research.google.com/github/abhishekpandaOfficial/machine-learning-algorithms/blob/master/Supervised-ML/Classification/Decision-Tree/02-transaction-fraud-classification/decision_tree_fraud.ipynb) | [Streamlit profile](https://share.streamlit.io/user/abhishekpandaofficial) · [MLflow placeholder](#mlflow-experiment-links) |

## Project deliverables

Every completed project is designed as a compact learning product:

- 📘 Theory, intuition, mathematics, assumptions, and limitations
- 🧪 Reproducible preprocessing and model-training pipeline
- 📊 Evaluation with metrics, visualisations, threshold analysis, and error review
- 💾 Version-pinned artifacts, metadata, and reload checks
- 🖥️ Streamlit application for interactive demonstration
- 🧰 Tests and contract checks where runtime artifacts require protection
- 🌐 Executed self-contained HTML export
- 🖨️ Printable PDF export

Browse the [HTML library](Algo-HTMLs/README.md) or [PDF library](Algo-PDFs/README.md) for book-oriented versions.

## Notebook and platform links

| Platform | Link | Use |
|---|---|---|
| Google Colab | [Repository launcher](https://colab.research.google.com/github/abhishekpandaOfficial/machine-learning-algorithms) | Run notebooks interactively |
| Streamlit | [Author profile](https://share.streamlit.io/user/abhishekpandaofficial) | Open deployed applications |
| MLflow | [Add tracking workspace URL](#mlflow-experiment-links) | Review experiments after deployment |
| GitHub | [Repository](https://github.com/abhishekpandaOfficial/machine-learning-algorithms) | Source, issues, and version history |

Colab notebooks that depend on local artifacts or data may require running the project from a cloned repository or uploading the required files first.

## Technology stack

### Languages and notebooks

[![Python](https://img.shields.io/badge/Python-3.12.13-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?style=for-the-badge&logo=jupyter&logoColor=white)](https://jupyter.org/)
[![Markdown](https://img.shields.io/badge/Markdown-Documentation-000000?style=for-the-badge&logo=markdown&logoColor=white)](https://www.markdownguide.org/)

### Machine learning and data

[![NumPy](https://img.shields.io/badge/NumPy-2.1.3-013243?style=for-the-badge&logo=numpy&logoColor=white)](https://numpy.org/)
[![pandas](https://img.shields.io/badge/pandas-2.3.3-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![SciPy](https://img.shields.io/badge/SciPy-1.16.3-8CAAE6?style=for-the-badge&logo=scipy&logoColor=white)](https://scipy.org/)
[![scikit--learn](https://img.shields.io/badge/scikit--learn-1.6.1-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-3.11.2-11557C?style=for-the-badge&logo=python&logoColor=white)](https://matplotlib.org/)
[![Seaborn](https://img.shields.io/badge/Seaborn-0.13.2-4C72B0?style=for-the-badge&logo=python&logoColor=white)](https://seaborn.pydata.org/)

### Applications, tracking, and quality

[![Streamlit](https://img.shields.io/badge/Streamlit-1.65.0-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![MLflow](https://img.shields.io/badge/MLflow-3.17.0-0194E2?style=for-the-badge&logo=mlflow&logoColor=white)](https://mlflow.org/)
[![pytest](https://img.shields.io/badge/pytest-8.4.2-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)](https://pytest.org/)
[![Joblib](https://img.shields.io/badge/Joblib-1.6.0-3670A0?style=for-the-badge&logo=python&logoColor=white)](https://joblib.readthedocs.io/)

### Publishing

[![nbconvert](https://img.shields.io/badge/nbconvert-7.17.2-F37626?style=for-the-badge&logo=jupyter&logoColor=white)](https://nbconvert.readthedocs.io/)
[![HTML](https://img.shields.io/badge/HTML-Exports-E34F26?style=for-the-badge&logo=html5&logoColor=white)](Algo-HTMLs/)
[![PDF](https://img.shields.io/badge/PDF-Print%20Exports-EC1C24?style=for-the-badge&logo=adobeacrobatreader&logoColor=white)](Algo-PDFs/)

Exact dependency pins are maintained in [requirements.txt](requirements.txt) and [requirements-lock.txt](requirements-lock.txt).

## Reproducible setup

```bash
git clone https://github.com/abhishekpandaOfficial/machine-learning-algorithms.git
cd machine-learning-algorithms

uv python install 3.12
uv venv --python 3.12 --seed .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Run a project app from the repository root:

```bash
streamlit run Supervised-ML/Classification/Logistic-Regression/01-credit-card-default/app.py
```

Export an executed notebook:

```bash
python tools/export_notebook.py \
  "Supervised-ML/Classification/Decision-Tree/01-telecom-customer-churn/decision_tree_churn.ipynb"
```

Read the [publishing guide](tools/VSCODE_AND_NOTEBOOK_PUBLISHING.md) for notebook kernels, math rendering, HTML, and PDF workflows.

## Quality and engineering standards

- Pin versions when serialized artifacts depend on a library ABI or model format.
- Keep training, preprocessing, and inference in a reproducible pipeline.
- Separate training data, artifacts, application code, and tests.
- Prefer precision-recall analysis for rare-event classification.
- Check leakage, calibration, threshold choice, drift, and subgroup behaviour.
- Validate notebooks, Markdown links, exports, and artifact contracts before publishing.
- Treat fraud, credit, and churn outputs as educational decision-support examples.

## MLflow experiment links

MLflow links are intentionally left as deployment placeholders until tracking servers are provisioned:

| Project | Tracking URI | Status |
|---|---|---|
| Credit Card Default | `ADD_MLFLOW_URL` | To be added |
| Insurance Fraud Detection | `ADD_MLFLOW_URL` | To be added |
| Telecom Customer Churn | `ADD_MLFLOW_URL` | To be added |
| Transaction Fraud Classification | `ADD_MLFLOW_URL` | To be added |

## Responsible use

These projects are educational. They must not be used as the sole basis for credit decisions, insurance claim decisions, fraud accusations, employment decisions, or other consequential outcomes. Real deployments require governance, consent, privacy review, fairness analysis, monitoring, human oversight, and domain validation.

## Roadmap

- Add regression implementations and datasets.
- Add clustering, dimensionality-reduction, and anomaly-detection chapters.
- Add semi-supervised and reinforcement-learning experiments.
- Publish verified Streamlit application URLs.
- Add MLflow tracking workspace URLs and model registry examples.
- Expand CI to validate notebooks, artifact contracts, links, and exports.

## Contributing

1. Create or update the appropriate taxonomy track.
2. Include theory, assumptions, equations, code, evaluation, limitations, and dataset attribution.
3. Pin dependencies and document any serialized-artifact compatibility requirements.
4. Add or update tests and regenerate reviewed HTML/PDF exports.
5. Run `git diff --check` and confirm all Markdown links resolve.

See the [project standards](Supervised-ML/Classification/README.md) and [publishing guide](tools/VSCODE_AND_NOTEBOOK_PUBLISHING.md) before opening a pull request.
