# Execution plan for the teaching MCP workshop

The priority is to deliver the experience promised in the prospectus: fork a reference server, install it in an editor, compare its behavior with a wrapper, and adapt its guidance to another product. The existing JSON → FastAPI → MCP implementation supplies the working baseline.

**Acceptance criterion:** An attendee can trace a recommendation to guidance they edited, observe its effect in their editor, and adapt that pattern to their own product.

The next implementation milestone is one complete version of that experience. Additional tools, slides, and production examples follow once the experience passes its checks.

**Implementation status:** The guide, source tracing, generated docs, managed startup, practice exercise, runnable deployment takeaway, and [standalone context-driven template](mcp-server-template/README.md) are implemented. See [verification evidence](evidence/README.md) and the [checklist](NEXT_STEPS.md) for the distinction between completed implementation and remaining attendee validation.

Track the work in the [next steps checklist](NEXT_STEPS.md).

## Scope and decisions

- Retain the synthetic Jeopardy dataset and existing API for the first implementation. Treat the practice application as a small product with documented usage recommendations.
- Preserve `jeopardy-basics` as the accurate wrapper. Its behavior supplies the control for the demonstration.
- Add a separate guide server using the same API and data. Begin with the practice task and only the tools needed to explain guidance, build a practice set, and reveal an answer on request.
- Store product guidance in one structured content file. Generate human documentation and MCP guidance from that source.
- Make the primary exercise a content edit. Attendees can complete the first loop without changing Python, API contracts, or data models.
- Use the same recorded model and editor settings for comparisons. Model selection is a rehearsal decision, with an accessible option tested before the workshop.

The original prospectus does not require thirty wrapper tools or six guide tools. Tool counts will follow the teaching task. The tutorial will lead with fork, install, compare, edit, and adapt; the infrastructure walkthrough becomes optional background.

## What we learned about developer education from pg-aiguide

Timescale's pg-aiguide supplies a concrete model for bringing product expertise into a developer's existing workflow. These lessons come from its public implementation at [revision 5d3b76b](https://github.com/timescale/pg-aiguide/tree/5d3b76b5c986693b30753828b404aa66ba34c31a). The workshop applications below are our design conclusions from that implementation.

### Teach a decision at the moment it is needed

pg-aiguide combines documentation search with curated PostgreSQL and TimescaleDB skills, and distributes that expertise through MCP and native agent skills. This puts guidance alongside the developer's schema or query task. [Source: project overview](https://github.com/timescale/pg-aiguide/blob/5d3b76b5c986693b30753828b404aa66ba34c31a/README.md).

**Workshop application:** Start with a real user request. Show the decision the developer needs to make, the guidance the agent receives, and the resulting recommendation. Installation and successful tool calls are prerequisites; the educational outcome is a decision the attendee can explain and apply again.

### Reference material and judgment serve different purposes

The documented API provides `search_docs` for reference retrieval and `view_skill` for curated guidance; native plugin deployments can supply skills directly. PostgreSQL documentation search is scoped by version. The Postgres skill entry point routes tasks to specialized references. [Sources: API](https://github.com/timescale/pg-aiguide/blob/5d3b76b5c986693b30753828b404aa66ba34c31a/API.md), [task routing](https://github.com/timescale/pg-aiguide/blob/5d3b76b5c986693b30753828b404aa66ba34c31a/skills/postgres/SKILL.md).

**Workshop application:** Let the agent retrieve the applicable guidance before recommending an action. A small content lookup is sufficient for our fixture; a vector database is unnecessary for this proof. Tool count does not measure teaching quality. What matters is whether the right guidance reaches the right task with enough context to apply it.

### A useful default includes its conditions and exceptions

The table-design skill gives preferred choices and alternatives, such as identity columns for ordinary identifiers and UUIDs when global uniqueness or opacity is needed. The hypertable skill relates configuration choices to query patterns and row density, and tells the agent to ask about retention rather than invent a period. These are examples of how the project encodes judgment, rather than universal prescriptions for every database. [Sources: table design](https://github.com/timescale/pg-aiguide/blob/5d3b76b5c986693b30753828b404aa66ba34c31a/skills/design-postgres-tables/SKILL.md), [hypertable setup](https://github.com/timescale/pg-aiguide/blob/5d3b76b5c986693b30753828b404aa66ba34c31a/skills/setup-timescaledb-hypertables/SKILL.md).

**Workshop application:** Give each teaching rule a recommendation, rationale, conditions, exception or clarifying question, and example. Explain when an explicit user choice overrides a default. In the practice guide, disclose the limits of board value as a difficulty proxy and ask about the learner's goal when that affects the recommendation.

### Teach an observable reasoning process

The schema-exploration skill begins with the user's question, inspects relevant objects, and separates observed facts, inferred meaning, and unresolved questions. It explicitly distinguishes a valid query plan from evidence of business meaning. [Source: schema exploration](https://github.com/timescale/pg-aiguide/blob/5d3b76b5c986693b30753828b404aa66ba34c31a/skills/schema-exploration/SKILL.md).

**Workshop application:** Have the guide explain what information supports its recommendation, what assumption remains, and how the learner can check the result. Our source rule IDs and content revisions make that process inspectable. A prose instruction influences an agent; a handler enforces a result constraint. Teach the distinction and test each through its own mechanism.

### Maintenance is part of educational quality

pg-aiguide's ingestion documentation describes scheduled documentation refreshes and coordination between ingested versions and searchable sources. Its task content also records version-sensitive behavior. [Sources: ingestion workflow](https://github.com/timescale/pg-aiguide/blob/5d3b76b5c986693b30753828b404aa66ba34c31a/ingest/README.md), [hypertable setup](https://github.com/timescale/pg-aiguide/blob/5d3b76b5c986693b30753828b404aa66ba34c31a/skills/setup-timescaledb-hypertables/SKILL.md).

**Workshop application:** Treat guidance updates as behavior changes: review the source, update derived docs, and rerun a representative task. Our one-source documentation renderer is a workshop implementation choice; the cited project does not establish that every human and agent document is generated from one source.

### Evaluate the developer's judgment as well as the generated artifact

The pg-aiguide README reports a schema comparison with four times as many constraints and 55 percent more indexes when its server was enabled. Those are results from the project's demonstration, not a general performance benchmark or evidence of learner comprehension. [Source: reported comparison](https://github.com/timescale/pg-aiguide/blob/5d3b76b5c986693b30753828b404aa66ba34c31a/README.md#see-the-difference).

**Workshop application:** Review whether a recommendation fits the task and whether the attendee understands its tradeoff. More indexes, more text, or more tool calls are insufficient measures of quality. After the content edit, give the attendee a changed scenario and ask which rule applies, why, and what information would change the recommendation. This checks transfer beyond repeating the demo.

For this workshop, building developer education means making expertise discoverable during a task, explaining its conditions, showing how to verify the result, and helping the developer carry that reasoning into the next task. The two-to-three edit establishes traceable behavior change; the explanation and adaptation exercises establish the educational outcome.

## The attendee experience to build first

Use the exact prompt below in a fresh editor chat:

> Give me a beginner practice round in Developer Tools.

The shipped guidance recommends starting with two clues. The guide returns a two-clue practice set with answers hidden, a short explanation, and a reference to the rule behind its recommendation.

The attendee opens the referenced guidance file, changes the default practice count from two to three, saves it, and restarts the guide. They use the same prompt in another fresh chat. The guide now returns three clues and identifies the updated guidance. The fixture already contains three Developer Tools clues, so this exercise requires no dataset changes.

The trace should be understandable to an attendee:

```text
Recommendation: Start with three clues for this practice round.
Reason: Use a short round so the learner can review mistakes before continuing.
Source: content/practice.json
Rule: practice.default_count
Applied value: 3
```

The tool result also includes a content revision derived from the source. Keep that diagnostic in the tool details; the conversational explanation only needs the recommendation, reason, and source reference.

The count example proves the content-to-behavior loop. A second example demonstrates product judgment: explain that board value is a rough difficulty proxy and redirect requests that treat it as a universal measure of conceptual difficulty. Include a documented reason and recommended alternative.

## Milestone 1 Define the guidance contract

**Deliverables**

- Add `JSON-API-MCP/content/practice.json` with stable rule IDs, values, rationale, applicability, exceptions or clarifying questions, anti-patterns, and worked examples.
- Define a validated content model and explicit precedence: product constraints apply first, valid explicit user choices apply next, and defaults fill omitted choices.
- Distinguish executable rules, such as a default count, from advisory guidance, such as interpreting board value. Document which mechanism each rule uses.
- Add a deterministic documentation renderer and a generated human-readable practice guide. Examples and descriptions interpolate rule values so editing a default does not leave contradictory numbers elsewhere.
- Keep development team norms in repository instructions and product usage guidance in the content file.

**Completion check:** A reader can locate each rule, explain its rationale, and identify where its value and wording enter the guide. Invalid content fails startup with the file and rule location. A renderer check detects stale generated documentation.

## Milestone 2 Deliver the guide and prove the content edit

**Deliverables**

- Add a separate guide module and editor configuration alongside the existing wrapper.
- Implement the smallest useful task surface: retrieve practice guidance, build a practice set, and reveal an answer when requested. Final tool names can follow existing naming conventions.
- Load and validate guidance at startup. Use it to construct tool descriptions and apply executable defaults. Every tool continues to use the existing API boundary for clue access.
- Return the applied rule ID, source location, applied value, rationale, and content revision with recommendations. Provenance must come from the content actually used by the handler.
- Use a practice response model that omits answers until a reveal is requested. State when too few records match; preserve an explicit user count when it is valid and feasible.
- Ask the agent through server guidance to explain the recommendation and cite its source. Verify that behavior in the editor.

**Completion check:** The two-to-three edit changes the actual practice set and its explanation through a real MCP client after a restart. REST behavior and the wrapper remain unchanged. An explicit valid count overrides the default, and shortage behavior stays truthful.

This milestone establishes the core implementation. Continue to attendee packaging only after it works.

## Milestone 3 Make both comparisons reproducible

There are two comparisons, serving different purposes:

| Comparison | What stays constant | What changes | What it establishes |
|---|---|---|---|
| Wrapper versus guide | Model, prompt, API, dataset, editor settings | Tool interface and supplied guidance | How a guide supports a task and exposes product recommendations |
| Guide before versus after an edit | Model, prompt, tools, code, API, dataset, editor settings | One guidance value and its resulting content revision | The edited content changes the recommendation and behavior |

**Deliverables**

- Write down the beginner prompt, a prompt that challenges the difficulty recommendation, and a spare prompt.
- Give each editor window only the tools for its assigned server. Use fresh chats and consistent repository instructions so prior context does not supply the answer.
- Add a reset procedure covering guidance, generated docs, processes, and chat context. Reset only workshop-owned state and preserve attendee edits unless they explicitly choose to restore the fixture.
- Record tool selection, applied guidance, returned data, and the final recommendation.
- Rehearse five fresh runs per primary scenario with a recorded model and settings. All five guide runs should expose the correct recommendation and source; report observed outcomes.

**Completion check:** The guide consistently demonstrates the documented policy and its edit. The wrapper is allowed to succeed. A wrapper success becomes a discussion of what the model inferred; it does not justify weakening the wrapper or claiming a guaranteed failure.

The first comparison changes both interface and guidance. Use the second comparison when attributing a behavior change specifically to the content edit.

## Milestone 4 Package the attendee installation and exercise

**Deliverables**

- Provide a root workspace configuration and a startup path that handles the backing API, readiness checks, and MCP startup without requiring attendees to manage two terminals.
- Extend the same workflow to Codespaces with configuration discoverable from the repository root.
- Add a root quickstart covering fork, open, start, and verify. Include both demo prompts and the expected tool names.
- Add `EXERCISE.md` with the exact rule location, before and after values, restart instructions, unchanged prompt, expected result, and recovery steps.
- Explain which parts of an MCP description are cached by the host in the tested setup and document the refresh procedure observed during rehearsal.
- Keep Python/data/API construction instructions available as an optional appendix.

**Completion check:** A reviewer using a fresh fork and clean environment reaches a working guide within the eight-minute installation block, then completes the edit and explanation within the six-minute exercise block. Test both local VS Code and Codespaces. Verify a second MCP-compatible host as a portability check and document any host-specific setup.

## Milestone 5 Make adaptation achievable

**Deliverables**

- Extend the adaptation exercise with a small runnable example from another product: a deployment guide that recommends a preview environment before a first production deployment. Supply its content and task handler using the same guidance loader and provenance pattern; it gives advice without performing deployments.
- Show the mapping from a real support question to a default, rationale, anti-pattern, worked example, and source reference.
- Identify which files change for content-only customization and which change when adding a new product task or data source.
- Keep transport, process startup, provenance, and the guidance-loading pattern reusable.
- Add a concise acceptance template: prompt, documented recommendation, rule edit, expected tool result, expected editor response, and evidence to capture.
- Include a changed scenario where the attendee must explain whether their rule still applies and which missing information could change the recommendation.

**Completion check:** A reviewer who did not implement the guide can substitute a rule from their own product into the worked example, restart, and observe the expected recommendation and source in the editor. They can identify the task handler that applies the rule and the changes needed for a new task. If they need to change several transport or startup files, simplify that boundary before calling the scaffold adaptable.

## Milestone 6 Align the session and rehearse

Update the README, outline, and tutorial around the completed attendee path. Reconcile existing issues with actual delivered scope and remove promises about tool counts that no longer serve the demo. Keep the original prospectus and this acceptance criterion visible in the planning materials.

Use this proposed 45-minute sequence:

| Block | Minutes |
|---|---:|
| Developer education problem and session promise | 5 |
| Wrapper and guide comparison | 7 |
| Trace a recommendation from docs through MCP to the editor | 6 |
| Fork, install, and verify | 8 |
| Edit guidance, restart, and observe | 6 |
| Adapt the pattern to a product | 5 |
| Questions, recovery time, and leave-behinds | 8 |
| Total | 45 |

Record screenshot or transcript fallbacks from actual rehearsals. Label recorded results clearly when using them. Build slides from the verified workflow, then run the complete session with a reviewer who has not seen the implementation.

**Completion check:** The attendee can demonstrate the criterion without presenter intervention beyond the written instructions. Update confusing steps and repeat the failed portion before the full rehearsal.

## Verification and release evidence

Retain the existing tests, lint, setup validation, and protocol smoke test. Add focused verification for the new guarantees:

- Guidance validation reports malformed rules and missing required fields.
- Changing only the guidance default from two to three changes a real MCP result after restart, including the applied value and revision.
- Practice results omit answers until explicitly revealed.
- Valid user choices, insufficient data, and difficulty limitations behave as documented.
- Human documentation and MCP descriptions derive from the same rule values and rationale.
- Fresh installation and editor observation pass the timed attendee checks.
- An attendee explains the recommendation and its exception in a changed scenario, so the exercise checks understanding as well as server behavior.

Keep a small evidence record with the tested commit, content revision, editor and model, prompts, tool traces, and observed results. Automated tests establish server behavior; editor rehearsals establish that the agent uses and explains the supplied guidance. Both are required.

The workshop is ready when a reviewer can complete all three actions:

1. **Trace:** Point from a recommendation to its exact source rule and explain why it applies.
2. **Observe:** Edit that rule and show the expected change using the same prompt in the editor.
3. **Adapt:** Run a rule from their own product through the scaffold and identify how it reaches the agent.

## Priority order

Implement milestones in dependency order: guidance contract → working guide and content edit → reproducible comparisons → attendee packaging → adaptation → full session rehearsal.

Optional production recordings, a separate landing page, a long-form post, additional domains, and a larger tool catalog come after the acceptance checks pass. The next concrete implementation task is **Milestone 1 followed immediately by the two-to-three proof in Milestone 2**.
