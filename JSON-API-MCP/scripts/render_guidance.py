#!/usr/bin/env python3
"""Render human guidance from the same content the MCP guide loads."""

import argparse

from jeopardy_template.guidance import PROJECT_ROOT, render_documentation


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    path = PROJECT_ROOT / "PRODUCT_GUIDANCE.md"
    rendered = render_documentation()
    if args.check:
        if not path.exists() or path.read_text() != rendered:
            raise SystemExit("PRODUCT_GUIDANCE.md is stale; run scripts/render_guidance.py")
        print("Product guidance matches source")
    else:
        path.write_text(rendered)
        print("Rendered PRODUCT_GUIDANCE.md")


if __name__ == "__main__":
    main()
