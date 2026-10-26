# Demo and rehearsal runbook

Use the root [quickstart](README.md#start-in-your-editor), [exercise](EXERCISE.md), and [takeaway](TAKEAWAY.md). This runbook describes observations to collect; it does not predeclare model outcomes.

## Comparison setup

- Window A: open `JSON-API-MCP`, start `jeopardy-basics`, and select only its three wrapper tools.
- Window B: open the repository root, start `education-guide`, and select only its four guide tools.
- Choose and record the same model and settings. Keep repository instructions consistent; do not add product answers to team instructions.
- Begin each run in a fresh chat. The launchers use the same bundled dataset and independent loopback API ports.
- Record the commit or working-tree snapshot, guidance revisions, editor version, model, tool arguments, tool results, and final response.

## Prompts and observations

| Prompt | Observe |
|---|---|
| Give me a beginner practice round in Developer Tools. Explain your recommendation and identify its guidance source. | Tool selection, count arguments, answer visibility, source attribution, and explanation of the recommended progression. |
| Does the highest board value mean this is objectively the hardest clue for me? I want to improve at debugging MCP servers. | Whether the agent discloses the proxy's limits, asks about goals, and avoids inventing matching content. |
| Spare: Give me ten Developer Tools clues without changing the category. | Whether the response acknowledges the three matching records and preserves the category. |

The wrapper can succeed. Note which recommendations the model inferred versus those supplied by the server. This comparison changes both tool design and guidance.

## Isolate the content edit

Follow `EXERCISE.md`: two clues → three clues, restart, refresh descriptions, fresh chat, identical prompt. Inspect the tool arguments; an agent-invented explicit count can mask the default. Acknowledge it and rerun with the count omitted. Record the initial outcome too.

For the final product example, follow `TAKEAWAY.md`: preview → staging, restart, identical prompt. Then request production without verification and inspect the question and rule. Confirm verification only when explicitly supplied by the user.

The source revision identifies the loaded content. The tool trace establishes server behavior. The final response establishes what the agent used and explained.

## Reset between rehearsals

- Stop both MCP servers through the host controls; their local APIs stop with them.
- Preserve your edits before restoring any fixture. To restore the demo manually, set `practice.default_count` to `2` and `deployment.default_environment` to `preview` in their source files.
- Run the documentation renderer and restart the servers. Confirm the descriptions match the intended starting values.
- Use fresh chats and reselect the assigned tools. If you switched the root config to `deployment`, set it back to `guide` for practice.
- The protocol verifier uses temporary content copies, so it can be rerun without resetting your working files.

## Rehearsal record

For each primary scenario, collect five fresh runs with a recorded model and settings. Record failures and revise the guidance or setup based on the evidence. Protocol runs do not fill these editor-result cells.

| Scenario | Run 1 | Run 2 | Run 3 | Run 4 | Run 5 |
|---|---|---|---|---|---|
| Guide practice recommendation and source | Two clues and rule cited; [smoke record](evidence/editor-smoke.md) | Pending | Pending | Pending | Pending |
| Guide after count edit | Three clues and same rule cited; [smoke record](evidence/editor-smoke.md) | Pending | Pending | Pending | Pending |
| Difficulty limitation and next question | Pending | Pending | Pending | Pending | Pending |
| Deployment after default edit | Staging and rule cited; [smoke record](evidence/editor-smoke.md) | Pending | Pending | Pending | Pending |
| Production request with missing evidence | Verification question and rule cited; [smoke record](evidence/editor-smoke.md) | Pending | Pending | Pending | Pending |

Also record a clean local installation, Codespaces installation, a second MCP host, the eight-minute installation and six-minute exercise, and a full 45-minute session with a reviewer unfamiliar with the code.

If a recorded fallback is needed, label it with its scenario and tested configuration. Use actual captured results and disclose that it is a recording.
