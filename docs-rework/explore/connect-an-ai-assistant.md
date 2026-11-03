---
diataxis: how-to
tab: explore
---

# Connect an AI assistant to ODM

ODM's MCP server lets an AI assistant search and read ODM for you: you ask a question in plain language, and the assistant finds the studies, samples, libraries, preparations and omics data that answer it. It works with any assistant that supports remote servers of the [Model Context Protocol](https://modelcontextprotocol.io) (MCP).

The assistant acts as you: it sees what you can see in ODM, and it cannot change anything.

## Prerequisites

- Your ODM administrator has [enabled the MCP server](../admin/mcp-server.md), and given you its address, `https://<ODM_HOST>/mcp`.
- You sign in to ODM with Microsoft.

## Step 1: Add ODM to your assistant

Add a remote MCP server with the address `https://<ODM_HOST>/mcp`, of the type *Streamable HTTP* (often just *HTTP*). Leave any client ID, client secret or API key empty: the assistant registers itself.

For example, in Claude Code:

```bash
claude mcp add --transport http odm https://<ODM_HOST>/mcp
```

In VS Code, in `.vscode/mcp.json`:

```json
{
  "servers": {
    "odm": {
      "type": "http",
      "url": "https://<ODM_HOST>/mcp"
    }
  }
}
```

## Step 2: Sign in

The first time the assistant connects, it opens a browser window:

1. On the **Application Access Request** page, check the assistant's name and allow it.
2. Sign in with your Microsoft account, as you do for ODM.

The assistant then lists ODM's tools.

## Step 3: Ask a question

For example:

- *Which studies have samples from patients with Alzheimer's disease?*
- *List the data classes in the GTEx study.*
- *Show me the healthy brain samples from donors older than 16.*

## If you have to sign in again

The sign-in lasts while the assistant stays connected. When the MCP server restarts, after an ODM upgrade for example, the assistant asks you to sign in again.
