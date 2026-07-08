---
Title: "Coding agents"
Author: "Swiggy Builders Club"
Reference: "https://mcp.swiggy.com/builders/docs/start/coding-agents/"
ContentType:
  - "markdown"
Created: 2026-07-08
Processed: true
tags:
  - "source"
---
Every page on this site ships in three forms the moment it's published: HTML for you, Markdown for your agent, and a compact index for quick lookup. Point your coding tool at one URL and it has the whole catalog - tool schemas, auth flow, error codes, rate limits - without scraping or guessing.

## Paste this into your coding agent

The fastest way to set up any coding agent - Claude Code, Cursor, Windsurf, Codex, Aider, Cline, or anything that reads project rules. Paste this prompt into your agent (or drop it in `CLAUDE.md` / `.cursor/rules/` / `AGENTS.md`):

```
You have access to Swiggy Builders Club docs - the authoritative source
for Swiggy MCP (Food, Instamart, Dineout). Always consult these before
writing Swiggy code:
 
- Index:      https://mcp.swiggy.com/builders/llms.txt
- Full text:  https://mcp.swiggy.com/builders/llms-full.txt
- Per-page:   append \`.md\` to any https://mcp.swiggy.com/builders/docs/... URL
 
Tool schemas live under \`/docs/reference/{food,instamart,dineout}\`.
Error codes live at \`/docs/reference/errors\`. Auth flow is at
\`/docs/start/authenticate\`.
 
Rules:
1. Before recommending a tool name, parameter, error code, rate limit,
   or auth flow, fetch the relevant doc and verify.
2. Never invent tool names or parameters. If the docs don't cover it,
   say so and ask.
3. Prefer \`.md\` page fetches over \`llms-full.txt\` when you know the
   exact area - it's cheaper on context.
 
Smoke test: fetch llms.txt and tell me how many tools the Food server
exposes. (Answer: 14.)
```

That's it. Your agent now reads real docs instead of guessing. Scroll for tool-specific install paths (`CLAUDE.md`, `.cursor/rules/`, `.windsurf/rules/`, `AGENTS.md`), or keep going for the reference section below.

## The docs, as Markdown

Append `.md` to any docs or blog URL:

| URL | Serves |
| --- | --- |
| `https://mcp.swiggy.com/builders/docs/start/authenticate.md` | This page as plain Markdown |
| `https://mcp.swiggy.com/builders/docs/reference/food/search_restaurants.md` | One tool, full schema |
| `https://mcp.swiggy.com/builders/llms.txt` | Compact index: every page, URL, and one-line description |
| `https://mcp.swiggy.com/builders/llms-full.txt` | Every page's full body concatenated - one file, ~all docs |

`llms.txt` follows the [llmstxt.org](https://llmstxt.org/) convention. `llms-full.txt` is the "drop the whole docs into a prompt" file - use it when your agent needs breadth without tool calls.

## Wire it into your coding tool

Add this to `CLAUDE.md` at the root of your project (or your global `~/.claude/CLAUDE.md`):

```
## Swiggy Builders Club
 
When writing code against Swiggy MCP (Food, Instamart, Dineout),
consult the authoritative docs at:
 
- Index:     https://mcp.swiggy.com/builders/llms.txt
- Full text: https://mcp.swiggy.com/builders/llms-full.txt
- Per-page:  append \`.md\` to any https://mcp.swiggy.com/builders/docs/... URL
 
Before recommending a tool name, parameter, error code, rate limit, or
auth flow, verify against these docs. The tool catalog lives under
\`/docs/reference/{food,instamart,dineout}\`.
```

Claude Code's `WebFetch` tool will pull these on demand. For interactive testing against the live MCP servers, also see [Connect your AI client](https://mcp.swiggy.com/builders/docs/start/consumer/use-in-ai-client/) - the Claude Desktop config works in Claude Code too.

## What a good agent rule looks like

A useful rule points your agent at the docs **and** tells it when to look. Three things worth including:

1. **Where** - the three URLs above.
2. **When** - before suggesting a tool name, parameter, error code, rate limit, or auth flow.
3. **Why not to guess** - Swiggy tool schemas evolve. Hallucinated parameters fail silently in dev and load-bearing in prod.

## Test your agent can read the docs

Ask your coding agent:

A correctly-wired agent answers "14" after reading `/docs/reference/food/`. A mis-wired one guesses.

## Connect Swiggy MCP for live tool calls

Rules above give your agent **docs**. If you want your agent to actually **call Swiggy tools** (place test orders, fetch real menus) while you develop, install the Swiggy MCP servers in your IDE - the full config for Cursor, Claude Desktop, VS Code Copilot, Windsurf, and any MCP client is on [Connect your AI client](https://mcp.swiggy.com/builders/docs/start/consumer/use-in-ai-client/).

## Where to go next

- New to Swiggy MCP: [What is Swiggy MCP?](https://mcp.swiggy.com/builders/docs/start/what-is-swiggy-mcp/).
- Building your first agent: [Developer quickstart](https://mcp.swiggy.com/builders/docs/start/developer/).
- Ready for prod: [Ship to production](https://mcp.swiggy.com/builders/docs/build/ship-to-production/).
- Tool catalog: [Reference](https://mcp.swiggy.com/builders/docs/reference/).