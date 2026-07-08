---
tags:
  - "concept"
topics:
  - "swiggy mcp"
  - "agent frameworks"
status: seed
created: 2026-07-08
updated: 2026-07-08
sources:
  - "Raw/Sources/Developer quickstart.md"
  - "Raw/Sources/Build an agent.md"
  - "Raw/Sources/Coding agents.md"
source_count: 3
aliases:
  - "Swiggy developer quickstart"
  - "wiring Swiggy MCP"
---

# Building Swiggy MCP Agents

## Summary

The developer path wires Swiggy MCP into an existing agent framework and makes a first tool call against a staging endpoint. The sources cover the self-serve quickstart, per-framework connector code, and how to point coding agents at Swiggy's authoritative docs so they verify tool schemas instead of guessing.

## Key Points

- The self-serve flow is: understand the tool-call loop, optionally apply for production access, pick a framework, complete OAuth, and make a first tool call such as `get_addresses`.
- Any MCP-compatible framework works; the sources list OpenAI Agents SDK, Anthropic SDK, LangGraph/LangChain, Vercel AI SDK 6, Mastra, PydanticAI, CrewAI, Google ADK, and raw MCP clients.
- SDK OAuth support splits into native `authProvider` support (SDK runs PKCE automatically) and bearer-header-only SDKs (obtain a token via the auth flow and forward `Authorization: Bearer <token>`).
- Since there are no refresh tokens in v1.0, agents treat the 5-day access token as the full session and re-run authorization on 401.
- Production access is invite-reviewed; applicants supply integration details, redirect URIs, target servers, expected volume, and a demo video link.
- Coding agents can consume Swiggy docs directly via per-page `.md`, the `llms.txt` index, and `llms-full.txt`, with a rule to verify tool names and parameters before recommending them.

## Related Notes

- [[Swiggy MCP]]
- [[Model Context Protocol]]
- [[Swiggy MCP Servers]]
- [[OAuth 2.1 With PKCE For MCP]]

## Source Notes

- Source: `Raw/Sources/Developer quickstart.md`
- Source: `Raw/Sources/Build an agent.md`
- Source: `Raw/Sources/Coding agents.md`
