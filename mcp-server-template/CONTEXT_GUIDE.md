# Your Product guidance

Generated from `context/guide.json` and its Markdown references. Run `uv run --locked python render_context.py` after editing context.

## Choose the next deployment step

Task ID: `deploy`

A developer asks where to deploy a change or proposes a first production release.

Default choice: **preview**

Avoid: Treating a successful build as proof that a change was verified outside production.

Example request: Recommend my next deployment step and explain why.

Example behavior: Use the configured default unless the developer makes a valid explicit choice. Ask about missing requirements before recommending a restricted choice.

### preview

Try the change in an isolated preview environment.

A preview lets you inspect the change before exposing it to users.

### staging

Try the change in your team's staging environment.

Staging provides a shared nonproduction place to check integration behavior.

### production

Consider production next, following your team's release requirements.

The developer explicitly selected production and confirmed nonproduction verification; this tool does not independently validate that claim.

Required confirmation: Has this change been verified in a nonproduction environment?

Reference: `context/product.md`

# Your Product context

Replace this file with the product or codebase context your developers need.

## Product purpose

This example product has a release workflow. Developers choose an environment and gather evidence before a change reaches users. The allowed choices and recommendation rules live in `guide.json`.

## Meaning of verification

Verification means the change has been exercised in a nonproduction environment. Agree on the specific checks with your team. A developer's confirmation is a supplied fact, not an independently inspected test result.

## Questions to answer for your own product

- What is the developer trying to accomplish?
- Which constraints or compatibility requirements matter?
- What should they do first, and why?
- Which missing fact changes the recommendation?
- How can they verify that the advice worked?

The server reads these documents as context. It provides advice and performs no deployment or other product operation.

