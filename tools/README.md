# Notebook publishing: HTML + PDF

This repository uses Jupyter notebooks as the main learning format. A published notebook should contain theory, equations, commented code, charts, and saved cell outputs.

## What the exporter does

`export_notebook.py`:
1. Executes the notebook from top to bottom in a temporary copy.
2. Writes an HTML version with syntax highlighting and outputs.
3. Writes a PDF version using nbconvert's WebPDF exporter.
4. Never overwrites the source notebook.

If notebook execution fails, fix the first failing cell or its dependencies before publishing. Do not hide errors just to create an export.

## One-time setup (inside your project's virtual environment)

Run from the repository root:

```bash
python -m pip install --upgrade pip
python -m pip install "nbconvert[webpdf]" jupyter
python -m playwright install chromium
```

Also install the requirements for the project whose notebook you are exporting. For example, activate that project's environment and install its `requirements.txt` first.

## Export one notebook

Run from the repository root, replacing the path with the notebook you want to publish:

```bash
python tools/export_notebook.py "PATH/TO/YOUR_NOTEBOOK.ipynb"
```

By default, the HTML and PDF are saved in a `docs/` folder beside the notebook. To choose a different destination:

```bash
python tools/export_notebook.py "PATH/TO/YOUR_NOTEBOOK.ipynb" --output-dir "PATH/TO/docs"
```

The first run can take time because the notebook is executed and Chromium may need to be installed. Cell execution has a default timeout of 600 seconds; change it with `--timeout 1200` for a notebook with longer-running cells.

## Publishing checklist

- Run the notebook in a clean environment and review all outputs.
- Check that plots, tables, formulas, and code fit in the HTML and PDF.
- Check that no private data, credentials, tokens, or local machine paths are included.
- Check PDF pagination before printing.
- Commit the source notebook and the reviewed HTML/PDF exports to GitHub if you want them available as public downloads.
- Rebuild exports whenever the notebook's content or results change.

## Important limitations

- This tool executes notebook cells; it does not repair broken code, missing datasets, expired external URLs, or environment-specific paths.
- PDF export requires a working Playwright/Chromium installation.
- Syntax colours depend on the notebook's HTML/PDF rendering and the viewer or printer settings.
- A public GitHub repository makes committed files public. Only publish datasets and model artifacts that you are allowed to redistribute.
