# JSON → FastAPI → MCP: Part 1

Build a small, repeatable data pipeline that turns JSON into a typed FastAPI API and then exposes that API to GitHub Copilot through an MCP server.

This is Part 1 of **Goodbye, Tutorial Hell: AI Guides and the New Documentation Layer**. It deliberately builds a thin, correct MCP wrapper first. In Part 2, the same project will become an opinionated AI Guide so you can see the difference between giving an agent access and giving it judgment.

For the complete teaching sequence—including the wrapper’s intentional failure case and the transition to a task-focused guide—see the [full workshop tutorial](../TUTORIAL.md).

If you only need to install, start, and use the server, follow the standalone [server instructions and design rationale](INSTRUCTIONS.md).

## What you will build

```text
JSON file → adapter → validated clues → FastAPI
                                         ↑
GitHub Copilot → MCP over stdio → HTTP client
curl / browser ──────────────────────────┘
```

The finished MCP server has exactly three read-only tools:

- `search_clues` searches clue text and filters by category or round.
- `get_clue` retrieves one clue by ID.
- `list_categories` finds category names.

Every clue result includes its board `value`, including `null` for Final Jeopardy. The MCP layer always calls FastAPI; it does not read the dataset directly or maintain a second implementation.

## Who this is for

This tutorial is for intermediate Python developers, maintainers, and technical product builders who want to expose their own JSON-backed data to AI agents. It is also the first hands-on exercise for a 45-minute GitHub Universe workshop.

## Prerequisites

- Python 3.12 or newer
- [`uv`](https://docs.astral.sh/uv/)
- VS Code with GitHub Copilot for the final step
- Optional: Git, Node, and `jq` to import the full upstream dataset

## Step 1: install the locked environment

Clone this repository, open it in VS Code, and run:

```bash
uv sync --locked
uv run --locked python scripts/check_setup.py
```

`pyproject.toml` declares the direct dependencies and `uv.lock` freezes the complete environment. Use `--locked` in development and CI so an outdated lockfile fails loudly. After a lockfile has already been verified, `--frozen` is appropriate for repeatable runs that must not re-resolve it.

## Step 2: understand the bundled data

`data/clues.json` is a tiny, fictional dataset shaped like [`chancehl/JeopardyQuestions`](https://github.com/chancehl/JeopardyQuestions). It is included so the tutorial works without a large download and without redistributing upstream clue text whose license has not been stated.

Each clue has this shape:

```json
{
  "id": 0,
  "prompt": "This protocol lets AI applications discover and call external tools",
  "answer": "What is MCP?",
  "category": "DEVELOPER TOOLS",
  "round": "Jeopardy",
  "value": 200,
  "gameId": 1001
}
```

The important files are:

- `models.py`: the validated domain and response contracts.
- `adapter.py`: the dataset-specific JSON-to-model boundary.
- `repository.py`: in-memory lookup, filtering, and pagination.
- `api.py`: HTTP routes only.
- `api_client.py`: the one client used by every MCP tool.
- `mcp_server.py`: typed MCP tools; it has no file or repository access.

## Step 3: start FastAPI

In the first terminal:

```bash
uv run uvicorn jeopardy_template.api:app --host 127.0.0.1 --port 8000
```

Check readiness and try the routes:

```bash
curl http://127.0.0.1:8000/health
curl 'http://127.0.0.1:8000/clues?query=protocol&limit=2'
curl http://127.0.0.1:8000/clues/0
curl 'http://127.0.0.1:8000/categories?query=dev'
```

FastAPI returns `404` for an unknown clue ID and `422` for invalid query parameters. Empty searches return `200` with an empty `items` list.

## Step 4: connect the MCP server

Keep FastAPI running. The MCP process is separate and talks to the API at `http://127.0.0.1:8000`.

This repository includes `.vscode/mcp.json`. In VS Code:

1. Open the `JSON-API-MCP` folder as the VS Code workspace.
2. Open the MCP server list and start `jeopardy-basics` if it is not already running.
3. Open Copilot Chat in agent mode and confirm the three Jeopardy tools appear.
4. Ask: **“Find two Developer Tools clues and retrieve the first one.”**

The MCP host launches `uv run --locked python -m jeopardy_template.mcp_server`. The server uses stdio, so do not print to stdout from `mcp_server.py`; stdout carries protocol messages. Application logging goes to stderr.

If VS Code cannot find `uv`, replace `"uv"` in `.vscode/mcp.json` with the absolute path printed by `which uv` (macOS/Linux) or `where uv` (Windows).

## Step 5: verify the whole pipeline

With FastAPI still running:

```bash
uv run --locked python scripts/smoke_test.py
uv run --locked pytest
```

The smoke test launches the MCP server as a real stdio subprocess, discovers exactly three tools, calls FastAPI through one of them, and checks that numeric and `null` clue values survive the entire path.

## Optional: import `chancehl/JeopardyQuestions`

The upstream repository stores nested episode JSON under `src/`. Its generated `combined.json` is gitignored, so build it before importing. Pin a revision rather than importing a moving branch.

```bash
git clone https://github.com/chancehl/JeopardyQuestions.git upstream
cd upstream
git checkout <recorded-commit-sha>
./combine.sh
node format.js
cd ..
```

Then prepare a deterministic, round-balanced sample:

```bash
uv run --locked python scripts/prepare_data.py \
  --source upstream/combined.json \
  --output data/clues.json \
  --manifest data/manifest.json \
  --source-revision <recorded-commit-sha> \
  --limit 300
```

The importer validates every record, rejects duplicate IDs, selects records deterministically across all three rounds, writes atomically, and records the input checksum and revision in the manifest. Re-run the API after replacing the data.

> The upstream repository does not currently state redistribution terms. Do not commit generated clue samples until you have confirmed that you have permission to redistribute them.

## Adapt this to another dataset

Repeatability here means a documented adapter pattern, not a magical schema generator. To swap domains:

1. Replace the domain models and source-field normalization in `models.py` and `adapter.py`.
2. Change repository filters and indexes in `repository.py`.
3. Revise FastAPI routes and response contracts in `api.py`; update `api_client.py` to match.
4. Replace the three domain-specific tool shapes and descriptions in `mcp_server.py`.
5. Add one synthetic fixture and test the full JSON → REST → MCP path.

Transport setup, environment configuration, error translation, lockfile workflow, and the protocol-level test pattern can remain the same.

Work through the [dataset adaptation exercise](ADAPTATION_EXERCISE.md) for a guided version of this swap.

## What Part 1 intentionally does not do

This baseline does not implement gameplay, scoring, answer grading, writes, accounts, vector search, remote MCP hosting, or authentication. It also returns answers, so it is not a spoiler-safe quiz guide.

Part 2 will add a task-focused tool that hides answers by default, explains strategic choices, and pushes back on poor requests. That is the shift from an API wrapper to an AI Guide.

## Troubleshooting

- **The MCP tools fail with “API unavailable.”** Start Uvicorn in a separate terminal and check `/health`.
- **VS Code shows no tools.** Confirm you opened the repository root, trust the workspace, and start `jeopardy-basics` from the MCP server list.
- **`uv` is not found by VS Code.** Use its absolute path in `.vscode/mcp.json`.
- **The dataset fails to load.** Run `scripts/check_setup.py`; the error includes the record index and validation problem.
- **A full import is slow or memory-heavy.** The tutorial is optimized for a bounded sample. Benchmark before replacing the repository with SQLite for the full archive.

## Reference material

- [Workshop outline](../OUTLINE.md)
- [chancehl/JeopardyQuestions](https://github.com/chancehl/JeopardyQuestions)
- [Official MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [VS Code MCP configuration](https://code.visualstudio.com/docs/agents/reference/mcp-configuration)
- [uv project documentation](https://docs.astral.sh/uv/guides/projects/)
