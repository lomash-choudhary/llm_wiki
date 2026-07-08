---
Title: "Connect your AI client"
Author: "Swiggy Builders Club"
Reference: "https://mcp.swiggy.com/builders/docs/start/consumer/use-in-ai-client/"
ContentType:
  - "markdown"
Created: 2026-07-08
Processed: true
tags:
  - "source"
---
Pick your AI client. Paste the config. Restart. Complete OAuth. You're done.

Edit Claude Desktop's config file:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Add all three Swiggy servers:

```
{
  "mcpServers": {
    "swiggy-food": {
      "command": "npx",
      "args": ["mcp-remote", "https://mcp.swiggy.com/food"]
    },
    "swiggy-instamart": {
      "command": "npx",
      "args": ["mcp-remote", "https://mcp.swiggy.com/im"]
    },
    "swiggy-dineout": {
      "command": "npx",
      "args": ["mcp-remote", "https://mcp.swiggy.com/dineout"]
    }
  }
}
```

Restart Claude Desktop. On first launch a browser window opens - complete OAuth (phone + OTP). Claude confirms the connection in the bottom-left status bar.

Try: *"Search Instamart for bananas near my saved home address."*

Only need one server? Keep just that entry in `mcpServers`.

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| OAuth flow loops | Kill the client fully and retry; PKCE verifier is regenerated each attempt |
| Tools not showing up | After config changes, reload the MCP server list in your client |
| 401 after a few days | Session expired. Re-connect / complete OAuth again |
| "Tool not found" | Check you're pointed at the right server URL (`/food` vs `/im` vs `/dineout`) |
| Only want Food | Keep only the `swiggy-food` entry in your config |

## Privacy

- Your AI client provider (Anthropic, OpenAI, etc.) receives your chat + tool results per their privacy policy.
- Swiggy's stance on data handling: [data-and-compliance](https://mcp.swiggy.com/builders/docs/operate/data-and-compliance/).
- You remain in control - any action is visible (and reversible) in the Swiggy app.