# Goodbye, Tutorial Hell: AI Guides and the New Documentation Layer

**Speakers:**  Erin Mikail Staples and Janice Niemeir

**Format:** 45-minute sandbox session with a working scaffold and attendee exercises

**Audience:** Intermediate developers, maintainers, and product teams

## Original prospectus

For years, "developer education" has meant read the docs and hope. And most MCP servers are just API wrappers with extra steps. What if the server could teach instead? When an AI agent in GitHub Copilot or another MCP-compatible editor reads documentation through an opinionated MCP server, it stops giving generic advice and starts teaching the way your product is meant to be used. Janice Niemeir  and Erin Mikail Staples show the difference live: you'll fork an open source reference server, install it in your editor, and watch agent behavior change side by side. You'll leave with a working scaffold you can adapt for your own product or codebase.

## Acceptance criterion

An attendee can trace a recommendation to guidance they edited, observe its effect in their editor, and adapt that pattern to their own product.

The exercise uses Jeopardy practice to make the first change easy to inspect. The final example is a standalone deployment-advice guide that carries a product default, an exception, and a question about missing evidence.

## Session timing

| Block | Minutes | Running total |
|---|---:|---:|
| 1. Developer education problem and session promise | 5 | 5 |
| 2. Wrapper and guide comparison | 7 | 12 |
| 3. What we learned and tracing a recommendation | 6 | 18 |
| 4. Fork, install, and verify | 8 | 26 |
| 5. Edit guidance, restart, and observe | 6 | 32 |
| 6. Adapt the pattern to a product | 5 | 37 |
| 7. Questions, recovery time, and leave-behinds | 8 | 45 |

## Before the session

- Put the repository link and [quickstart](README.md#start-in-your-editor) on screen.
- Invite attendees to fork and clone, or create a Codespace on their fork.
- Use the [demo runbook](DEMO.md) for model/settings records, prompts, and actual observations.
- Prepare a recording or screenshots from a verified run and label them as recorded results if used.

## 1 Developer education problem and session promise

- A tutorial can get you to a first success. Your own project introduces choices the tutorial never made for you.
- Product judgment already appears in support answers, onboarding, and code review. Make that advice available while the developer is doing the task.
- Promise the concrete loop: find the recommendation, inspect the rule, edit it, rerun, and adapt the pattern.
- Distinguish reliable data access, documented advice, and behavior enforced by code.

## 2 Wrapper and guide comparison

- Open the repository root for the guide and the nested `JSON-API-MCP` folder in another window for the wrapper. Give each chat only its assigned server's tools.
- Use the same model, prompt, API fixture, and fresh chat context.
- Run the beginner prompt from `DEMO.md` in both windows. Inspect what each tool returns, answer visibility, and whether the agent explains a recommendation.
- The wrapper may produce a good response. Identify which decisions the model inferred and which the server supplied.
- Show the guide's rule, rationale, applied value, and content revision. The comparison changes the tool surface and guidance together; the later same-guide edit isolates the content change.
- Use the difficulty prompt to discuss the limits of board value. Never claim the wrapper is guaranteed to fail or that more tools prove a worse learning experience.

## 3 What we learned about developer education

- Use the [explicit pg-aiguide lessons](EXECUTION_PLAN.md#what-we-learned-about-developer-education-from-pg-aiguide) as the real implementation reference.
- **Teach a decision when it is needed.** Follow a user task to its applicable guidance.
- **Pair reference with judgment.** pg-aiguide's documented API provides documentation search and curated skills; its task entry point routes requests to relevant references.
- **State conditions and missing information.** Its hypertable skill asks about unknown retention requirements. Our deployment example asks whether nonproduction verification occurred.
- **Separate evidence and inference.** Its schema-exploration skill models that distinction. User confirmation is evidence of a statement, not independent proof that tests passed.
- Trace `practice.default_count` from JSON to generated human documentation, the MCP description, and the returned recommendation.
- Explain the mechanism: the count is an executable default, answers are omitted by the response model, and conceptual-difficulty advice must be used by the agent.
- Ask attendees to explain why the recommendation applies and what would change it.

## 4 Fork install and verify

- Follow the root quickstart: fork, open, sync, start `education-guide`, and select its tools.
- The launcher starts the local API and MCP together on a private ephemeral port.
- Confirm the four guide tools appear and run the beginner prompt.
- Check the actual MCP result for the source rule and applied value. Resolve setup failures using the README.
- Keep the optional infrastructure tutorial available for later reading.

## 5 Edit guidance restart and observe

- Follow [EXERCISE.md](EXERCISE.md): change the default count from two to three in `content/practice.json`.
- Restart, refresh tool descriptions as needed, and run the same prompt in a fresh chat.
- Inspect three clues, the same rule ID, and the changed content revision.
- Inspect tool arguments if the agent supplies an unrequested explicit count; omit it to exercise the default.
- Run the one-clue exception. Ask why a valid explicit user choice takes precedence.
- Explain how the same content generates human documentation and agent guidance.

## 6 Adapt the pattern to a product

- Open [TAKEAWAY.md](TAKEAWAY.md) and demonstrate the standalone deployment guide.
- Ask for a next deployment step, trace the preview recommendation, edit the default to staging, restart, and repeat.
- Ask to go directly to production. Inspect the question about verification and the rule behind it. The tool gives advice and performs no deployment.
- Ask attendees for a recurring support question. Capture the recommendation, rationale, exception, example, and source using the takeaway template.
- Distinguish a content change from implementing a new domain task. The scaffold reuses loading, validation, source tracing, and transport.
- Ask how the advice should change in a different scenario. Understanding includes explaining when the rule stops applying.

## 7 Questions and leave-behinds

- Invite a short explanation of one attendee's rule and the evidence of its effect.
- Leave the quickstart, exercise, takeaway, product guidance, and pg-aiguide source links on screen.
- Seed questions: What recurring support answer belongs in your guide? Which missing fact should make it ask a question? How will you notice guidance becoming stale?
- Close on the acceptance criterion: trace the recommendation, observe your edit, and adapt the reasoning to your product.

## Remaining validation

Protocol tests establish server behavior. Editor/model comparisons, a clean-machine and Codespaces install, a second host, and a timed attendee rehearsal still need observed records. Track those in [NEXT_STEPS.md](NEXT_STEPS.md) and [evidence/README.md](evidence/README.md).
