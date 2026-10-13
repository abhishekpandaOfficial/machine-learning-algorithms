# Visual Studio Code + Beautiful Notebook Exports

This guide sets up a repeatable local workflow for the public repository:
https://github.com/abhishekpandaOfficial/machine-learning-algorithms

## 1. Install the tools

Install these on macOS:
- Visual Studio Code: https://code.visualstudio.com/
- Python 3: https://www.python.org/downloads/macos/
- Git: https://git-scm.com/download/mac

In VS Code, install Microsoft's **Python** and **Jupyter** extensions.

## 2. Open the repository

If you already have a Git clone, open that folder in VS Code and run `git status` before pulling. If you only downloaded a ZIP, that folder is not a Git clone; clone into a new directory instead.

```bash
git clone https://github.com/abhishekpandaOfficial/machine-learning-algorithms.git
cd machine-learning-algorithms
code .
```

Do not run `git clone` inside an existing repository folder.

## 3. Create an isolated Python environment for Decision Tree Project 1

From the repository root:

```bash
cd 02-decision-tree/01-telecom-customer-churn
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m ipykernel install --user --name dt-churn --display-name "Python (Decision Tree - Churn)"
```

If `pip install` fails, keep the full error and stop. Fix dependencies before running the notebook. Return to the repository root for the export command with `cd ../../..`.

## 4. Select the correct notebook kernel

Open `notebooks/decision_tree_churn.ipynb` in VS Code. Click **Select Kernel** at the upper right and choose **Python (Decision Tree - Churn)** (or the interpreter inside this project's `.venv`). This ensures the notebook uses the installed packages.

## 5. Execute and inspect

Use **Run All**. Read all Markdown cells and inspect the outputs. Resolve any cell error; do not hide or skip it. Save the notebook after successful execution so its cells retain output. If training/data download requires Internet, run with an approved connection and document the data source and terms. Do not commit the raw dataset unless its terms permit it.

## 6. Create polished HTML and PDF

From the repository root:

```bash
python tools/export_notebook.py "02-decision-tree/01-telecom-customer-churn/notebooks/decision_tree_churn.ipynb"
```

The script executes a temporary copy (source notebook is not overwritten), then creates:
- `02-decision-tree/01-telecom-customer-churn/notebooks/docs/decision_tree_churn.html`
- `02-decision-tree/01-telecom-customer-churn/notebooks/docs/decision_tree_churn.pdf`

The HTML export supports syntax highlighting and preserves cell outputs. The PDF uses nbconvert's WebPDF renderer (Chromium/Playwright). The first export may need to download Chromium.

## 7. Improve the print result

- Open the HTML export in Chrome and inspect headings, equations, code, plots, and tables.
- For browser printing, use **Print → Save as PDF**, enable background graphics, and check paper size/margins.
- The script's WebPDF output is a separate renderer, so inspect that PDF too. Very wide code/table cells may need wrapping or smaller figure dimensions.
- Keep explanations in Markdown cells rather than screenshots of text. Use plots for concepts, screenshots only when a real interface needs illustration.
- Syntax colours depend on renderer and printer settings. Colour on screen does not guarantee colour output from a monochrome printer.

## 8. Use images responsibly

Prefer self-created Matplotlib diagrams/charts or diagrams that have an explicit licence. Add source/attribution and licence notes for third-party images. Avoid hotlinking images that may disappear. Keep image assets in the relevant project folder and use relative paths so GitHub and notebook exports can find them.

For this Decision Tree project, useful visuals include:
1. a small Gini-impurity plot;
2. a hand-drawn example tree;
3. churn class-distribution chart;
4. confusion matrix;
5. feature-importance chart.

Plots generated in code cells are embedded in saved notebook outputs and therefore appear in exports. For static images, reference a local path relative to the notebook and verify that the export can find it.

## 9. Before publishing

- Restart kernel and Run All to prove reproducibility.
- Confirm saved outputs are present.
- Review data terms and exclude private data, secrets and local absolute paths.
- Check HTML and PDF for missing images, clipped code, broken formulas and page breaks.
- Run tests and verify the Streamlit app separately.
- Commit the source notebook and only reviewed exports.
- Never claim a deployment is public until the live URL has been tested.
