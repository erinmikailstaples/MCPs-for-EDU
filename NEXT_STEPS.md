# Next steps checklist

Completed implementation and observed checks are marked below; see [verification evidence](evidence/README.md). Five-run comparisons, clean installs, and attendee rehearsal remain open. Work through this checklist in order. The [execution plan](EXECUTION_PLAN.md) contains the design rationale and lessons from pg-aiguide.

**Acceptance criterion:** An attendee can trace a recommendation to guidance they edited, observe its effect in their editor, and adapt that pattern to their own product.

## 1 Write the guidance

**Narrative**

- A tutorial can get someone to a first success. The next question is what to change when their own project has different requirements.
- The advice we give in support, onboarding, and code review contains the decisions developers need: what to try first, why, and when to choose something else.
- We will put that judgment into guidance humans can read and agents can use, with a reason and an example attached to each rule.

**Tasks**

- [x] Add `JSON-API-MCP/content/practice.json` with a default practice count of two and stable rule IDs.
- [x] Give each rule a rationale, applicability, exception or clarifying question, anti-pattern, and worked example.
- [x] Document board value as a rough difficulty proxy and describe when to ask about the learner's goal.
- [x] Validate the content and define precedence between constraints, explicit user choices, and defaults.
- [x] Generate human documentation from the same source and add a check for stale output.

**Done when:** A reader can find a recommendation, explain why it applies, and identify its source rule.

## 2 Build the smallest working guide

**Narrative**

- The wrapper gives the agent access to clues. The guide adds a recommended way to use them for practice.
- A short practice round, hidden answers, and an explanation of difficulty turn available data into a learning activity.
- Every recommendation should lead back to its source. The attendee should be able to inspect the advice and understand which parts the server enforces.

**Tasks**

- [x] Add a separate guide server using the existing API and dataset; preserve `jeopardy-basics` as the wrapper.
- [x] Provide guidance retrieval, practice-set creation, and explicit answer reveal.
- [x] Build descriptions and executable defaults from the loaded guidance.
- [x] Include the applied rule, source location, rationale, value, and content revision in tool results.
- [x] Verify hidden answers, valid user overrides, and truthful handling of too few matching clues.

**Done when:** A real MCP call returns a practice set and identifies the guidance that shaped it.

## 3 Prove the edit in the editor

**Narrative**

- This is the moment the attendee becomes the author of the guidance: they change a rule and see its effect in their own editor.
- Two clues becoming three makes the connection visible. The source reference lets them explain exactly where the recommendation came from.
- The next question is why that default is useful and when to override it. That discussion connects a working edit to product judgment.

**Tasks**

Use the same prompt in fresh chats:

> Give me a beginner practice round in Developer Tools.

- [x] Run with the default of two; capture the tool result and the agent's explanation and source reference.
- [x] Change only the guidance default to three, save, restart the guide, and refresh host descriptions if needed.
- [x] Rerun the prompt; verify three clues, the correct explanation, and updated source revision.
- [x] Add a protocol test proving the content-only edit changes the result after restart.
- [x] Run lint, existing tests, setup validation, and the REST-to-MCP smoke test alongside the new checks.

**Done when:** The attendee can point from the changed recommendation to the exact rule they edited.

## 4 Rehearse the comparisons

**Narrative**

- Side by side, the wrapper and guide let us inspect what the agent inferred and what the server supplied.
- Repeating the same guide before and after one content edit lets us trace the change more precisely. Keep the prompt, model, code, and data consistent.
- The wrapper may give a good answer. Report what happens and use the tool traces to explain the role of guidance in each result.

**Tasks**

- [x] Write the beginner, difficulty-tradeoff, and spare prompts with expected observations.
- [ ] Record the model and editor settings; isolate each server's tools and use fresh chats.
- [ ] Compare wrapper versus guide using the same prompt, API, and data. Record actual outcomes, including wrapper successes.
- [ ] Repeat the guide before and after the edit across five fresh runs per primary scenario; capture correctness and source attribution.
- [x] Document a reset procedure that preserves attendee edits unless they choose to restore the fixture.

**Done when:** The guide reliably applies and explains its rules. Attribute the content edit's effect using the same-guide comparison.

## 5 Make installation and the exercise easy

**Narrative**

- The session promise becomes concrete when attendees can fork the scaffold, start it, and use it themselves.
- Clear setup and recovery steps give them time to inspect and change the guidance during the workshop.
- Each checkpoint should answer a practical question: is it running, which rule is active, and how can I verify my edit?

**Tasks**

- [x] Add root workspace configuration and startup that manages the API, readiness, and MCP process.
- [ ] Make the same path work from a fresh fork in local VS Code and Codespaces.
- [x] Write the quickstart and `EXERCISE.md` with the rule location, edit, restart, refresh, verification, and recovery steps.
- [ ] Test installation within eight minutes and the edit exercise within six minutes with a reviewer using a clean environment.
- [ ] Verify a second MCP-compatible host and document setup differences.

**Done when:** A reviewer completes installation and the edit using the written instructions.

## 6 Prove the pattern transfers

**Narrative**

- Jeopardy makes the first example easy to inspect. The deployment example shows how the same structure can carry advice for a different product.
- Start with a question your users ask repeatedly. Write the recommended path, its reason, and the condition that would change your advice.
- Ask the attendee to apply their rule to a changed scenario. Their explanation shows whether they can carry the reasoning into their own work.

**Tasks**

- [x] Provide a standalone template with editable product context, reference docs, editor configuration, a safe copy helper, and an independent copied-project verification.
- [x] Add the runnable deployment-advice example using the same guidance-loading and source-tracing pattern.
- [x] Explain which files change for a content edit, a new task, and a new data source.
- [ ] Have a reviewer substitute a rule from their own product, restart, and observe its recommendation and source in the editor.
- [ ] Give them a changed scenario; ask why the rule applies, when it does not, and what missing information would change the answer.

**Done when:** The reviewer demonstrates both adaptation and understanding of the tradeoff.

## 7 Finish the session materials

**Narrative**

- The session follows one continuous story: encounter a decision, find the guidance, inspect its effect, edit it, and apply the pattern elsewhere.
- The pg-aiguide lessons give that story a real implementation reference; our scaffold lets attendees practice the content-to-behavior loop themselves.
- Leave attendees with a working scaffold and a repeatable habit: review guidance, observe behavior, explain the tradeoff, and revise as the product changes.

**Tasks**

- [ ] Align the README, tutorial, outline, and existing issues with the verified attendee workflow.
- [x] Move infrastructure construction into optional background and remove unsupported tool-count and demo-outcome promises.
- [ ] Build slides and clearly labeled screenshot or transcript fallbacks from actual runs.
- [ ] Run the full 45-minute session with someone unfamiliar with the implementation and fix the steps where they get stuck.

**Final check:** The reviewer can trace, observe, and adapt without presenter intervention beyond the written instructions.

Keep the optional production recording, landing page, long-form post, additional domains, and larger tool catalog behind these acceptance checks.
