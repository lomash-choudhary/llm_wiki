---
Title: "Build an agent"
Author: "Swiggy Builders Club"
Reference: "https://mcp.swiggy.com/builders/docs/start/developer/build-an-agent/"
ContentType:
  - "markdown"
Created: 2026-07-08
Processed: true
tags:
  - "source"
---
Swiggy MCP speaks standard streamable HTTP. Every major agent framework in 2026 has first-class MCP support. Pick your framework, paste the connector, give your agent access to 35 Swiggy tools.

Swiggy MCP is OAuth 2.1 + PKCE - there is no static API key. SDK support for the flow splits into two camps:

- **Native `authProvider` support** (raw MCP TS / Python SDKs, OpenAI Agents JS, Vercel AI SDK 6, Mastra) - pass an OAuth client provider and the SDK runs PKCE against Swiggy's `/.well-known/oauth-protected-resource` and `/.well-known/oauth-authorization-server` automatically.
- **Bearer-header only** (OpenAI Agents Python, LangChain MCP adapters, PydanticAI, CrewAI, Google ADK, Anthropic hosted MCP connector) - the SDK has no OAuth hook, so you obtain an access token via the [Authenticate](https://mcp.swiggy.com/builders/docs/start/authenticate/) flow and forward it as `Authorization: Bearer <token>`.

The snippets below assume:

- `swiggyOAuthProvider` / `swiggy_oauth_provider` - your implementation of the MCP SDK's `OAuthClientProvider` interface, wrapping the [Authenticate](https://mcp.swiggy.com/builders/docs/start/authenticate/) flow. The Mastra tab shows a ready-made one via `MCPOAuthClientProvider`.
- `getSwiggyAccessToken()` - your helper that runs the [Authenticate](https://mcp.swiggy.com/builders/docs/start/authenticate/) flow and returns a fresh Bearer token. Re-run on 401.

Refresh tokens are not yet wired in v1.0; treat the 5-day access token as the full session and re-run authorization on 401.

```
import { Agent, Runner, MCPServerStreamableHttp } from "@openai/agents";
import { swiggyOAuthProvider } from "./swiggy-oauth"; // implements OAuthClientProvider
 
const swiggyFood = new MCPServerStreamableHttp({
  url: "https://mcp.swiggy.com/food",
  authProvider: swiggyOAuthProvider,
});
 
const agent = new Agent({
  name: "FoodOrderingAgent",
  instructions: "Help users order food on Swiggy. Always call get_addresses first.",
  mcpServers: [swiggyFood],
});
 
await swiggyFood.connect();
const result = await Runner.run(agent, "Order biryani to my home address.");
console.log(result.finalOutput);
```

Python (the `agents` SDK doesn't expose an OAuth hook today - pass a Bearer token in headers):

```
import os
from agents import Agent, Runner
from agents.mcp import MCPServerStreamableHttp
 
token = await get_swiggy_access_token()  # your OAuth helper
 
swiggy_food = MCPServerStreamableHttp(
    params={
        "url": "https://mcp.swiggy.com/food",
        "headers": {"Authorization": f"Bearer {token}"},
    },
)
 
agent = Agent(
    name="FoodOrderingAgent",
    instructions="Help users order food on Swiggy. Always call get_addresses first.",
    mcp_servers=[swiggy_food],
)
 
await swiggy_food.connect()
result = await Runner.run(agent, "Order biryani to my home address.")
print(result.final_output)
```

## Handling expired tokens

Access tokens live 5 days. When a call returns 401 (or JSON-RPC `-32001`), re-run the OAuth flow and retry. Most frameworks expose a hook for this; for raw clients:

```
async function callWithReauth<T>(fn: () => Promise<T>): Promise<T> {
  try {
    return await fn();
  } catch (e: any) {
    if (e?.status === 401) {
      await reAuthenticate();
      return fn();
    }
    throw e;
  }
}
```

See [Authenticate](https://mcp.swiggy.com/builders/docs/start/authenticate/) for the full OAuth walkthrough.

## Wire more than one Swiggy server

Each server is independent - connect multiple if your agent needs to span domains:

```
mcpServers: [
  { url: "https://mcp.swiggy.com/food" },
  { url: "https://mcp.swiggy.com/im" },
  { url: "https://mcp.swiggy.com/dineout" },
]
```

Tool names are unique across servers, so your agent can dispatch across all 35 tools without conflict.

## Where to go next

- [Recipes](https://mcp.swiggy.com/builders/docs/build/) - end-to-end journeys for food, grocery, dineout, and combined flows.
- [Agent patterns](https://mcp.swiggy.com/builders/docs/build/agent-patterns/voice-vs-chat/) - voice vs chat response shaping, multi-turn state.
- [Reference](https://mcp.swiggy.com/builders/docs/reference/) - every tool, every parameter.
- [Ship to production](https://mcp.swiggy.com/builders/docs/build/ship-to-production/) - retries, observability, go-live checklist.