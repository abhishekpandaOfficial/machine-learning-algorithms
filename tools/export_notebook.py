#!/usr/bin/env python3
"""Execute one Jupyter notebook and export the results to HTML and PDF.

The source notebook is never overwritten. The executed copy is temporary;
the published HTML and PDF contain the executed cell outputs.
"""
from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import unquote, urlsplit


MARKDOWN_IMAGE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")


def run(command: list[str], cwd: Path | None = None) -> None:
    print("\n> " + " ".join(command), flush=True)
    subprocess.run(command, check=True, cwd=cwd)


def embed_local_markdown_images(notebook: Path, source_dir: Path) -> None:
    """Embed local Markdown images as notebook attachments before export.

    Exported files may live in a different directory from the source notebook,
    so leaving relative image URLs unchanged produces broken HTML and PDF
    images. Attachments keep both exports self-contained.
    """
    document = json.loads(notebook.read_text(encoding="utf-8"))

    for cell_index, cell in enumerate(document.get("cells", [])):
        if cell.get("cell_type") != "markdown":
            continue

        markdown = "".join(cell.get("source", []))

        def replace_image(match: re.Match[str]) -> str:
            alt_text, raw_target = match.groups()
            target = raw_target.strip()

            # Preserve optional Markdown image titles while resolving the path.
            path_text = target
            if target.startswith("<") and ">" in target:
                path_text = target[1:target.index(">")]
            elif " " in target:
                path_text = target.split(" ", 1)[0]

            parsed = urlsplit(path_text)
            if parsed.scheme or path_text.startswith(("data:", "attachment:", "#")):
                return match.group(0)

            image_path = (source_dir / unquote(parsed.path)).resolve()
            if not image_path.is_file():
                raise FileNotFoundError(
                    f"Markdown image not found: {path_text} "
                    f"(resolved to {image_path})"
                )

            media_type = mimetypes.guess_type(image_path.name)[0]
            if not media_type or not media_type.startswith("image/"):
                raise ValueError(f"Unsupported Markdown image type: {image_path}")

            attachment_name = f"image-{cell_index}-{image_path.name}"
            encoded = base64.b64encode(image_path.read_bytes()).decode("ascii")
            cell.setdefault("attachments", {})[attachment_name] = {
                media_type: encoded
            }
            return f"![{alt_text}](attachment:{attachment_name})"

        updated = MARKDOWN_IMAGE.sub(replace_image, markdown)
        cell["source"] = updated.splitlines(keepends=True)

    notebook.write_text(
        json.dumps(document, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Execute a notebook and export coloured HTML and PDF files."
    )
    parser.add_argument("notebook", type=Path, help="Path to the .ipynb file")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Output directory (default: project root beside the notebook)",
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
        else notebook.parent
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
            ], cwd=notebook.parent)

            embed_local_markdown_images(executed, notebook.parent)

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
