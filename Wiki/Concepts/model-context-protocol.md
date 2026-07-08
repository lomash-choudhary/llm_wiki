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
  - "Raw/Sources/What is Swiggy MCP?.md"
  - "Raw/Sources/Build an agent.md"
  - "Raw/Sources/Coding agents.md"
source_count: 3
aliases:
  - "MCP"
  - "Model Context Protocol"
---

# Model Context Protocol

## Summary

The Model Context Protocol (MCP) is the open standard that AI agents use to talk to external tools. In the Swiggy sources, MCP is what lets an LLM see tool schemas, decide which tool to call, and orchestrate multi-step flows at runtime, with Swiggy exposed as a tool provider over standard streamable HTTP.

## Key Points

- MCP is described as an open standard for connecting AI agents to external tools, with tool discovery and reasoning happening at runtime.
- Swiggy MCP uses streamable HTTP transport with one URL per server and standard JSON-RPC calls.
- A tool call loop is: the agent picks a tool from the server catalogue, the MCP client sends a JSON-RPC call, the server authenticates the session and runs the tool returning `{ success, data }`, and the agent decides what to call next.
- Every major agent framework in 2026 is described as having first-class MCP support.
- Swiggy publishes agent-readable docs (Markdown per page, an `llms.txt` index, and `llms-full.txt`) so coding agents can read authoritative schemas instead of guessing.

## Related Notes

- [[Swiggy MCP]]
- [[Swiggy MCP Servers]]
- [[Building Swiggy MCP Agents]]

## Source Notes

- Source: `Raw/Sources/What is Swiggy MCP?.md`
- Source: `Raw/Sources/Build an agent.md`
- Source: `Raw/Sources/Coding agents.md`
