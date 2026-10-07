#!/usr/bin/env python3
"""Fail fast with actionable setup diagnostics."""

from pathlib import Path

from jeopardy_template.adapter import load_clues, load_manifest_version


def main() -> None:
    data_path = Path("data/clues.json")
    manifest_path = Path("data/manifest.json")
    clues = load_clues(data_path)
    version = load_manifest_version(manifest_path)
    print(f"setup ready: {len(clues)} clues, {version}")


if __name__ == "__main__":
    main()
