---
tags:
  - "concept"
topics:
  - "swiggy mcp"
  - "ai clients"
status: seed
created: 2026-07-08
updated: 2026-07-08
sources:
  - "Raw/Sources/Use Swiggy in your AI client.md"
  - "Raw/Sources/Connect your AI client.md"
source_count: 2
aliases:
  - "no-code Swiggy install"
  - "Swiggy in Claude Desktop"
---

# Using Swiggy In AI Clients

## Summary

Users of an existing AI client (Claude Desktop, ChatGPT, Cursor, VS Code, Windsurf) can add Swiggy as a tool with no code: paste a config, restart the app, and complete OAuth. The sources describe the install as taking under two minutes, after which the client picks the right tool and the user's own Swiggy account places the order.

## Key Points

- The Claude Desktop config adds Swiggy servers under `mcpServers` using `npx mcp-remote` pointed at the server URLs; only the needed server entries have to be kept.
- On first launch a browser window opens to complete OAuth with phone and OTP, and the client confirms the connection.
- Every tool call is scoped to the user's authenticated Swiggy session; addresses, carts, and orders remain tied to the existing account and can be verified, modified, or cancelled in the Swiggy app.
- The AI client provider receives chat messages and tool results per its own privacy policy.
- Common issues include OAuth loops (kill and retry), tools not showing (reload the MCP server list), and 401 after a few days (session expired, re-connect).

## Related Notes

- [[Swiggy MCP]]
- [[Swiggy MCP Servers]]
- [[OAuth 2.1 With PKCE For MCP]]

## Source Notes

- Source: `Raw/Sources/Use Swiggy in your AI client.md`
- Source: `Raw/Sources/Connect your AI client.md`
