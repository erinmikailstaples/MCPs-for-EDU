# GitHub Universe 2026

## Goodbye, Tutorial Hell: AI Guides and the New Documentation Layer

This repository contains the talk, demos, and hands-on workshop materials for a proposed 45-minute GitHub Universe sandbox session. The session shows developers how to move beyond thin MCP API wrappers and build AI Guides that give GitHub Copilot useful product judgment: opinionated defaults, decision guidance, anti-patterns, guardrails, and worked examples.

The workshop begins by building a deliberately thin but correct JSON → FastAPI → MCP reference implementation. A later section evolves that baseline into a task-focused AI Guide, making the difference between **access** and **judgment** visible in the same editor, with the same model and the same underlying data.

## Workshop materials

- [Full workshop tutorial](TUTORIAL.md) — the teaching sequence from validated JSON through a thin MCP wrapper and into an opinionated AI Guide.
- [Part 1: JSON → FastAPI → MCP](JSON-API-MCP/README.md) — a runnable, repeatable reference implementation using a Jeopardy-shaped dataset.
- [Server instructions](JSON-API-MCP/INSTRUCTIONS.md) — setup, startup, verification, troubleshooting, and reasons to put an API in front of JSON.
- [Talk outline](OUTLINE.md) — the complete 45-minute session flow, demos, exercises, and build plan.

## Audience

The session is designed for intermediate engineers, developers, maintainers, founders, and product teams who want to make their APIs and documentation more useful to AI coding agents without maintaining a separate body of agent-only documentation.

## Core thesis

An MCP server that only wraps an API gives Copilot access. An AI Guide gives Copilot judgment. Access answers what an agent *can* do; judgment helps it decide what it *should* do.
