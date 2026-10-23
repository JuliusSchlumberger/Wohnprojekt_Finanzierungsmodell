"""Build the static browser version of the dashboard (Pyodide) into one folder.

Usage: python scripts/build_site.py [--out site]
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# panel convert prepends code to the script, so the entry must not use `from __future__`.
ENTRY = ROOT / "scripts" / "site_entry.py"
TITLE = "Wohnprojekt-Rechner"
# Packages the app imports beyond Panel itself; our own code ships as a local wheel.
RUNTIME_REQUIREMENTS = ["numpy", "pandas", "plotly"]


def run(*command: str) -> None:
    print("+", " ".join(command), flush=True)
    subprocess.run(command, check=True, cwd=ROOT)


def build(out: Path) -> Path:
    """Write index.html, the worker script and our wheel into `out`; return the page."""
    if out.exists():
        shutil.rmtree(out)
    wheels = out / "wheels"
    wheels.mkdir(parents=True)
    run(sys.executable, "-m", "pip", "wheel", ".", "--no-deps", "--wheel-dir", str(wheels))
    (wheel,) = wheels.glob("wohnprojekt_dashboard-*.whl")
    requirements = out / "requirements.txt"
    requirements.write_text(
        "\n".join([*RUNTIME_REQUIREMENTS, f"./wheels/{wheel.name}"]) + "\n", encoding="utf-8"
    )
    run(
        sys.executable,
        "-m",
        "panel",
        "convert",
        str(ENTRY),
        "--to",
        "pyodide-worker",
        "--out",
        str(out),
        "--title",
        TITLE,
        "--requirements",
        str(requirements),
    )
    page = out / "site_entry.html"
    page.replace(out / "index.html")
    requirements.unlink()
    shutil.rmtree(wheels)  # the wheel is packed into main.resources.zip
    return out / "index.html"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", type=Path, default=ROOT / "site", help="output folder")
    args = parser.parse_args()
    page = build(args.out.resolve())
    print(f"built {page}")


if __name__ == "__main__":
    main()
