---
tags:
  - "topic"
topics:
  - "swiggy mcp"
  - "agentic commerce"
status: seed
created: 2026-07-08
updated: 2026-07-08
sources:
  - "Raw/Sources/What is Swiggy MCP?.md"
  - "Raw/Sources/Use Swiggy in your AI client.md"
  - "Raw/Sources/Developer quickstart.md"
  - "Raw/Sources/Power an agent platform.md"
source_count: 4
aliases:
  - "Swiggy Builders Club"
  - "Swiggy MCP"
---

# Swiggy MCP

## Summary

Swiggy Builders Club exposes Swiggy's commerce platform as MCP servers, using the open Model Context Protocol that AI agents speak to external tools. The sources describe it as one protocol, three independent servers, 35 tools, and no vendor lock-in, aimed at letting agents discover and reason across Swiggy tools at runtime.

## Key Points

- Swiggy MCP is delivered as three independent servers: Food, Instamart, and Dineout.
- It targets three audiences: agent developers, agent platforms operating at scale, and AI-client users who want Swiggy as a tool in their existing client.
- MCP fits when an agent needs to discover and orchestrate multi-step flows (search to menu to cart to checkout); a fixed embedded widget without an agent should use Swiggy's regular APIs instead.
- Out of the box it provides OAuth 2.1 with PKCE, streamable HTTP transport, session auth, a stable error taxonomy, and a versioning contract with 6-month deprecation windows.
- The service is India-only, uses whitelist-based production onboarding, and is governed by a per-partner contract.

## Related Notes

- [[Swiggy MCP Servers]]
- [[Model Context Protocol]]
- [[Using Swiggy In AI Clients]]
- [[Building Swiggy MCP Agents]]
- [[OAuth 2.1 With PKCE For MCP]]
- [[Delegated Auth For Agent Platforms]]

## Source Notes

- Source: `Raw/Sources/What is Swiggy MCP?.md`
- Source: `Raw/Sources/Use Swiggy in your AI client.md`
- Source: `Raw/Sources/Developer quickstart.md`
- Source: `Raw/Sources/Power an agent platform.md`
