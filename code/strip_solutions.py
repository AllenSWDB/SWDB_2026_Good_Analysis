#!/usr/bin/env python3
"""Clear outputs and blank out '#:' solution snippets in a notebook.

Usage: python strip_solutions.py path/to/notebook.ipynb [more.ipynb ...] [-o output_dir] [-f]
"""

import argparse
import json
import os


def strip_markers(lines):
    """Blank out everything between a '#:' comment and the next comment line."""
    out = []
    i = 0
    while i < len(lines):
        line = lines[i]
        out.append(line)
        if line.strip().startswith("#:"):
            j = i + 1
            while j < len(lines) and not lines[j].strip().startswith("#"):
                j += 1
            out.append("\n")
            i = j
        else:
            i += 1
    return out


def process_notebook(input_path, output_path):
    with open(input_path) as f:
        nb = json.load(f)

    for cell in nb["cells"]:
        if cell["cell_type"] != "code":
            continue
        cell["outputs"] = []
        cell["execution_count"] = None
        source = cell["source"]
        text = "".join(source) if isinstance(source, list) else source
        cell["source"] = strip_markers(text.splitlines(keepends=True))

    with open(output_path, "w") as f:
        json.dump(nb, f, indent=1)
        f.write("\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("notebooks", nargs="+", help="Path(s) to the input notebook(s)")
    parser.add_argument(
        "-o", "--output-dir", default=".",
        help="Path to write the result",
    )
    parser.add_argument(
        "-f", "--force", action="store_true",
        help="Overwrite the output file if it already exists",
    )
    args = parser.parse_args()

    for notebook in args.notebooks:
        output_path = os.path.join(args.output_dir, os.path.basename(notebook))
        if os.path.exists(output_path) and not args.force:
            parser.error(f"{output_path} already exists; pass -f/--force to overwrite it")
        process_notebook(notebook, output_path)


if __name__ == "__main__":
    main()
