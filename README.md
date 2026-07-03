# Codebase Guardrail

**Give your AI coding agent a memory that does not just remember - it enforces.**

Built for the Cognee "Hangover" hackathon. Powered by [Cognee](https://github.com/topoteretes/cognee).

## The Problem

Coding agents like Claude Code are stateless - they forget everything between sessions, so they cheerfully re-introduce approaches your team already tried and rejected. You proved last month that storing auth tokens in localStorage was an XSS hole and switched to HttpOnly cookies. A fresh session does not know that, and writes the localStorage code again. A bigger context window does not fix this: a real codebase plus months of decisions is millions of tokens. This is where persistent, structured memory has to take over.

## The Solution

Codebase Guardrail stores your team's rejected approaches as structured memory in Cognee's hybrid graph-vector store, then acts as an active guardrail on your coding agent. Before the agent acts on a prompt, it checks memory - and if your request conflicts with a decision you already made, it stops and cites why. The stock Cognee plugin remembers and injects context; Codebase Guardrail remembers the reasoning and enforces it.

## How It Works

Three pieces, wired into Claude Code:

1. **/decide** (capture) - record a rejected approach in plain English. Calls `cognee.remember()` to structure it into the knowledge graph.
2. **The guardrail** (enforce) - a Claude Code UserPromptSubmit hook runs on every prompt, calls `cognee.recall()`, and warns you when a request conflicts with a past decision.
3. **/why** (query) - ask the decision graph anything, e.g. "how should we store timestamps?"

## Cognee Memory Lifecycle Used

- `remember()` - every /decide ingests a rejected decision and builds it into the graph.
- `recall()` - the guardrail and /why query memory, auto-routing between semantic similarity and graph traversal.
- `improve()` - self-improvement enriches the decision graph after ingestion.
- `visualize_graph()` - renders the decision graph to interactive HTML.

## Setup

1. `pip install cognee`
2. Create a `.env` with your LLM + embedding config (LLM_PROVIDER, LLM_MODEL, LLM_API_KEY, EMBEDDING_PROVIDER, EMBEDDING_MODEL, EMBEDDING_DIMENSIONS).
3. Open Claude Code in the project folder: `claude`

The guardrail hook lives in `.claude/settings.json`; the /decide and /why commands in `.claude/commands/`; the memory scripts in `memory/`.

## Why It Matters

Institutional knowledge evaporates, and coding agents make it worse by re-deriving decisions from scratch every session. Codebase Guardrail turns your team's hard-won "we already tried that" into memory the agent cannot ignore.
