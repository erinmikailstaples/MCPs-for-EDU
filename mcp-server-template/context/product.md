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
