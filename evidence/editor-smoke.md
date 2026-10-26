# Observed editor smoke checks

Observed in local VS Code 1.140.0 on October 26, 2026. The repository root was opened in a separate window and `education-guide` was started through **MCP: List Servers**. VS Code reported a running connection and discovery of four tools.

Copilot used Agent mode, Auto model selection with Balance, and default permissions. The completed responses identified **GPT-6 Luna**. Global tool settings were preserved; prompts restricted the request to the guide and prohibited workspace reads/edits. The agent also used its todo facility. These are smoke checks, rather than a fully isolated or five-run comparison.

## Practice before and after one content edit

The identical prompt was sent in two fresh chats:

```text
Use only MCP tools from education-guide for this request; do not read or edit workspace files. Give me a beginner practice round in Developer Tools. Explain your recommendation and identify its guidance source. Omit clue_count so the server's documented default applies.
```

| Observation | Before | After |
|---|---|---|
| Local response time shown | 09:21 | 09:23 |
| Model shown | GPT-6 Luna | GPT-6 Luna |
| Rule value in source file | 2 | 3 |
| Clue IDs displayed | 0, 2 | 0, 2, 3 |
| Answers displayed | None | None |
| Source cited | `content/practice.json` | `content/practice.json` |
| Rules cited | `practice.default_count`, `practice.answer_visibility`, `practice.difficulty` | Same three rules |

Between the chats, only the practice rule value was changed, human docs were regenerated, and the guide restart action was invoked. The second chat's tool-step summary confirmed that guidance specified three clues. Both responses explained that `clue_count` was omitted so the documented default applied, and both disclosed the limits of board value as a difficulty proxy.

The source-file hashes for this edit were calculated locally:

- Two-clue file: `c19bd5fd00f12cc7ef30ade5d4d2f4a5b63faf4f7e1ed7bc6f50d0de2f5550e1`
- Three-clue file: `534391e328482bf88dbb09655be605832aabe0a1e9e9ef81f3a113e77d971125`

Full JSON tool output was not exported from the editor. The separate [protocol record](protocol-verification.json) captures structured before/after results and verifies loaded source revisions through a real MCP client.

## Deployment before and after one content edit

Prompt in a fresh chat:

```text
Use only MCP tools from education-guide; do not read or edit workspace files. Recommend my next deployment step. Explain why and identify the product guidance you used. Omit target so the documented default applies.
```

At 09:25, the response identified GPT-6 Luna and recommended **preview**, explained that it lets the developer inspect behavior before exposing a change to users, cited `content/deployment.json` and `deployment.default_environment`, and stated that no deployment occurred. The tool-step summary recorded `get_guidance` for `deployment` and `recommend_deployment` with `{}` as its input.

The default value was then changed to `staging`, the human docs were regenerated, and the guide restart action was invoked. The identical prompt in a fresh chat at 09:27 produced **staging**, explained the nonproduction rationale, cited the same source and rule, and again stated that the advice performs no deployment. The response identified GPT-6 Luna, and the tool-step summary again recorded an empty input for `recommend_deployment`.

## Limits and next checks

At 09:29, a follow-up asked to skip nonproduction without assuming verification. The tool-step summary recorded `recommend_deployment` with only `target: production`. The GPT-6 Luna response recommended staging, asked “Has this change been verified in a nonproduction environment?”, and cited `deployment.production_readiness` in `content/deployment.json`. It stated that no deployment occurred.

After the smoke checks, the test server was stopped and VS Code's server list showed `education-guide` as stopped. The source defaults were restored to two clues and preview, and human documentation was regenerated so the next attendee starts from the shipped exercise state.

This record establishes observed editor integration and one content-edit comparison for each example. Five fresh runs, a wrapper/model comparison, description inspection after restart, a second host, a clean installation, Codespaces, and timed attendee comprehension/adaptation still require rehearsal. The tested prompts deliberately omit optional parameters; shorter natural prompts may lead the agent to supply them and should be evaluated separately.
