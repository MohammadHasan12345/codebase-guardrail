# Codebase Guardrail

**Give your AI coding agent a memory that doesn't just remember — it enforces.**

Built for the Cognee "Hangover" hackathon. Powered by [Cognee](https://github.com/topoteretes/cognee).

---

## The Problem

Every time you call an LLM, it's stateless. Coding agents like Claude Code forget everything between sessions — so they cheerfully **re-introduce approaches your team already tried and rejected**. You spent a week last month proving that storing auth tokens in `localStorage` was an XSS disaster and switched to HttpOnly cookies. A fresh session doesn't know that. It writes the `localStorage` code again.

A bigger context window doesn't fix this: a real codebase plus months of decisions is millions of tokens — it physically won't fit. This is exactly where persistent, structured memory has to take over.

## The Solution

Codebase Guardrail stores your team's **rejected approaches** as structured memory in Cognee's hybrid graph-vector store, then acts as an **active guardrail** on your coding agent. Before the agent acts on a prompt, it silently checks memory — and if your request conflicts with a decision you already made, it **stops and cites why**, instead of walking you back into the mistake.

The stock Cognee plugin *remembers and injects context*. Codebase Guardrail adds the layer it doesn't have: it *remembers the reasoning and enforces it*.

## How It Works

Three pieces, wired into Claude Code:

1. **`/decide` — capture (visible).** You record a rejected approach in plain English:
   `/decide We rejected storing timestamps as local strings; use UTC ISO-8601 because local strings broke cross-timezone sorting.`
   This calls `cognee.remember()`, which structures the decision into the knowledge graph.

2. **The guardrail — enforce (automatic).** A Claude Code `UserPromptSubmit` hook runs on every prompt. It calls `cognee.recall()` against your decision memory and, if the request conflicts with a past rejected approach, injects a warning so the agent stops and explains the tradeoff before proceeding.

3. **`/why` — query (on demand).** Ask the decision graph anything:
   `/why how should we store timestamps?` → *"UTC ISO-8601, because local strings broke sorting across timezones."*

## Cognee Memory Lifecycle Used

- **`remember()`** — every `/decide` ingests a rejected approach and builds it into the graph.
- **`recall()`** — the guardrail and `/why` query memory, with Cognee auto-routing between semantic similarity and graph traversal.
- **`improve()`** — self-improvement runs after ingestion to enrich the decision graph for sharper future recall.

## Demo

> A fresh session with no mention of the past decision. The user asks the agent to store an auth token in `localStorage`. The guardrail fires:
>
> *"There's a past project decision that conflicts with this request. Past decision: Don't store auth tokens in localStorage — it's vulnerable to XSS... use HttpOnly, SameSite cookies instead."*

[▶ Demo video](ADD_YOUR_VIDEO_LINK)

## Setup

```bash
# 1. Install Cognee
pip install cognee

# 2. Configure your LLM + embeddings in a .env file (Gemini shown)
#    LLM_PROVIDER, LLM_MODEL, LLM_API_KEY,
#    EMBEDDING_PROVIDER, EMBEDDING_MODEL, EMBEDDING_DIMENSIONS

# 3. Open Claude Code in the project folder
claude
```

The guardrail hook lives in `.claude/settings.json`; the `/decide` and `/why` commands live in `.claude/commands/`; the memory scripts live in `memory/`.

## Project Structure

```
codebase-guardrail/
├── .claude/
│   ├── settings.json          # UserPromptSubmit hook -> guard.py
│   └── commands/
│       ├── decide.md          # /decide -> capture.py
│       └── why.md             # /why -> query.py
├── memory/
│   ├── capture.py             # cognee.remember() a rejected approach
│   ├── guard.py               # cognee.recall() + inject guardrail warning
│   └── query.py               # cognee.recall() for /why
├── visualize.py               # render the decision graph to HTML
└── .env                       # LLM + embedding config
```

## Why It Matters

Institutional knowledge evaporates, and coding agents make it worse by re-deriving decisions from scratch every session. Codebase Guardrail turns your team's hard-won "we already tried that" into memory the agent can't ignore — a codebase that remembers its own scars.