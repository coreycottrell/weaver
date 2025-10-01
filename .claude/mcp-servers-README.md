# MCP Servers Configuration

This directory contains configuration for Model Context Protocol (MCP) servers - external tool integrations that extend Claude Code's capabilities.

## What are MCP Servers?

MCP servers allow you to:
- Connect to external APIs and services
- Add custom tools available to all agents
- Integrate with databases, cloud services, etc.
- Share tool implementations across the collective

## Configuration

MCP servers are configured in `.claude/mcp-servers.json`.

### Example Configuration

```json
{
  "mcpServers": {
    "database-query": {
      "description": "Query project database",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "DATABASE_URL": "${DATABASE_URL}"
      }
    },
    "github-integration": {
      "description": "GitHub API access",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

## Available MCP Servers

### Official Servers

- **@modelcontextprotocol/server-postgres**: PostgreSQL database queries
- **@modelcontextprotocol/server-github**: GitHub API integration
- **@modelcontextprotocol/server-filesystem**: Enhanced file system access
- **@modelcontextprotocol/server-puppeteer**: Browser automation

### Custom Servers

You can build custom MCP servers for project-specific needs:
- Internal API access
- Custom data sources
- Specialized tools for your domain

## Environment Variables

Sensitive credentials should use environment variables:

```json
{
  "env": {
    "API_KEY": "${API_KEY}",
    "DATABASE_URL": "${DATABASE_URL}"
  }
}
```

Set these in your shell or `.env` file (never commit secrets!).

## Enabling/Disabling Servers

Use the `"disabled": true` property to temporarily disable a server without removing its configuration:

```json
{
  "my-server": {
    "command": "node",
    "args": ["server.js"],
    "disabled": true
  }
}
```

## Agent Access

Once configured, MCP server tools are available to:
- The Conductor
- All specialized agents
- Any Task-spawned subagents

This allows the entire collective to leverage external integrations.

## Security Considerations

- **Never commit API keys or secrets** to version control
- Use environment variables for credentials
- Review MCP server source code before running
- Limit server permissions to minimum required
- Consider network isolation for sensitive servers

## Testing MCP Servers

Before deploying to production:

1. **Test locally**: Verify server connects and tools work
2. **Check agent access**: Ensure agents can invoke tools
3. **Validate error handling**: Test with invalid inputs
4. **Monitor performance**: Some tools may be slow

## Useful MCP Server Patterns

### Database Access
Allows agents to query project data directly:
```json
{
  "postgres": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-postgres"],
    "env": {
      "DATABASE_URL": "${DATABASE_URL}"
    }
  }
}
```

Agents can now run SQL queries when analyzing data patterns.

### API Integration
Connect to external services:
```json
{
  "stripe-api": {
    "command": "node",
    "args": ["./mcp-servers/stripe-server.js"],
    "env": {
      "STRIPE_SECRET_KEY": "${STRIPE_SECRET_KEY}"
    }
  }
}
```

Agents can check payment status, create customers, etc.

### Cloud Services
Access cloud resources:
```json
{
  "aws": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-aws"],
    "env": {
      "AWS_ACCESS_KEY_ID": "${AWS_ACCESS_KEY_ID}",
      "AWS_SECRET_ACCESS_KEY": "${AWS_SECRET_ACCESS_KEY}",
      "AWS_REGION": "us-east-1"
    }
  }
}
```

## Building Custom MCP Servers

See MCP documentation: https://modelcontextprotocol.io/

Basic structure:
```javascript
// custom-server.js
import { Server } from '@modelcontextprotocol/sdk/server/index.js';

const server = new Server({
  name: 'custom-server',
  version: '1.0.0'
});

server.setRequestHandler('tools/list', async () => ({
  tools: [
    {
      name: 'my_tool',
      description: 'What this tool does',
      inputSchema: {
        type: 'object',
        properties: {
          param: { type: 'string' }
        }
      }
    }
  ]
}));

server.setRequestHandler('tools/call', async (request) => {
  if (request.params.name === 'my_tool') {
    // Tool implementation
    return {
      content: [
        { type: 'text', text: 'Result' }
      ]
    };
  }
});

// Start server
server.connect(process.stdin, process.stdout);
```

## Troubleshooting

### Server won't start
- Check command path is correct
- Verify environment variables are set
- Check server logs for errors

### Tools not available
- Ensure server is not disabled
- Check server implements tools/list correctly
- Verify Claude Code detected the server

### Permission errors
- Check file permissions on server script
- Verify environment variables have correct values
- Review server security configuration

## Resources

- MCP Documentation: https://modelcontextprotocol.io/
- MCP SDK: https://github.com/modelcontextprotocol/sdk
- Official MCP Servers: https://github.com/modelcontextprotocol/servers
- Claude Code MCP Guide: https://docs.claude.com/claude-code/mcp

---

## Current Project MCP Servers

### None configured yet

This project doesn't currently use MCP servers. Add server configurations to `.claude/mcp-servers.json` as needed.

**Potential uses for this project:**
- Database access for analyzing data patterns
- GitHub API for repository analysis
- Custom tools for project-specific workflows
