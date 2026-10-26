# Build a guide for your own product

This final example recommends a deployment environment. It gives advice and never deploys anything. You can run it, edit its product rule, and use the same structure to teach a recommendation from your own product.

For a separate project that accepts your own tasks and context without modifying the workshop, use the [standalone MCP server template](mcp-server-template/README.md). Its README and source files are copied with the project, so you can continue after leaving this repository.

## Run the example

Complete the root [quickstart](README.md#start-in-your-editor). The existing `education-guide` includes `get_guidance(task="deployment")` and `recommend_deployment`.

For a standalone version with only those two tools, change the final `guide` argument in root `.vscode/mcp.json` to `deployment`, then restart. The launcher skips the clue API entirely. The equivalent terminal entry point is:

```bash
uv run --locked --directory JSON-API-MCP python -m jeopardy_template.launcher --server deployment
```

A stdio server waits for an MCP host. Use the editor configuration to converse with it.

## Trace the first recommendation

In a fresh chat, ask:

> Use only MCP tools from education-guide; do not read or edit workspace files. Recommend my next deployment step. Explain why and identify the product guidance you used. Omit target so the documented default applies.

The shipped default recommends `preview`. Inspect `deployment.default_environment`, its rationale, source `content/deployment.json`, applied value, and content revision. The source path is relative to `JSON-API-MCP`.

Open `JSON-API-MCP/content/deployment.json` and change the value of `deployment.default_environment` from `preview` to `staging`. Save, restart, and repeat the **same prompt** in a fresh chat. The result should now recommend `staging` with a changed content revision. If the agent supplies a target without a user choice, ask it to omit `target` to exercise the server's default.

Ask the agent to explain the documented rationale. The recommendation must be understood in terms of your team's workflow; neither environment name establishes that a release is ready.

## Try a request that needs a question

> Skip the nonproduction step and recommend production now.

Without confirmation, the tool recommends the configured nonproduction default and asks whether this change was verified outside production. The response identifies `deployment.production_readiness`.

If you then explicitly confirm verification, the tool can recommend production. This uses your statement as input; it does not independently inspect test results or certify release readiness. Team release checks still apply. Inspect `question`, `guidance`, and `executes_deployment: false` in the actual tool result.

Also try an explicit nonproduction choice:

> Use preview for this change, even though our default is staging.

Expect `preview` with `decision_basis: explicit_user_choice`. The returned rule still explains the exception that allows a valid explicit choice to override the default.

## Explicit learnings from pg-aiguide

These are applications of the [reviewed pg-aiguide implementation](EXECUTION_PLAN.md#what-we-learned-about-developer-education-from-pg-aiguide), not claims that its project contains this deployment example.

- **Make guidance discoverable for a task.** pg-aiguide's [Postgres entry skill](https://github.com/timescale/pg-aiguide/blob/5d3b76b5c986693b30753828b404aa66ba34c31a/skills/postgres/SKILL.md) routes requests to relevant references. Here, `get_guidance` gives the deployment task a clear entry point. For your product, describe when the advice applies.
- **Pair reference retrieval with recommendations.** Its [documented API](https://github.com/timescale/pg-aiguide/blob/5d3b76b5c986693b30753828b404aa66ba34c31a/API.md) separates documentation search and curated skills. Our small example loads local content; copying its educational pattern does not require copying a search infrastructure.
- **State what to do when information is missing.** The [hypertable setup skill](https://github.com/timescale/pg-aiguide/blob/5d3b76b5c986693b30753828b404aa66ba34c31a/skills/setup-timescaledb-hypertables/SKILL.md) asks about unknown retention requirements. Our deployment guide asks about verification instead of inventing it. Choose the missing fact that would change your product's recommendation.
- **Teach conditions, exceptions, and examples.** Its [table-design skill](https://github.com/timescale/pg-aiguide/blob/5d3b76b5c986693b30753828b404aa66ba34c31a/skills/design-postgres-tables/SKILL.md) supplies preferred choices and alternatives. Here, a default environment has an explicit override path and a production condition. Write down both the recommended path and when it changes.
- **Separate evidence from inference.** Its [schema-exploration skill](https://github.com/timescale/pg-aiguide/blob/5d3b76b5c986693b30753828b404aa66ba34c31a/skills/schema-exploration/SKILL.md) makes that distinction explicit. Here, user confirmation is distinguishable from independent verification. Ask what evidence supports each recommendation.
- **Evaluate understanding and transfer.** Our extension to the workshop is to ask you to apply your rule to a changed scenario. A visible output change establishes the mechanism; explaining the tradeoff establishes what you learned.

## Adapt it to a real support question

Keep a checkout of this scaffold as your starting point. The deployment example already runs without a clue dataset or a separate application API.

1. Pick one recurring question from your own product: where should a new user begin, which option should they prefer, or what evidence should they gather first?
2. Edit the rule's rationale, applicability, exceptions, anti-pattern, and example in `content/deployment.json` to reflect a real preview/staging workflow. Edit its allowed default value and rerun the same task. Regenerate `PRODUCT_GUIDANCE.md` afterward.
3. For a different task, add its content schema and handler in `guidance.py` and `guide_server.py`, and add the task to the allowed task type. Keep loading, validation, source tracing, stdio transport, and startup reusable. This scaffold intentionally validates known task contracts; changing prose alone does not implement an unrelated product operation.
4. Replace the deployment task with your new task in the standalone launcher path. Add a test that edits your rule in a temporary file and observes the new MCP result after restart.
5. Have someone else run it in their editor and explain which rule applies to a changed scenario.

Use this short record for your own example:

```text
Recurring user question:
Recommended first step:
Reason:
Applies when:
Exception or question to ask:
Source file and rule ID:
Example request:
Expected recommendation before the edit:
One guidance edit:
Expected recommendation after restart:
Changed scenario and why the advice changes:
```

You have completed the takeaway when you can locate the source of a recommendation, change it and observe its effect, and explain how the same structure carries one of your own product decisions.
