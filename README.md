# Goodbye, Tutorial Hell: AI Guides and the New Documentation Layer

**A 45-minute GitHub Universe workshop with Claire Waters and Erin Mikail Staples.**

A tutorial can get a developer to a first success. Their own project brings new choices: which option to use, what to avoid, and when to ask for more information. This workshop shows how an opinionated MCP server can bring documented product judgment into the editor while a developer works.

You will fork a working scaffold, compare a thin API wrapper with a guide, edit a recommendation, and reuse the pattern in a deployment-advice example.

**You have completed the workshop when you can trace a recommendation to guidance you edited, observe its effect in your editor, and adapt that pattern to your own product.**

**Ready to build your own?** Use the standalone [MCP server template](mcp-server-template/README.md) and the [copy and customization steps below](#build-your-own-mcp-server). You can supply your own context and add recommendation tasks without changing Python.

## Follow the full talk

Read this page in order to follow the session independently. During the live talk, complete setup while you wait; the presenters demonstrate the first comparison before the installation checkpoint.

| Part | Time | What you will learn or do |
|---|---:|---|
| [Before the session: setup](#start-in-your-editor) | Before the clock | Fork the scaffold and prepare the editor. |
| [1. Why developer education needs judgment](#1-why-developer-education-needs-judgment) | 5 min | Identify the decisions a tutorial leaves to its reader. |
| [2. Compare a wrapper and a guide](#2-compare-a-wrapper-and-a-guide) | 7 min | Inspect what the server supplies and what the model infers. |
| [3. Learn from pg-aiguide and trace a recommendation](#3-learn-from-pg-aiguide-and-trace-a-recommendation) | 6 min | Connect product advice to its source and rationale. |
| [4. Run your own guide](#4-run-your-own-guide) | 8 min | Confirm your installation and retrieve a practice round. |
| [5. Edit guidance and observe the change](#5-edit-guidance-and-observe-the-change) | 6 min | Change two clues to three and inspect the result. |
| [6. Take away a product example](#6-take-away-a-product-example) | 5 min | Change a deployment recommendation and apply the pattern elsewhere. |
| [7. Explain what you learned](#7-explain-what-you-learned) | 8 min | Discuss tradeoffs, recover from setup issues, and identify your next use case. |

The timed parts total 45 minutes. [OUTLINE.md](OUTLINE.md) contains presenter notes; this README contains the attendee walkthrough.

## Start in your editor

You need a GitHub account, VS Code with GitHub Copilot agent mode available, Python 3.12 or newer, and [uv](https://docs.astral.sh/uv/getting-started/installation/).

### Fork and open the repository

1. Fork [MCPs-for-EDU](https://github.com/erinmikailstaples/MCPs-for-EDU) into your GitHub account.
2. Clone your fork. Replace `YOUR-USERNAME` below; adjust the repository name if you renamed your fork:

   ```bash
   git clone https://github.com/YOUR-USERNAME/MCPs-for-EDU.git
   cd MCPs-for-EDU
   ```

3. In VS Code, choose **File → Open Folder** and open the cloned repository root: the folder containing this README and `JSON-API-MCP`.
4. Sign in to GitHub Copilot and trust this workspace so its local server can run.

For the Codespaces route, create a Codespace from your fork's **Code → Codespaces** menu. The root devcontainer is configured to install uv and the project environment. Once it opens, continue with the setup check below. Codespaces still needs a clean-environment rehearsal; local editor smoke results are recorded in [verification status](evidence/README.md).

### Install and check the environment

Run these commands in a terminal at the **repository root**:

```bash
uv sync --locked --directory JSON-API-MCP
uv run --locked --directory JSON-API-MCP python scripts/check_setup.py
```

Expected setup output:

```text
setup ready: 6 clues, synthetic-workshop-v1
```

### Start the guide

1. Open the Command Palette and run **MCP: List Servers**.
2. Select **education-guide**, then **Start Server**.
3. Open Copilot Chat in **Agent** mode and inspect **Configure Tools**. Confirm these tools are available:

   - `get_guidance`
   - `build_practice_set`
   - `reveal_answer`
   - `recommend_deployment`

Use only this server's tools for the guide exercise. Tool selection can apply across chats in the tested VS Code setup, so check it again when switching windows or restore your usual selection afterward.

The included configuration starts the clue API and MCP server together. You do not need to launch FastAPI separately or manage a second terminal. The guide is ready when VS Code reports four discovered tools.

## 1 Why developer education needs judgment

An API reference tells you which operations exist. Product guidance helps you choose an operation, use a sensible default, recognize an exception, and check the result.

Our example is a practice application. Its API returns clues, answers, categories, and board values. A useful practice experience also needs decisions: how many clues to start with, when to show answers, and how to explain difficulty.

Keep three mechanisms in mind throughout the talk:

| Mechanism | Example in this scaffold |
|---|---|
| Data access | The API returns matching clues. |
| Executable policy | The guide applies the configured count and omits answers from practice results. |
| Advice for the agent | The guidance explains the limits of board value and when to ask about a learner's goals. |

The workshop asks you to inspect those mechanisms and explain the resulting recommendation.

## 2 Compare a wrapper and a guide

The presenters demonstrate this comparison. To reproduce it yourself, use two VS Code windows:

| Window | Folder to open | MCP server | Tools |
|---|---|---|---|
| A: wrapper | `JSON-API-MCP` | `jeopardy-basics` | `search_clues`, `get_clue`, `list_categories` |
| B: guide | Repository root | `education-guide` | The four guide tools listed above |

Both launchers use the same bundled data and manage their own local API. Choose the same model in both windows, enable only the assigned server's tools, and begin with fresh chats.

Send this **identical prompt** in each window:

> Give me a beginner practice round in Developer Tools. Explain your recommendation and identify its guidance source.

Inspect the tool calls as well as the final response:

- Did the agent select a count itself, or use a server default?
- Did the tool result contain answers? Did the final response expose them?
- What recommendation did the agent make, and what reason did it give?
- Can you locate a product rule behind that recommendation?

The wrapper's tool results include answers. The guide's practice results omit them and return source rules. The model may still produce a good practice experience with the wrapper. Record what happened and distinguish what the server supplied from what the model inferred.

For the second discussion prompt, ask:

> Does the highest board value mean this is objectively the hardest clue for me? I want to improve at debugging MCP servers.

Look for an explanation of the proxy's limits and a useful question about the learner's goal. This comparison changes both tool design and guidance. Part 5 uses the same guide before and after a content edit to trace that edit's effect more precisely. [DEMO.md](DEMO.md) contains the rehearsal and reset procedure.

## 3 Learn from pg-aiguide and trace a recommendation

Timescale's pg-aiguide provides the real implementation reference for the teaching patterns in this workshop. Our [sourced lessons](EXECUTION_PLAN.md#what-we-learned-about-developer-education-from-pg-aiguide) explain the reviewed implementation and how we apply it here:

- **Make the right guidance discoverable during a task.** Give the agent a clear entry point and conditions for using the advice.
- **Pair reference material with judgment.** Supply the relevant facts along with a recommended path and its rationale.
- **Write defaults with exceptions.** Explain what would change the recommendation and which missing information requires a question.
- **Separate evidence from inference.** Show what is known, what was assumed, and how to verify the result.
- **Check transfer.** Ask whether the attendee can explain and apply the reasoning in a changed scenario. This is our learning check for the workshop.

Follow this path in the repository:

```text
JSON-API-MCP/content/practice.json
       ↓ loaded and validated at startup
MCP tool description and practice handler
       ↓ tool result includes applied rule and rationale
Copilot's recommendation in the editor
```

The same JSON also generates [PRODUCT_GUIDANCE.md](JSON-API-MCP/PRODUCT_GUIDANCE.md) for human readers. Editing the source changes the next server startup; running the renderer updates the human document.

The key question is: can you explain why the rule applies, identify its source, and describe its exception?

## 4 Run your own guide

Complete [setup](#start-in-your-editor) if you have not already done so. In a fresh guide chat, paste this exercise prompt. Keep it for Part 5:

> Use only MCP tools from education-guide for this request; do not read or edit workspace files. Give me a beginner practice round in Developer Tools. Explain your recommendation and identify its guidance source. Omit clue_count so the server's documented default applies.

With the shipped content, expect **two clues with answers hidden**. Expand the `get_guidance` and `build_practice_set` calls. In the practice result's `guidance` array, find the entry with `rule_id: practice.default_count`:

| Field | What to look for |
|---|---|
| `source` | `content/practice.json`, relative to `JSON-API-MCP` |
| `source_field` | `/rules/0/value` |
| `configured_value` and `applied_value` | `2` |
| `decision_basis` | `default` |
| `rationale` | Why a short round is recommended |
| `content_revision` | A hash identifying the loaded content file |

The model's wording can vary. Use the tool result to verify which rule actually shaped the set. If you have edited the fixture previously, check its current value before expecting two clues.

**Checkpoint:** You can retrieve a practice round and locate the source of its count recommendation.

## 5 Edit guidance and observe the change

### Change one rule

Open [JSON-API-MCP/content/practice.json](JSON-API-MCP/content/practice.json). Find the rule with ID `practice.default_count` and change its value from two to three:

```json
"value": 2
```

becomes:

```json
"value": 3
```

Save the file. Run **MCP: List Servers → education-guide → Restart Server**. Confirm the `build_practice_set` description reflects three clues; refresh the host's tool list if needed.

### Repeat the same task

Start a **fresh chat** with the same model and paste the **exact Part 4 prompt**. Keep the code and dataset unchanged.

Expect three clues, the same `practice.default_count` rule ID, an applied value of `3`, and a changed `content_revision`. Compare the explanation with the rule's rationale.

If the agent passes a `clue_count` despite the prompt, inspect that argument and ask it to omit the parameter. An explicit count overrides the server default and can mask your edit. Record the initial outcome when evaluating the demo.

### Update the human documentation

From the repository root, run:

```bash
uv run --locked --directory JSON-API-MCP python scripts/render_guidance.py
```

Open [PRODUCT_GUIDANCE.md](JSON-API-MCP/PRODUCT_GUIDANCE.md). Find the same rule and its updated three-clue recommendation. Edit the JSON source for future changes; the Markdown is generated.

### Check the exception

Ask:

> Give me one Developer Tools clue, then explain why you used one instead of the default.

Expect one clue and `decision_basis: explicit_user_choice`. Discuss why the default yields to a valid user choice. To reveal a practice answer, explicitly ask for it by clue ID; the separate `reveal_answer` tool returns it.

The response model enforces answer omission from a practice set. The agent is instructed to reveal an answer only when asked; that instruction depends on the agent honoring it.

**Checkpoint:** You can connect a changed result to your exact edit and explain when the rule should yield to another choice. [EXERCISE.md](EXERCISE.md) provides the dedicated exercise sheet and reflection questions.

## 6 Take away a product example

The final example recommends a deployment environment. It gives advice and performs no deployment. It is already included in `education-guide`, so you can continue without another installation.

### Observe the default

In a fresh chat, ask:

> Use only MCP tools from education-guide; do not read or edit workspace files. Recommend my next deployment step. Explain why and identify the product guidance you used. Omit target so the documented default applies.

With the shipped content, expect **preview**, citing `deployment.default_environment` in `content/deployment.json`.

### Edit and repeat

Open [JSON-API-MCP/content/deployment.json](JSON-API-MCP/content/deployment.json). Change only the `deployment.default_environment` value from `preview` to `staging`. Save, restart `education-guide`, and repeat the **identical prompt** in a fresh chat.

Expect **staging**, the same source rule, and an updated content revision. Regenerate the human docs using the command from Part 5.

### Try a request that needs a question

Ask:

> Skip the nonproduction step and recommend production now. I have not told you whether this change was verified outside production; do not assume that it was.

Expect the configured nonproduction recommendation and this question:

> Has this change been verified in a nonproduction environment?

Find `deployment.production_readiness` in the tool result. This applies the pg-aiguide lesson of asking for a missing fact that changes the recommendation. If you explicitly confirm verification, the tool can recommend production; your confirmation is an input, not independent proof of release readiness.

### Carry the pattern into your product

Pick one recurring support or onboarding question. Write down:

- The recommended first step and why it helps.
- When the advice applies, its exception, and what to ask when information is missing.
- One example request, its expected recommendation, and a way to verify the result.

Use [TAKEAWAY.md](TAKEAWAY.md) for the deployment exercise and explicit pg-aiguide learnings. To create a separate guide with your own tasks and context, follow [Build your own MCP server](#build-your-own-mcp-server). The copyable template supports new recommendation tasks through JSON and Markdown; tools that perform product operations need their own handlers.

**Checkpoint:** You can map a real product recommendation into the scaffold and explain how it reaches the agent.

## 7 Explain what you learned

Before leaving, explain these to another attendee or use them as a self-check:

- **Trace:** Which rule shaped the recommendation, and why did it apply?
- **Observe:** What changed after your edit, and which tool-result fields establish that connection?
- **Adapt:** What rule would you add for your own product? How would your advice change in a different scenario?

To repeat the original exercises, manually restore `practice.default_count` to `2` and `deployment.default_environment` to `preview`, regenerate the human docs, and restart the guide. Preserve any other edits you want to keep.

## Build your own MCP server

The [mcp-server-template](mcp-server-template/README.md) folder is a standalone project you can take away. It includes a server, sample context, editor configuration, a lockfile, generated human documentation, and tests. It does not depend on Jeopardy, the workshop API, or a database.

### 1 Copy it into a new project

Start in the workshop repository root:

```bash
python3 mcp-server-template/copy_template.py ../my-product-guide
cd ../my-product-guide
uv sync --locked
```

Choose a new destination folder you own. The helper refuses to overwrite an existing folder and omits virtual environments and caches. All remaining commands in this section run from the **copied folder**.

### 2 Add your product context

Edit `context/guide.json`:

- Set `product_name` to your product or codebase name.
- Replace the sample task with a recurring user question. Give it a unique `id`, a title, and a description of when the advice applies.
- Define its `choices`: each needs an ID, recommendation, rationale, and any required facts. Set `default_choice` to a choice with no required facts.
- Add a question in `fact_questions` for every required fact, plus an anti-pattern and a worked example.

Replace `context/product.md` with your own reference material. Add more Markdown files inside `context/` and list their relative paths in the task's `references`. Unlisted files are not loaded. Add more objects to the `tasks` array to teach additional decisions; no Python edit is needed for this recommendation structure.

The template's [field-by-field instructions](mcp-server-template/README.md#3-replace-the-context-with-your-own) explain the full format. The same README is included in your copied project.

### 3 Validate and render your context

```bash
uv run --locked python server.py --check
uv run --locked python render_context.py
```

The first command reports the product name and task count, or the location of invalid context. Review `CONTEXT_GUIDE.md` to see the same rules and documents the agent will receive.

### 4 Connect it to your editor

Open **the copied folder** in VS Code. Its `.vscode/mcp.json` launches the template automatically through uv. Run **MCP: List Servers → my-product-guide → Start Server** and select `list_tasks`, `get_guidance`, and `recommend_next_step`.

In a fresh agent chat, ask:

> Use only my-product-guide tools. List the available tasks, read the guidance for the relevant task, and recommend a next step. Omit choice so the documented default applies. Explain why and cite the context source.

Inspect the returned `guidance_sources`: each source identifies a file, a JSON pointer, and the revision loaded at startup. `get_guidance` also returns the Markdown reference documents for the task.

### 5 Edit and verify your own recommendation

Change the task's `default_choice` to another choice with no required facts. Validate, render the docs, restart the server, and repeat the exact prompt in a fresh chat. Look for the new recommendation and changed source revision. Then request a choice that requires a missing fact and check the returned question.

Run the supplied checks:

```bash
uv run --locked ruff check .
uv run --locked pytest
uv run --locked python verify.py
```

The tests include assertions for the sample deployment context; adapt those assertions when replacing that example. The protocol verifier needs two unrestricted choices in the first task to demonstrate the default edit. It tests a temporary copy and preserves your files.

For new product operations, add validated task tools and handlers in `server.py`. The template already supplies context loading, recommendations, source tracing, and MCP transport. Its [standalone README](mcp-server-template/README.md) also includes explicit pg-aiguide learnings and extension instructions.

**Checkpoint:** Your own project runs independently, serves your context, and changes its recommendation after a context edit. Return to the workshop repository root before using the workshop maintainer commands below.

## Troubleshooting

| Symptom | What to do |
|---|---|
| No guide tools appear | Open the repository root, trust the workspace, sign in to Copilot, use Agent mode, and start `education-guide`. |
| You see only three clue tools | You opened the nested wrapper workspace. Open the repository root for the guide. |
| VS Code cannot find uv | Replace `"uv"` in the active MCP configuration with the absolute path from `which uv` or `where uv`. In the configured Codespace, try `/home/vscode/.local/bin/uv`. |
| Behavior stays unchanged after an edit | Save, restart, refresh tool descriptions, and start a fresh chat. Inspect optional arguments such as `clue_count` or `target` that may override the default. |
| Guidance fails validation | Read the file and rule location in the error. The practice default accepts integers from 1 to 10; the deployment default accepts `preview` or `staging`. |
| Generated documentation is stale | Run the documentation renderer from Part 5 after changing content. |

For startup diagnostics, run this from the repository root:

```bash
uv run --locked --directory JSON-API-MCP python -m jeopardy_template.launcher --server guide
```

A healthy stdio server waits for an MCP host. Use VS Code to converse with it; logs belong on stderr. Stop the terminal process with Ctrl+C.

## Verify the scaffold

These checks are useful for maintainers and anyone adapting the code; they are separate from the timed attendee exercise. Run them from the repository root:

```bash
uv run --locked --directory JSON-API-MCP ruff check .
uv run --locked --directory JSON-API-MCP pytest
uv run --locked --directory JSON-API-MCP python scripts/render_guidance.py --check
uv run --locked --directory JSON-API-MCP python scripts/verify_workshop.py
```

The last command starts real stdio servers, verifies both content edits using temporary copies, and leaves your working guidance intact. It requires localhost binding.

Protocol checks and local Copilot smoke comparisons pass. Five-run comparisons, clean installation, Codespaces, a second MCP host, and timed attendee rehearsal remain open. See [verification evidence](evidence/README.md) for the tested configuration and observed results.

## Continue after the talk

| Material | Use it for |
|---|---|
| [Exercise sheet](EXERCISE.md) | Repeat the practice edit and reflection questions. |
| [Deployment takeaway](TAKEAWAY.md) | Run and adapt the final product example; review explicit pg-aiguide learnings. |
| [Standalone MCP server template](mcp-server-template/README.md) | Copy a working project and create a guide with your own context, tasks, and reference docs. |
| [Product guidance](JSON-API-MCP/PRODUCT_GUIDANCE.md) | Read the human documentation generated from the rule files. |
| [Presenter outline](OUTLINE.md) and [demo runbook](DEMO.md) | Deliver and rehearse the session. |
| [Execution plan](EXECUTION_PLAN.md) and [checklist](NEXT_STEPS.md) | Track implementation and remaining validation. |
| [Background tutorial](TUTORIAL.md) | Study the JSON, FastAPI, and MCP construction after the workshop. |
| [Manual API instructions](JSON-API-MCP/INSTRUCTIONS.md) and [dataset adaptation](JSON-API-MCP/ADAPTATION_EXERCISE.md) | Explore the infrastructure and replace the data domain. |
