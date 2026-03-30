# CyberChef API MCP Server

This model context protocol (MCP) server interfaces with the [CyberChef Server](https://github.com/gchq/CyberChef-server) API. Allowing you to use any LLM/MCP client of your choosing to utilise the tools and resources within CyberChef.

🧰 Available Tools and Resources
---
- `get_cyberchef_operations_categories`: __resource__ - gets updated Cyber Chef categories for additional context / selection of the correct operations
- `get_cyberchef_operation_by_category`: __resource__ - gets list of Cyber Chef operations for a selected category
- `bake_recipe`: __tool__ - bake (execute) a recipe (a list of operations) in order to derive an outcome from the input data
- `batch_bake_recipe`: __tool__ - bake (execute) a recipe (a list of operations) in order to derive an outcome from a batch of input data
- `perform_magic_operation`: __tool__ - perform CyberChef's magic operation which is designed to automatically detect how your data is encoded and which operations can be used to decode it

📝 Usage
---
Start the server using the default stdio transport and specifying an environment variable pointing to a CyberChef API

```bash
CYBERCHEF_API_URL="your-cyberchef-api-url" uv run cyberchef_api_mcp_server
```

🧑‍💻Usage (Development)
---
Start the server and test it with the MCP inspector

```bash
uv add "mcp[cli]"
mcp dev server.py
```

📚 Client Configuration
---
The following commands will generate a client configuration file, the location will depend on your operating system

```bash
uv add "mcp[cli]"
mcp install server.py --name "CyberChef API MCP Server"
```

> [!TIP]
> After running the above command you can then tweak the client configuration to include the environment variable for the CyberChef API URL

```json
{
 "mcpServers": {
   "CyberChef API MCP Server": {
     "command": "uv",
     "args": [
       "run",
       "--with",
       "mcp[cli]",
       "--directory",
       "cyberchef-api-mcp-server/cyberchef_api_mcp_server/",
       "mcp",
       "run",
       "server.py"
     ],
     "env": {
       "CYBERCHEF_API_URL": "your-cyberchef-api-url"
     }
   }
 }
}
```

🔍 Demo
---
Using the MCP server in this example use case, the following prerequisites apply: 
- You must have Claude desktop installed
- Have a running CyberChef API instance or one you are able to use

Here is a basic prompt being solved using the MCP server tools:
<img width="1511" src="https://github.com/user-attachments/assets/657f52b3-43eb-4c3b-94f1-289fc12817b2" />

🙇 References
---
- [CyberChef](https://github.com/gchq/CyberChef)
- [CyberChef Server](https://github.com/gchq/CyberChef-server)
- [Model Context Protocol](https://github.com/modelcontextprotocol)
- [FastMCP](https://github.com/jlowin/fastmcp)

🪪 License
---
MIT License

## Hosted deployment

A hosted deployment is available on [Fronteir AI](https://fronteir.ai/mcp/slouchd-cyberchef-api-mcp-server).

