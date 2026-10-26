"""Copy this template without virtual environments or generated caches."""

import argparse
import shutil
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "destination", type=Path, help="A new folder; existing folders are preserved"
    )
    args = parser.parse_args()
    source = Path(__file__).resolve().parent
    destination = args.destination.expanduser().resolve()
    if destination.is_relative_to(source):
        parser.error("Choose a destination outside the template folder")
    if destination.exists():
        parser.error("Destination already exists; choose a new folder to preserve its files")
    shutil.copytree(
        source,
        destination,
        ignore=shutil.ignore_patterns(
            ".venv", "__pycache__", ".pytest_cache", ".ruff_cache", ".DS_Store", ".git"
        ),
    )
    print(f"Copied template to {destination}")
    print("Open that folder in your editor and follow its README.md")


if __name__ == "__main__":
    main()
