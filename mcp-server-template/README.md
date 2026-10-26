# Build an MCP guide with your own context

Copy this folder into your own project, replace the example context, and start a working MCP server in your editor. It runs independently of the workshop and requires no database, external API, or model API key. Your editor supplies the model.

The server helps an agent discover product tasks, read relevant documentation, and recommend a next step with a rationale and source reference. It is a recommendation template: performing product operations requires adding your own tools and handlers.

## 1 Copy the template

From the workshop repository root:

```bash
python3 mcp-server-template/copy_template.py ../my-product-guide
cd ../my-product-guide
```

Choose any new destination folder you own. The copier preserves existing folders and excludes virtual environments and caches. You can also copy the folder manually with those exclusions.

This folder includes everything needed to continue:

```text
my-product-guide/
├── README.md                 Your setup and adaptation instructions
├── .vscode/mcp.json           Editor configuration
├── pyproject.toml            Dependencies and checks
├── uv.lock                   Reproducible dependency versions
├── server.py                 MCP tools and recommendation handler
├── context_loader.py         Validation, source references, and rendering
├── context/
│   ├── guide.json            Product name, tasks, choices, and decision rules
│   └── product.md            Your product or codebase reference material
├── CONTEXT_GUIDE.md          Generated human version of that context
├── render_context.py         Refresh the human guide
├── verify.py                 Test a copied server and a context-only edit
├── copy_template.py          Copy again without generated caches
└── tests/test_template.py    Contract and behavior checks
```

## 2 Install and run the supplied example

You need Python 3.12+ and [uv](https://docs.astral.sh/uv/getting-started/installation/). Run these commands from your **copied folder**:

```bash
uv sync --locked
uv run --locked python server.py --check
```

Expected output:

```text
Context ready: Your Product, 1 task(s)
```

In VS Code, open the copied folder itself. Sign in to Copilot, use Agent mode, and run **MCP: List Servers → my-product-guide → Start Server**. Select its three tools:

- `list_tasks`: discover which product tasks the server supports.
- `get_guidance`: retrieve a task's rules, examples, and Markdown reference docs.
- `recommend_next_step`: apply a documented default or valid explicit choice; ask questions about unmet requirements.

Start a fresh chat:

> Use only my-product-guide tools. List the available tasks, then recommend my next deployment step for task deploy. Omit choice so the documented default applies. Explain the rationale and cite the source.

Expect `preview`. Inspect the tool result for `decision_basis: default` and a source pointing to `context/guide.json` at `/tasks/0/default_choice`. Source revisions are SHA-256 hashes of the files loaded at startup.

For another MCP host, configure it to launch `uv run --locked --directory /absolute/path/to/my-product-guide python server.py` over stdio. Resolve its working directory with that absolute path. Host configuration formats differ; the included `.vscode/mcp.json` is specifically for VS Code.

## 3 Replace the context with your own

Open `context/guide.json` and set `product_name` to your product or codebase name. It becomes the server's display name. The configuration ID `my-product-guide` can stay the same or be renamed in `.vscode/mcp.json`.

Choose one recurring user question and edit the task fields:

| Field | What to put there |
|---|---|
| `id` | A unique lowercase task ID, such as `choose-storage`. Use letters, numbers, hyphens, or underscores; start with a letter. |
| `title` and `when_to_use` | The user's goal and when the agent should retrieve this guidance. |
| `default_choice` | The ID of the recommended starting choice. It must exist and have no required facts. |
| `choices` | Allowed next steps, each with an ID, recommendation, rationale, and `requires` list. |
| `fact_questions` | A question for each fact that can change the recommendation. Keys must match `requires` entries. |
| `avoid` | The common mistake or anti-pattern you want to prevent. |
| `example_request` and `example_behavior` | A realistic user request and the response behavior to aim for. |
| `references` | Markdown paths relative to `context/`, such as `product.md` or `guides/setup.md`. |

Replace `context/product.md` with your documentation: product purpose, compatibility requirements, terminology, examples, and how users can check success. Add more Markdown files inside `context/` and reference them from the appropriate tasks. Only listed references are loaded; copying a document into the folder alone does not expose it.

To add another task, duplicate a task object in the `tasks` array, give it a unique ID, and replace its choices, questions, examples, and references. **No Python change is required** for tasks that fit this recommendation structure. The generic tool names and transport stay the same.

## 4 Validate and refresh

From the copied folder:

```bash
uv run --locked python server.py --check
uv run --locked python render_context.py
uv run --locked python render_context.py --check
```

Review `CONTEXT_GUIDE.md`. It renders the same source rules and reference material the MCP tools load. Edit the JSON and Markdown sources, rather than the generated guide.

Restart `my-product-guide` after a context edit. The server loads a snapshot at startup. Use a fresh chat and refresh the host's tool descriptions if they show old content.

## 5 Prove your edit changed the recommendation

For the supplied example, change `default_choice` from `preview` to `staging`. Validate, render, restart, and repeat the **same prompt** from Step 2 in a fresh chat.

Expect `staging`, the same default-choice source pointer, a changed revision, and staging's rationale. Confirm the tool call omitted `choice`; an agent-supplied explicit choice can mask the default.

Ask for an explicit alternative:

> For task deploy, choose preview even though staging is the default. Explain why the explicit choice takes precedence.

Expect `decision_basis: explicit_choice`. Then test a requirement:

> For task deploy, choose production. I have not supplied any verification facts. Ask me for the missing information rather than assuming it.

Expect the current default plus `decision_basis: clarification_required` and a question about nonproduction verification. Supplying `facts: {"verified_nonproduction": true}` permits the production recommendation. That is user-supplied confirmation; the server performs no independent validation or deployment.

In your own context, repeat this loop with a real choice and question from your product. Explain why the rule applies, when it changes, and how the developer can verify the advice.

## 6 Test and extend your server

```bash
uv run --locked ruff check .
uv run --locked pytest
uv run --locked python verify.py
```

The verifier copies the implementation and context to a temporary folder outside the workshop, starts real stdio MCP clients, changes a default, and adds a task without modifying Python. It leaves your files untouched. Its edit scenario needs two choices without required facts in the first task; adapt it if your context has a different shape.

The bundled unit tests cover the supplied deployment fixture. When replacing that fixture, update the scenario-specific assertions in `tests/test_template.py` to match your task. Keep the validation, source-reference, and protocol checks.

For more than advice, add a task-shaped tool in `server.py` with validated inputs and a return model. Connect your own API or data source in its handler, enforce operational constraints in code, and test the real behavior. Plain text in `context/` does not implement API calls or enforce every instruction on the agent.

To debug startup directly, run `uv run --locked python server.py`. It waits for an MCP host on stdio; use Ctrl+C to stop it. Keep application logging on stderr.

If VS Code cannot find uv, replace `"uv"` in `.vscode/mcp.json` with the absolute path from `which uv` or `where uv`. If tools are missing, open the copied folder itself, trust the workspace, and start `my-product-guide`. Unknown task or choice errors list the available IDs; retrieve `list_tasks` instead of guessing a name. Invalid or missing reference files are reported by `python server.py --check`.

## What this template takes from pg-aiguide

- **Task discovery and relevant context:** the [Postgres entry skill](https://github.com/timescale/pg-aiguide/blob/5d3b76b5c986693b30753828b404aa66ba34c31a/skills/postgres/SKILL.md) routes work to relevant references. Here, a task catalog leads to the rules and documents you supplied.
- **Opinionated choices with reasons:** the [table-design skill](https://github.com/timescale/pg-aiguide/blob/5d3b76b5c986693b30753828b404aa66ba34c31a/skills/design-postgres-tables/SKILL.md) gives preferred choices and alternatives. Here, each choice has a rationale and explicit conditions.
- **Questions for missing facts:** the [hypertable skill](https://github.com/timescale/pg-aiguide/blob/5d3b76b5c986693b30753828b404aa66ba34c31a/skills/setup-timescaledb-hypertables/SKILL.md) asks about unknown requirements. Here, `fact_questions` makes those questions part of your context contract.
- **Evidence you can inspect:** the [schema-exploration skill](https://github.com/timescale/pg-aiguide/blob/5d3b76b5c986693b30753828b404aa66ba34c31a/skills/schema-exploration/SKILL.md) distinguishes observations from inference. Here, file pointers, revisions, and supplied facts make the basis of a recommendation visible.

The template uses local files and a small recommendation handler. Its generated human guide and deterministic default-edit test are workshop implementation choices, rather than claims about pg-aiguide's architecture.

## Completion check

- You can find your task and read your product context through MCP.
- You can identify the exact source of a recommendation.
- A context edit changes the next recommendation after restart.
- A missing fact produces a useful question.
- Someone else can explain when the advice applies to a changed scenario.
