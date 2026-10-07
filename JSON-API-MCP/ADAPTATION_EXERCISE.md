# Exercise: swap in your own JSON dataset

The goal is to change the domain without rewriting the MCP transport plumbing. Use a small, synthetic fixture from your own domain so the feedback loop stays fast.

## 1. Define one record

Write down the smallest useful record your users need. Identify:

- its stable identifier;
- required and nullable fields;
- any constrained values that should become an enum;
- the fields users will search or filter.

Replace `Clue` and `Round` in `src/jeopardy_template/models.py`. Keep strict numeric validation so JSON booleans cannot silently become integers.

## 2. Adapt and index it

Update `adapter.py` to turn one source object into the new model, then update `repository.py` with the lookup and filters your tools need. Avoid building a universal converter: make invalid source data fail with the record index and a useful diagnostic.

## 3. Redesign the public contracts

Change the routes and response models in `api.py`, then make the matching changes in `api_client.py`. The client is the boundary that prevents malformed or unexpected HTTP responses from reaching an MCP tool as trusted data.

## 4. Shape tools around user tasks

Replace the three functions in `mcp_server.py`. Tool names and descriptions should describe what a user is trying to accomplish, not merely repeat internal function or endpoint names.

For Part 1, keep them as thin mappings so you have a baseline. In Part 2, add a preferred default, an anti-pattern, and a worked example to one tool description and compare agent behavior.

## 5. Prove the path

Add a synthetic fixture containing both ordinary and edge-case values. Update the REST and MCP assertions, then run:

```bash
uv run --locked ruff check .
uv run --locked pytest
```

With FastAPI running, finish with:

```bash
uv run --locked python scripts/smoke_test.py
```

You are done when the same known record travels from your JSON fixture through FastAPI and a real MCP stdio subprocess without changing meaning.
