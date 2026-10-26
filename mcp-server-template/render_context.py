"""Render the same source context for human readers."""

import argparse
from pathlib import Path

from context_loader import DEFAULT_CONTEXT, LoadedContext


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    output = Path(__file__).resolve().parent / "CONTEXT_GUIDE.md"
    expected = LoadedContext(DEFAULT_CONTEXT).render()
    if args.check:
        if not output.exists() or output.read_text() != expected:
            raise SystemExit("CONTEXT_GUIDE.md is stale; run python render_context.py")
        print("Human context guide matches source")
    else:
        output.write_text(expected)
        print("Rendered CONTEXT_GUIDE.md")


if __name__ == "__main__":
    main()
