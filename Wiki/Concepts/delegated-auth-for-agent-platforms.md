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
  - "Raw/Sources/Delegated auth.md"
  - "Raw/Sources/Power an agent platform.md"
source_count: 2
aliases:
  - "on-behalf-of auth"
  - "multi-tenant Swiggy auth"
---

# Delegated Auth For Agent Platforms

## Summary

Delegated auth is the OAuth 2.1 on-behalf-of flow for platform operators who broker Swiggy for many end users. The source frames the principle as "your user, Swiggy's account, your UI": Swiggy holds the PII while the platform holds a scoped per-user session. Each end user runs the authorization flow, and the platform stores and uses that user's access token to call Swiggy MCP on their behalf.

## Key Points

- The platform registers dynamically via RFC 7591 at `POST /auth/register`; onboarding aligns on an allowlist of exact-match HTTPS redirect URIs (or platform schemes) and which servers it will call.
- A fresh PKCE verifier and challenge is generated per user session before sending the user to `/auth/authorize`.
- Access tokens are stored per user in secure storage, never shared across users and never persisted in plaintext beyond their lifetime.
- Token lifecycle mirrors the direct flow: 5-day access token, 30-day sliding session, 120-second single-use authorization code; no refresh tokens in v1.0.
- Logout is a `POST /auth/logout` with the user's bearer token, which revokes the session server-side.
- Commitments include PII staying with Swiggy, per-user audit logs on lawful request, and instrumented token issuance.
- Platform onboarding is white-glove: apply, intro call, architecture review, partner contract, staging access, then production cutover, with negotiated rate limits and a 99.9% uptime SLA target.

## Related Notes

- [[Swiggy MCP]]
- [[OAuth 2.1 With PKCE For MCP]]

## Source Notes

- Source: `Raw/Sources/Delegated auth.md`
- Source: `Raw/Sources/Power an agent platform.md`
