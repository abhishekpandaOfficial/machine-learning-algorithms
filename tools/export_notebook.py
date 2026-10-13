#!/usr/bin/env python3
"""Execute one Jupyter notebook and export the results to HTML and PDF.

The source notebook is never overwritten. The executed copy is temporary;
the published HTML and PDF contain the executed cell outputs.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path


def run(command: list[str]) -> None:
    print("\n> " + " ".join(command), flush=True)
    subprocess.run(command, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Execute a notebook and export coloured HTML and PDF files."
    )
    parser.add_argument("notebook", type=Path, help="Path to the .ipynb file")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Output directory (default: docs beside the notebook)",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=600,
        help="Maximum seconds allowed for each cell (default: 600)",
    )
    args = parser.parse_args()

    notebook = args.notebook.resolve()
    if not notebook.is_file() or notebook.suffix.lower() != ".ipynb":
        print(f"ERROR: Notebook not found or not an .ipynb file: {notebook}", file=sys.stderr)
        return 2

    output_dir = (
        args.output_dir.resolve()
        if args.output_dir
        else notebook.parent / "docs"
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = notebook.stem

    try:
        with tempfile.TemporaryDirectory(prefix="ml-notebook-export-") as temp:
            temp_dir = Path(temp)
            executed = temp_dir / f"{stem}.executed.ipynb"

            run([
                sys.executable, "-m", "jupyter", "nbconvert",
                "--to", "notebook",
                "--execute", str(notebook),
                "--output", executed.name,
                "--output-dir", str(temp_dir),
                f"--ExecutePreprocessor.timeout={args.timeout}",
            ])

            run([
                sys.executable, "-m", "jupyter", "nbconvert",
                "--to", "html", "--template", "lab", str(executed),
                "--output", f"{stem}.html",
                "--output-dir", str(output_dir),
            ])

            # webpdf requires Playwright/Chromium. Install with:
            # python -m pip install "nbconvert[webpdf]"
            # python -m playwright install chromium
            run([
                sys.executable, "-m", "jupyter", "nbconvert",
                "--to", "webpdf", "--template", "lab", str(executed),
                "--allow-chromium-download",
                "--output", f"{stem}.pdf",
                "--output-dir", str(output_dir),
            ])

    except subprocess.CalledProcessError as exc:
        print(
            "\nEXPORT FAILED. Read the first error above, install the notebook's "
            "requirements, fix the failing cell, and run this command again. "
            "The source notebook was not overwritten.",
            file=sys.stderr,
        )
        return exc.returncode or 1

    print(f"\nExport complete. Files saved in: {output_dir}")
    print(f"  - {output_dir / (stem + '.html')}")
    print(f"  - {output_dir / (stem + '.pdf')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
