# Workshop verification status

The [protocol evidence](protocol-verification.json) records actual local MCP subprocess runs. It verifies practice content changing from two to three and deployment content changing from preview to staging using temporary copies. It also checks the unchanged wrapper, answer visibility and reveal, explicit count overrides, shortages, and the production-readiness question.

The record includes its timestamp, Python version, a hash of the implementation modules, content revisions, and before/after tool results. These are server results; no editor or model is represented by that JSON record.

Separate [editor smoke observations](editor-smoke.md) record VS Code discovering all four tools and Copilot using the edited practice and deployment defaults in fresh chats. Both before/after pairs identified GPT-6 Luna. These observed comparisons do not establish five-run reliability or attendee comprehension.

Regenerate it from the repository root:

```bash
uv run --locked --directory JSON-API-MCP python scripts/verify_workshop.py --output ../evidence/protocol-verification.json
```

The existing `JSON-API-MCP/.venv` was used for local verification. Lint, 21 tests, setup validation, and generated-document consistency pass. The local runtime is Python 3.14; the workflow targets Python 3.12 and has been extended for the new checks, but the updated CI has not run on GitHub yet.

## Standalone template verification

The [copyable MCP template](../mcp-server-template/README.md) has its own lockfile, context, editor configuration, and checks. Eight template tests, lint, context validation, and generated-document consistency pass in Python 3.12.15.

The copy helper was exercised into a new temporary project outside the repository. That project installed its locked dependencies into a fresh virtual environment using the local package cache and passed its real stdio MCP verifier. The [template protocol record](template-verification.json) captures a default change and the addition of a task without Python changes. This verifies copy/install/protocol behavior; an editor/model or attendee run of the new template is still unverified.

## Remaining workshop observations

- Broader editor/model behavior, strict tool isolation, natural prompts without parameter hints, and description inspection after restart.
- Five fresh editor runs per primary scenario, recorded in [DEMO.md](../DEMO.md).
- A clean local install, root Codespaces startup, and a second MCP-compatible host.
- A reviewer completing installation within eight minutes and the edit within six minutes.
- A reviewer adapting a product rule and explaining its tradeoff in a changed scenario.
- A full 45-minute session rehearsal and fallback captures from actual editor runs.

Configuration and instructions for these checks are supplied. Their results remain unverified until observed; protocol success alone does not establish the attendee acceptance criterion.
