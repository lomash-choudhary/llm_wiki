---
tags:
  - "entity"
topics:
  - "swiggy mcp"
status: seed
created: 2026-07-08
updated: 2026-07-08
sources:
  - "Raw/Sources/What is Swiggy MCP?.md"
  - "Raw/Sources/Build an agent.md"
  - "Raw/Sources/Connect your AI client.md"
source_count: 3
aliases:
  - "Food server"
  - "Instamart server"
  - "Dineout server"
---

# Swiggy MCP Servers

## Summary

Swiggy MCP is split into three independent MCP servers, each with its own endpoint and tool set. The sources state they do not share carts, orders, or sessions, and that tool names are unique across servers so an agent can wire one, two, or all three without conflict.

## The Three Servers

- Food: endpoint `mcp.swiggy.com/food`, restaurant discovery, menus, ordering, and tracking, 14 tools.
- Instamart: endpoint `mcp.swiggy.com/im`, quick-commerce grocery, 13 tools.
- Dineout: endpoint `mcp.swiggy.com/dineout`, table reservations, 8 tools.

## Key Points

- Each server is independent and addressed by its own URL.
- The three servers total 35 tools.
- Tool names are unique across servers, so an agent can dispatch across all of them.
- A client can connect only the servers it needs (for example, keep just the Food entry in a config).

## Related Notes

- [[Swiggy MCP]]
- [[Model Context Protocol]]
- [[Using Swiggy In AI Clients]]

## Source Notes

- Source: `Raw/Sources/What is Swiggy MCP?.md`
- Source: `Raw/Sources/Build an agent.md`
- Source: `Raw/Sources/Connect your AI client.md`
