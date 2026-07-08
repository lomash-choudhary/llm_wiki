---
tags:
  - "concept"
topics:
  - "swiggy mcp"
  - "authentication"
status: seed
created: 2026-07-08
updated: 2026-07-08
sources:
  - "Raw/Sources/Authenticate.md"
source_count: 1
aliases:
  - "OAuth 2.1 PKCE"
  - "Swiggy MCP auth"
---

# OAuth 2.1 With PKCE For MCP

## Summary

Swiggy MCP authenticates every external caller with OAuth 2.1 using PKCE, the same flow that clients like Claude Desktop and Cursor run automatically. The source describes the direct developer flow: generate a PKCE verifier and challenge, send the user through `/auth/authorize`, exchange the authorization code at `/auth/token` for a signed JWT access token, and call the MCP server with a bearer token.

## Key Points

- Clients do not manage a client identity manually; Swiggy MCP supports Dynamic Client Registration (RFC 7591) at `POST /auth/register`, which MCP-compatible clients call transparently.
- Core endpoints include `GET /auth/authorize`, `POST /auth/token`, `POST /auth/logout`, and the two `.well-known` metadata documents.
- v1 scopes are server-level: `mcp:tools`, `mcp:resources`, and `mcp:prompts`; finer-grained read/write and per-domain scopes are on the roadmap but not enforced.
- Token lifecycle: access token lives 5 days, user session is 30 days idle and sliding, and the authorization code is single-use and valid for 120 seconds.
- Refresh-token issuance is not wired in v1.0; treat a 401 as "re-run authorization" and re-authenticate. Rolling refresh tokens are planned for v1.1.
- Redirect URIs must be HTTPS (except `http://localhost`), exact-match with no wildcards, and known MCP client custom schemes are allowed.

## Related Notes

- [[Swiggy MCP]]
- [[Delegated Auth For Agent Platforms]]
- [[Building Swiggy MCP Agents]]

## Source Notes

- Source: `Raw/Sources/Authenticate.md`
