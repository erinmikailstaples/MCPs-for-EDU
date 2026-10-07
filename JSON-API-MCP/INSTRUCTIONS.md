# Using the Jeopardy JSON → FastAPI → MCP Server

This guide explains how to install, start, verify, and use the reference server. It also explains why you might put a server in front of a JSON file instead of giving an application or AI agent direct access to the file.

## What runs locally

The example has two separate processes:

```text
data/clues.json
      ↓
FastAPI on http://127.0.0.1:8000
      ↑
MCP server over stdio
      ↑
VS Code / GitHub Copilot
```

FastAPI owns data loading, validation, searching, filtering, pagination, and HTTP errors. The MCP server exposes three tools and calls FastAPI for every result. It never opens the JSON file directly.

Keeping these processes separate is intentional. It lets ordinary applications and AI tools use the same domain contract without duplicating data-access logic.

## Requirements

Install these before starting:

- Python 3.12 or newer
- [`uv`](https://docs.astral.sh/uv/)
- VS Code with GitHub Copilot if you want to call the server from an AI agent

Run all commands in this document from the `JSON-API-MCP` directory:

```bash
cd JSON-API-MCP
```

## 1. Install the environment

Install the exact dependency versions recorded in `uv.lock`:

```bash
uv sync --locked
```

Then check the local dataset and manifest:

```bash
uv run --locked python scripts/check_setup.py
```

Expected output:

```text
setup ready: 6 clues, synthetic-workshop-v1
```

Use `--locked` while developing or running CI. It verifies that `uv.lock` still agrees with `pyproject.toml` instead of silently changing the environment.

## 2. Start FastAPI

Open a terminal and run:

```bash
uv run --locked uvicorn jeopardy_template.api:app \
  --host 127.0.0.1 \
  --port 8000
```

Leave this terminal running. The MCP tools depend on the API.

The API binds to loopback, so it is available only from the local machine. This example is not configured for public hosting.

## 3. Verify the API

Open a second terminal in `JSON-API-MCP`.

Check that the process is ready and the dataset loaded successfully:

```bash
curl http://127.0.0.1:8000/health
```

Retrieve one clue:

```bash
curl http://127.0.0.1:8000/clues/0
```

Search and filter:

```bash
curl 'http://127.0.0.1:8000/clues?query=protocol&limit=2'
curl 'http://127.0.0.1:8000/clues?category=DEVELOPER%20TOOLS'
curl 'http://127.0.0.1:8000/categories?query=dev'
```

Interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

Useful response behavior:

- Unknown clue IDs return `404`.
- Invalid rounds, limits, or offsets return `422`.
- Searches with no matches return `200` and an empty `items` array.
- Every clue includes `value`; Final Jeopardy values remain `null`.
- Every response identifies the active dataset version.

## 4. Start the MCP server in VS Code

Open the `JSON-API-MCP` directory as the VS Code workspace. This is important because the MCP configuration uses `${workspaceFolder}`.

The included `.vscode/mcp.json` tells VS Code to launch:

```bash
uv run --locked python -m jeopardy_template.mcp_server
```

To use it:

1. Keep FastAPI running in the first terminal.
2. Open VS Code’s MCP server list.
3. Start `jeopardy-basics` if it is not already running.
4. Open GitHub Copilot Chat in agent mode.
5. Confirm these tools are available:
   - `search_clues`
   - `get_clue`
   - `list_categories`

Try this prompt:

> Find two clues in the Developer Tools category and retrieve the first one.

The model should call `search_clues`, use an ID from the structured result, and then call `get_clue`.

## 5. Verify MCP without relying on Copilot

Copilot output can vary, so use the deterministic smoke test when checking the implementation:

```bash
uv run --locked python scripts/smoke_test.py
```

This test:

1. checks the running FastAPI service;
2. launches the MCP server as a real stdio subprocess;
3. discovers exactly three tools;
4. invokes search, retrieval, and category tools; and
5. confirms numeric and `null` clue values survive the entire pipeline.

Run the complete test suite with:

```bash
uv run --locked ruff check .
uv run --locked pytest
```

## Stopping the server

Press `Ctrl+C` in the terminal running Uvicorn. VS Code manages the MCP subprocess and stops or restarts it from the MCP server controls.

## Troubleshooting

### The MCP tool reports that the API is unavailable

The two-process architecture means starting the MCP server does not start FastAPI. Run Uvicorn in a separate terminal and verify `/health` before trying the tool again.

### VS Code cannot find `uv`

Find the executable:

```bash
which uv
```

On Windows:

```powershell
where uv
```

Replace `"uv"` in `.vscode/mcp.json` with the absolute path returned by that command.

### No MCP tools appear

Confirm that:

- `JSON-API-MCP` is the open workspace folder;
- the workspace is trusted;
- `uv sync --locked` completed successfully; and
- `jeopardy-basics` is running in the MCP server list.

### The MCP process starts and immediately disconnects

Run the module from a terminal to expose its startup error:

```bash
uv run --locked python -m jeopardy_template.mcp_server
```

A healthy stdio server appears to do nothing because it is waiting for an MCP host to write to stdin. Stop it with `Ctrl+C`.

Do not add debugging `print()` calls to MCP stdout. Standard output carries protocol messages; use Python logging, which writes to stderr by default.

### The dataset fails to load

Run:

```bash
uv run --locked python scripts/check_setup.py
```

The adapter reports malformed JSON, the failing array index, missing fields, invalid values, or duplicate IDs. Fix the source instead of silently dropping bad records.

## Why convert a JSON file into a server?

A JSON file is an excellent storage format for small, static, portable datasets. You do not need a server merely because the file exists. A server becomes useful when multiple consumers need a stable and controlled way to work with that data.

### 1. A server creates a contract

Raw JSON describes values, but it does not enforce how clients interpret them. The API establishes validated request and response models, allowed round names, pagination limits, nullable fields, error behavior, and dataset-version metadata.

Without that contract, every client must independently decide how to handle missing fields, invalid records, duplicate IDs, filtering, and pagination. Those implementations will eventually disagree.

### 2. Validation happens once

The adapter validates the dataset when the API starts. Downstream clients receive normalized records instead of repeatedly parsing and trusting an arbitrary file.

This is especially useful for AI integrations. Models can turn malformed or ambiguous data into confident prose, so validating information before it enters model context is valuable.

### 3. Consumers do not need filesystem access

A browser, another application, or an MCP server may not share the dataset’s filesystem. An API provides a narrow interface without exposing directory paths or allowing callers to read unrelated files.

For this local example, FastAPI is bound to loopback and the MCP server receives only a configured base URL. The model cannot choose an arbitrary URL or file path.

### 4. Search and pagination stay consistent

If every consumer reads the JSON directly, each one must reimplement substring matching, exact category filters, round validation, ordering, pagination, and result limits.

Putting those behaviors behind an API creates one tested definition. A CLI, web interface, and AI agent can all return the same records for the same query.

### 5. Storage can change without breaking clients

This tutorial uses an in-memory collection because it is easy to understand and appropriate for a small workshop dataset. If the full dataset becomes too large or slow, the repository can move to SQLite or another store while preserving the REST and MCP contracts.

That boundary lets you change implementation details without asking every consumer to change at the same time.

### 6. MCP tools can reuse the application boundary

The MCP server does not need its own dataset logic. It translates model-friendly tool calls into API calls and validates the responses.

This prevents a common failure mode where the web product and the AI integration produce different answers because they use separate implementations.

### 7. You gain observable failure behavior

Servers provide clear places to record readiness, request outcomes, latency, result size, dataset version, and controlled errors. Those signals are harder to centralize when clients silently read a file themselves.

## When a server is unnecessary

Do not add a server if all of these are true:

- one local script is the only consumer;
- the file is small and trusted;
- no shared search or business rules are needed;
- filesystem access is acceptable; and
- there is no need for independent versioning or observability.

In that case, reading and validating JSON directly is simpler. The extra process, port, configuration, HTTP client, and failure modes would add ceremony without buying a useful boundary.

## Why the server is not the end of the lesson

Converting JSON into FastAPI and MCP gives an agent reliable **access**. It does not automatically give the agent good **judgment**.

The current MCP tools closely mirror API operations. They can search and retrieve clues, but they do not know that a learner asking to be quizzed probably wants answers hidden. They also do not know how to build a useful practice progression or when to explain the limitations of board value as a difficulty signal.

Use this prompt to expose the gap:

> Quiz me with three Developer Tools clues. Do not reveal the answers until I respond.

The API accurately returns answers, and the thin MCP wrapper accurately passes them through. A successful tool call can therefore create a poor learning experience.

That limitation is the bridge to an AI Guide. The next layer should add task-shaped tools and explicit product judgment, such as:

- hide answers by default for practice tasks;
- use board value only as a disclosed difficulty proxy;
- prefer a small, focused practice set;
- state when too few records match; and
- offer a clear next action.

The larger workshop tutorial walks through that transition in [From API Access to an AI Guide](../TUTORIAL.md).

## Practical design tips

- Start with one real user task, not every possible endpoint.
- Keep dataset access in the API; do not duplicate it in MCP handlers.
- Return structured results so hosts can reason about fields without scraping prose.
- Preserve meaningful `null` values instead of inventing replacements.
- Cap result sizes before data enters model context.
- Translate expected API failures into useful tool errors.
- Include dataset-version metadata when record IDs can change between snapshots.
- Test through the protocol, not only by calling decorated Python functions directly.
- Keep a thin wrapper as a control when teaching the value of an opinionated guide.
- Treat the server boundary as infrastructure; encode product judgment deliberately on top.
