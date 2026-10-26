# Edit guidance and observe a recommendation

The goal is to trace a recommendation to a rule you can change. First complete the [quickstart](README.md#start-in-your-editor). Keep the model, prompt, code, and dataset the same throughout this exercise.

## 1 Observe the shipped recommendation

Start a fresh chat with only `education-guide` tools selected:

> Use only MCP tools from education-guide for this request; do not read or edit workspace files. Give me a beginner practice round in Developer Tools. Explain your recommendation and identify its guidance source. Omit clue_count so the server's documented default applies.

Inspect the `get_guidance` and `build_practice_set` results. With the shipped content, expect two clues with no `answer` fields. Find:

- `rule_id`: `practice.default_count`
- `source`: `content/practice.json` (relative to `JSON-API-MCP`)
- `source_field`: `/rules/0/value`
- `configured_value` and `applied_value`: `2`
- `content_revision`: the SHA-256 of the loaded content file
- `rationale`: why a short round is recommended

If the model supplies a count explicitly, inspect its arguments. Ask it to omit `clue_count` so the server's default is exercised. Explicit user choices take precedence over defaults; an agent-supplied argument can mask a default change.

## 2 Make one content edit

Open `JSON-API-MCP/content/practice.json`. In the rule with ID `practice.default_count`, change only:

```json
"value": 2
```

to:

```json
"value": 3
```

Save, stop, and restart `education-guide` in the MCP controls. Check that the `build_practice_set` description now says “Start with 3 clues.” Refresh the host's tool list if it still shows the old text.

## 3 Observe the change

Use a fresh chat and the **exact same prompt**. Confirm three clues, the same rule ID, an applied value of three, and a changed content revision. Ask the agent why this recommendation applies and when it should use a different count.

Generate the matching human documentation from the root:

```bash
uv run --locked --directory JSON-API-MCP python scripts/render_guidance.py
```

Open `JSON-API-MCP/PRODUCT_GUIDANCE.md` and find the same default and rationale. The example text and tool description interpolate the configured value rather than maintaining a second copy of the number.

## 4 Check an exception and a changed scenario

> Give me one Developer Tools clue, then explain why you used one instead of the default.

Expect one clue with `decision_basis: explicit_user_choice`. Now ask:

> Does the highest board value mean this is objectively the hardest clue for me? I want to improve at debugging MCP servers.

The agent should explain the proxy's limits and ask about relevant goals or available material. Inspect the difficulty guidance rather than treating its answer as proof. Discuss how this scenario changes the recommendation.

The count is an executable default. Answer omission is enforced by the practice response model. The agent is instructed to call the separate reveal tool only on an explicit learner request; the server cannot independently read the user's intent. The difficulty explanation is advice the agent must use; its wording and use require editor rehearsal.

## 5 Capture what you learned

- Which exact rule shaped the first recommendation?
- What changed after your edit, and what evidence connects it to that edit?
- When should the default yield to an explicit user choice?
- What recommendation would your own users benefit from, and when should the agent ask a question instead?

Continue with the runnable product example in [TAKEAWAY.md](TAKEAWAY.md). To repeat the original practice exercise, manually restore this rule's value to two, regenerate the docs, and restart. Preserve any other content edits you want to keep.
