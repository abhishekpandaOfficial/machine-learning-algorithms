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

## 3. Create the shared Python 3.12 environment

From the repository root (install [uv](https://docs.astral.sh/uv/) if needed):

```bash
uv python install 3.12
uv venv --python 3.12 --seed .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m ipykernel install --user --name machine-learning-algorithms --display-name "Python 3.12 (Machine Learning Algorithms)"
```

For an exact reinstall on this Mac, use `python -m pip install -r requirements-lock.txt`. The lock records the installed package versions.

The root `.python-version` selects Python 3.12. Use one root `.venv` for all projects; the root requirements file includes each project's dependencies. Python 3.13 is also supported: recreate the environment with `uv venv --python 3.13 --seed .venv`, reinstall dependencies, and register its kernel with a matching display name. Do not reuse a venv across Python versions.

## 4. Select the notebook kernel and render equations

Install the recommended Python and Jupyter extensions. Workspace settings point to `${workspaceFolder}/.venv/bin/python`. Open a notebook, click **Select Kernel**, and choose **Python 3.12 (Machine Learning Algorithms)** or the root `.venv` interpreter. Previously selected kernels may need to be changed manually.

Use `$X$` for inline math and standalone `$$` lines for display math in Markdown cells:

```markdown
For class proportions $p_k$:

$$
G(t) = 1 - \sum_{k=1}^{K} p_k^2
$$
```

Run a Markdown cell to render it in Jupyter. For `.md` files, open VS Code's Markdown preview; `markdown.math.enabled` is enabled in workspace settings. A system LaTeX installation is not required for notebook HTML or WebPDF exports.

## 5. Execute and inspect

Use **Run All**. Read all Markdown cells and inspect the outputs. Resolve any cell error; do not hide or skip it. Save the notebook after successful execution so its cells retain output. If training/data download requires Internet, run with an approved connection and document the data source and terms. Do not commit the raw dataset unless its terms permit it.

## 6. Create polished HTML and PDF

From the repository root:

```bash
python tools/export_notebook.py "02-decision-tree/01-telecom-customer-churn/decision_tree_churn.ipynb"
```

The script executes a temporary copy (source notebook is not overwritten), then creates:
- `02-decision-tree/01-telecom-customer-churn/decision_tree_churn.html`
- `02-decision-tree/01-telecom-customer-churn/decision_tree_churn.pdf`

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
- Copy reviewed HTML exports into `Algo-HTMLs/<algorithm>/` and reviewed PDF exports into `Algo-PDFs/<algorithm>/` so all algorithm downloads are collected at the repository root.
- Never claim a deployment is public until the live URL has been tested.
