# Workshop Tutorial: From API Access to an AI Guide

## Goodbye, Tutorial Hell: AI Guides and the New Documentation Layer

This tutorial supports the full GitHub Universe talk. Attendees first build a correct JSON → FastAPI → MCP pipeline, then use its limitations to discover why an MCP server that merely mirrors an API is not automatically a good learning experience.

The thin server is intentional. It is the control group.

By the end, attendees should be able to explain and demonstrate the difference between:

- giving an agent access to data and operations; and
- giving an agent enough product judgment to help someone make a good decision.

The runnable Part 1 implementation lives in [`JSON-API-MCP/`](JSON-API-MCP/README.md).

## The learning arc

| Stage | What attendees build | What it demonstrates | Question it leaves open |
|---|---|---|---|
| 1. JSON | A validated clue dataset | Source data needs an explicit domain contract | How should users access it? |
| 2. FastAPI | Search, retrieval, and category routes | A typed API creates a stable application boundary | How does an AI agent discover and call it? |
| 3. MCP wrapper | Three tools mapped to REST | MCP gives an agent reliable access | Does access teach the agent what it should do? |
| 4. Failure comparison | A realistic “quiz me” prompt | Correct tools can still produce an unhelpful experience | Where should product judgment live? |
| 5. AI Guide | A task-shaped, spoiler-safe practice tool | Defaults and anti-patterns change agent behavior | How do we keep guidance current? |
| 6. Shared guidance | One structured source for docs and tools | Documentation can teach humans and agents together | What should the team measure and maintain? |

The important teaching move is to pause after every stage. Do not reveal the next abstraction until attendees have felt the limitation of the current one.

## Before the workshop

Open the `JSON-API-MCP` folder as the VS Code workspace, then install and validate the locked environment:

```bash
cd JSON-API-MCP
uv sync --locked
uv run --locked python scripts/check_setup.py
```

Expected output:

```text
setup ready: 6 clues, synthetic-workshop-v1
```

The bundled clues are fictional but use the same flat record shape as the generated `combined.json` from `chancehl/JeopardyQuestions`. This keeps the workshop fast and avoids redistributing source material whose license is not stated.

## Chapter 1: turn JSON into a trustworthy domain model

Start with [`data/clues.json`](JSON-API-MCP/data/clues.json). Ask attendees what could go wrong if the application passed these objects directly to an agent.

Likely answers include missing fields, duplicate identifiers, unexpected round names, boolean values masquerading as integers, and losing the distinction between a numeric board value and a `null` Final Jeopardy value.

Open [`models.py`](JSON-API-MCP/src/jeopardy_template/models.py) and [`adapter.py`](JSON-API-MCP/src/jeopardy_template/adapter.py). Point out four choices:

1. `Round` is an enum rather than an arbitrary string.
2. IDs and board values use strict integer validation.
3. `value` explicitly permits `null`.
4. The adapter rejects malformed records and duplicate IDs with a record location.

Run the adapter tests:

```bash
uv run --locked pytest tests/test_adapter.py -q
```

### What this demonstrates

AI integration does not remove the need for data contracts. It makes them more important: once a tool result enters a model’s context, malformed data can become a confident natural-language claim.

### What this does not demonstrate

Validation says whether a record is structurally acceptable. It does not say whether showing that record is useful, whether revealing its answer is appropriate, or what the user should do next.

## Chapter 2: build a small FastAPI boundary

Open [`repository.py`](JSON-API-MCP/src/jeopardy_template/repository.py) and [`api.py`](JSON-API-MCP/src/jeopardy_template/api.py). The repository handles domain queries; FastAPI handles HTTP contracts.

Start the API:

```bash
uv run --locked uvicorn jeopardy_template.api:app \
  --host 127.0.0.1 \
  --port 8000
```

From a second terminal, inspect readiness and retrieve a clue:

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/clues/0
```

Then search and paginate:

```bash
curl 'http://127.0.0.1:8000/clues?category=DEVELOPER%20TOOLS&limit=2'
curl 'http://127.0.0.1:8000/categories?query=dev'
```

Ask attendees to find where the API guarantees:

- `404` for an unknown clue ID;
- `422` for invalid parameters;
- bounded result sizes;
- dataset-version metadata; and
- preservation of numeric and `null` values.

### What this demonstrates

FastAPI gives the dataset a typed, testable boundary that browsers, scripts, applications, and the later MCP server can share. The API—not the MCP server—owns data lookup and filtering.

### What this does not demonstrate

An OpenAPI description tells a caller what operations exist. It does not tell the caller which operation best serves a beginner, which defaults are pedagogically useful, or when a technically valid action creates a poor experience.

## Chapter 3: expose the API through MCP

Open [`api_client.py`](JSON-API-MCP/src/jeopardy_template/api_client.py) and [`mcp_server.py`](JSON-API-MCP/src/jeopardy_template/mcp_server.py).

The separation is deliberate:

```text
MCP tool → validated HTTP client → FastAPI → repository → JSON
```

The MCP server never opens the dataset. Every result comes through the same API contract used by other clients.

The three tools are:

- `search_clues` → `GET /clues`
- `get_clue` → `GET /clues/{clue_id}`
- `list_categories` → `GET /categories`

Each function uses type hints for its input schema, returns a validated model, and has read-only annotations. Expected API failures become MCP tool errors the model can read and recover from.

With FastAPI still running, execute the protocol-level smoke test:

```bash
uv run --locked python scripts/smoke_test.py
```

This test launches the MCP server as a real stdio subprocess, discovers its tools, invokes all three, and confirms clue values survive JSON → REST → MCP unchanged.

### Connect it to Copilot

The workspace includes `.vscode/mcp.json`. Start `jeopardy-basics` from VS Code’s MCP server list, open Copilot Chat in agent mode, and try:

> Find two clues in the Developer Tools category and retrieve the first one.

At this point, celebrate the working system—but do not imply the problem is solved.

### What this demonstrates

MCP makes capabilities discoverable and callable from an AI host. Typed tools, controlled errors, and structured results are a meaningful improvement over asking a model to invent an HTTP request.

### What this does not demonstrate

The tools still mirror API operations. They know how to search and retrieve, but they do not understand the user’s learning task. The server has access without much judgment.

## Chapter 4: make the wrapper fail honestly

Now use a prompt that expresses a goal instead of naming an endpoint:

> Quiz me with three Developer Tools clues. Do not reveal the answers until I respond.

Before running it, ask attendees to predict what will happen.

The wrapper’s search response includes each clue’s answer because that is the accurate API contract. Copilot may compensate using its own reasoning, but the tool itself offers no spoiler-safe behavior, no practice-set concept, and no guidance about when answers should be revealed.

Try a second prompt:

> I want to get better at the hardest material. Build me a short practice round.

The wrapper exposes round and value filters, but it does not define what “hardest” means, recommend a progression, or distinguish a search result from a useful exercise.

This is not a planted bug. The API and MCP server are both behaving correctly. Their limitation is that they model available operations rather than the user’s task.

### The discussion to lead

Ask the room:

1. Did the tool call succeed?
2. Was the user’s goal satisfied?
3. What judgment did Copilot have to invent at prompt time?
4. Where does that judgment already exist in a real company?

The likely sources are support macros, onboarding advice, documentation warnings, code-review comments, and experienced teammates. Those are the raw materials for an AI Guide.

## Chapter 5: redesign around the learning task

Do not add more endpoint-shaped tools. Create a second server so the original wrapper remains a fair control.

The first guide tool should represent the task:

```text
build_practice_set(
    category: optional string,
    difficulty: beginner | intermediate | advanced,
    clue_count: 1–10,
    reveal_answers: false by default
)
```

Its judgment should be explicit:

- Default to hiding answers because the user asked to practice.
- Use board value as a simple, disclosed difficulty proxy.
- Prefer a small set that fits one practice round.
- Do not pretend `value` measures universal conceptual difficulty.
- If too few clues match, return a smaller set and explain why instead of silently weakening the filters.

The guide may still call the same FastAPI endpoints internally. The difference is the interface and the encoded decision policy, not privileged access to better data.

### Write the guidance before the code

Create a structured guidance file for the practice task. A useful block contains:

```yaml
task: build_practice_set
default: Hide answers until the learner asks to reveal them.
use_when: The user wants to practice, study, or be quizzed.
avoid: Returning raw search results with answers visible.
tradeoff: Board value is only a rough difficulty proxy.
example:
  request: Quiz me on three advanced Developer Tools clues.
  behavior: Return three high-value prompts with IDs and values, but no answers.
```

Keep policy out of the Python decorator body where possible. The same structured content should later render into human documentation and supply the MCP tool description or handler behavior.

### Run the controlled comparison

Open two VS Code windows with the same model and prompt:

- Window A: `jeopardy-basics`, the thin wrapper.
- Window B: the task-focused guide server.

Run the same two prompts from Chapter 4. Compare:

- which tools are selected;
- whether answers leak;
- whether the server uses an opinionated default;
- whether it names the difficulty tradeoff; and
- whether its output gives the learner a clear next action.

The point is not that the guide uses a smarter model. The model, data, and API remain constant. The server supplies better judgment.

## Chapter 6: let attendees encode one judgment

Ask each attendee to change one rule in the guidance file. Good starter rules include:

- beginners receive lower-value clues first;
- practice sets should not repeat a category unless requested;
- answers remain hidden by default;
- Final Jeopardy clues should be labeled as having no fixed board value; or
- a result shortage should be disclosed rather than filled with unrelated clues.

Restart the guide server and repeat the relevant prompt. The learning objective is the edit–restart–observe loop: documentation changes agent behavior.

Then ask whether the rule belongs in:

- repository instructions, if it describes how this development team works; or
- the AI Guide, if it describes how the product should be used.

This turns the “house rules versus product manual” distinction into something attendees can test.

## Chapter 7: adapt the pattern to another dataset

Use the [adaptation exercise](JSON-API-MCP/ADAPTATION_EXERCISE.md) to replace Jeopardy-shaped data with a small fixture from another domain.

The reusable pieces are:

- stdio transport and VS Code configuration;
- validated HTTP-client boundary;
- controlled tool-error translation;
- lockfile and test workflow; and
- protocol-level smoke-test pattern.

The domain-specific pieces are:

- models and adapter;
- filters and indexes;
- routes and HTTP response contracts;
- tool shapes and descriptions; and
- product judgment.

Attendees should not leave believing three generic tools are a universal interface. They should leave knowing how to identify and redesign the domain-specific layer.

## Closing synthesis

End by returning to the original pipeline:

```text
JSON → FastAPI → MCP wrapper → access
                      + structured judgment → AI Guide
```

The wrapper is valuable infrastructure. It proves transport, validation, error handling, and end-to-end fidelity. But infrastructure alone does not teach.

The complete lesson is:

1. Build a trustworthy data and API boundary.
2. Expose a small, testable MCP surface.
3. Observe where endpoint-shaped tools fail user-shaped goals.
4. Encode defaults, decisions, anti-patterns, and examples.
5. Compare behavior with one variable changed.
6. Maintain that judgment as shared documentation for humans and agents.

That is how the workshop avoids becoming another “follow these commands and admire the demo” tutorial. Attendees experience the limitation, change the system, and see why the change matters.

## Completion checklist

An attendee has completed the workshop when they can:

- retrieve a clue through both REST and MCP;
- explain why the MCP server calls FastAPI instead of reading JSON directly;
- show that numeric and `null` values survive end to end;
- identify a successful tool call that still fails the user’s goal;
- rewrite one endpoint-shaped interaction as a task-shaped tool;
- encode one explicit default or anti-pattern; and
- describe which parts they would replace for their own dataset.
