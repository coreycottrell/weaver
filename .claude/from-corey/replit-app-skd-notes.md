# ChatGPT MCP Integration Guide: Fixing Tool Discovery Issues

## The Problem We Solved

When building an MCP (Model Context Protocol) server for ChatGPT integration, the app badge appeared in ChatGPT, but ChatGPT couldn't discover any tools. The server was running, but returning "Not Found" for tool discovery requests.

### Symptoms
- ✅ App badge visible in ChatGPT developer mode
- ❌ No tools showing up in ChatGPT
- ❌ `/mcp/messages` endpoint returning "Not Found"
- ❌ ChatGPT making `list_resources` and `api_tool` requests with no results

## Root Cause

The server was using **low-level MCP protocol handlers** instead of the modern **FastMCP 2.x decorator pattern**. This prevented proper tool registration and discovery.

### What Was Wrong

**❌ Old Pattern (Broken):**
```python
import mcp.types as types
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="my-server")

# Manually registering tools with low-level API
@mcp._mcp_server.list_tools()
async def _list_tools() -> List[types.Tool]:
    return [
        types.Tool(
            name="my_tool",
            description="Does something",
            inputSchema={...}
        )
    ]

# Manually handling tool calls
async def _call_tool_request(req: types.CallToolRequest):
    # Complex manual handling
    pass

mcp._mcp_server.request_handlers[types.CallToolRequest] = _call_tool_request
```

**Problems with this approach:**
1. Tools not properly registered in FastMCP's internal registry
2. Endpoints not correctly exposed for ChatGPT discovery
3. Manual protocol handling bypasses FastMCP's automatic setup
4. Fragile and version-dependent

## The Solution: FastMCP 2.x Decorator Pattern

**✅ Modern Pattern (Works):**

```python
from fastmcp import FastMCP

mcp = FastMCP(name="my-server")

@mcp.tool()
def my_tool(param: str, limit: int = 5) -> dict:
    """Clear description of what this tool does.
    
    Args:
        param: Description of param
        limit: Number of results (default: 5)
    
    Returns:
        Dictionary containing results
    """
    return {
        "data": "result",
        "message": "Success"
    }
```

**Why this works:**
1. ✅ FastMCP automatically registers tools
2. ✅ Proper endpoint configuration
3. ✅ Type hints automatically generate JSON schemas
4. ✅ Docstrings become tool descriptions
5. ✅ Future-proof against MCP updates

## Complete Working Implementation

### 1. Basic MCP Server with Tools

```python
from fastmcp import FastMCP
from typing import Dict, List
import os

mcp = FastMCP(name="ai-civ-blog")

@mcp.tool()
def list_blog_posts(limit: int = 5) -> dict:
    """Shows latest blog posts from AI Civilization.
    
    Args:
        limit: Number of posts to return (1-10)
    
    Returns:
        Dictionary with posts array and metadata
    """
    posts = fetch_posts()  # Your data fetching logic
    return {
        "posts": posts[:limit],
        "count": len(posts),
        "message": f"Found {len(posts)} posts"
    }

@mcp.tool()
def read_post(post_id: str) -> dict:
    """Read a specific blog post by ID.
    
    Args:
        post_id: The unique identifier of the post
    
    Returns:
        Full post details or error message
    """
    post = find_post(post_id)
    if not post:
        return {"error": f"Post not found: {post_id}"}
    return {"post": post}
```

### 2. Adding Custom Routes (Homepage, Health Check)

```python
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.responses import HTMLResponse, JSONResponse
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
import pathlib
import uvicorn

# Homepage route
async def homepage(request: Request):
    html = """
    <html>
        <head><title>My MCP Server</title></head>
        <body>
            <h1>MCP Server Running</h1>
            <p>Connect this server to ChatGPT at: <code>/mcp</code></p>
        </body>
    </html>
    """
    return HTMLResponse(html)

# Health check
async def healthz(request: Request):
    return JSONResponse({
        "ok": True,
        "status": "running",
        "service": "my-mcp-server"
    })

# Get FastMCP app (has /mcp route built-in)
mcp_app = mcp.http_app()

# Add custom routes
custom_routes = [
    Route("/", homepage),
    Route("/healthz", healthz),
]

# Add static files if needed
assets_dir = pathlib.Path(__file__).parent / "assets"
if assets_dir.exists():
    custom_routes.append(
        Mount("/assets", StaticFiles(directory=str(assets_dir)), name="assets")
    )

# Insert custom routes into MCP app
for route in reversed(custom_routes):
    mcp_app.routes.insert(0, route)

app = mcp_app

# Add CORS for ChatGPT
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://chat.openai.com",
        "https://chatgpt.com",
        "*"  # Remove in production
    ],
    allow_methods=["GET", "POST", "OPTIONS", "DELETE"],
    allow_headers=["*"],
    allow_credentials=False,
    expose_headers=["*"],
)

if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
```

### 3. Critical Routing Details

**⚠️ IMPORTANT:** FastMCP's `http_app()` already includes a `/mcp` route internally.

**❌ Wrong (creates /mcp/mcp):**
```python
routes = [
    Mount("/mcp", mcp.http_app(), name="mcp"),  # Wrong!
]
app = Starlette(routes=routes)
```

**✅ Correct (MCP at /mcp):**
```python
mcp_app = mcp.http_app()  # Already has /mcp built-in
# Add your custom routes to it
for route in custom_routes:
    mcp_app.routes.insert(0, route)
app = mcp_app
```

## Testing Your MCP Server

### 1. Health Check
```bash
curl http://localhost:5000/healthz
# Should return: {"ok":true,"status":"running"}
```

### 2. MCP Endpoint (Basic)
```bash
curl -X POST http://localhost:5000/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
```

**Expected behavior:**
- Without proper headers: `406 Not Acceptable` or `400 Bad Request`
- With session: Returns tool list
- This is NORMAL - ChatGPT will establish proper sessions

### 3. Verify Tools Load
```bash
cd your_server_dir && python -c "
from main import mcp
tools = mcp._mcp_server._tool_manager._tools
print(f'Registered tools: {list(tools.keys())}')
"
```

## Deployment Checklist

### For Replit
- [x] Server binds to `0.0.0.0:${PORT}`
- [x] PORT environment variable used
- [x] CORS configured for ChatGPT domains
- [x] Health check endpoint at `/healthz`
- [x] MCP endpoint at `/mcp`

### For ChatGPT Integration
- [x] Tools use `@mcp.tool()` decorator
- [x] Docstrings describe tool purpose
- [x] Type hints for all parameters
- [x] Return dictionaries (JSON-serializable)
- [x] Error handling returns error messages in dict

## Common Pitfalls

### 1. Using Deprecated Methods
```python
# ❌ Deprecated
mcp.streamable_http_app()

# ✅ Use instead
mcp.http_app()
```

### 2. Wrong Transport for ChatGPT
```python
# ❌ SSE creates /sse endpoint (not /mcp)
mcp.run(transport="sse")

# ✅ HTTP creates /mcp endpoint
mcp.run(transport="http")
# Or mount mcp.http_app() in Starlette
```

### 3. Missing Accept Headers
MCP endpoints require specific headers. Don't worry if manual testing fails - ChatGPT sends correct headers automatically.

### 4. Complex Return Types
```python
# ❌ ChatGPT can't parse this
@mcp.tool()
def bad_tool() -> SomeCustomClass:
    return SomeCustomClass()

# ✅ Always return dicts
@mcp.tool()
def good_tool() -> dict:
    return {"data": "value", "status": "ok"}
```

## Debugging Tips

### Check FastMCP Version
```bash
pip show fastmcp | grep Version
# Should be 2.x or higher
```

### Enable Debug Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Verify Tool Registration
```python
# After defining tools
print("Registered tools:", mcp._mcp_server._tool_manager._tools.keys())
```

### Monitor ChatGPT Requests
Watch your server logs when ChatGPT connects. You should see:
- `POST /mcp` - Tool discovery
- Session establishment
- Tool invocations

## Key Takeaways

1. **Use `@mcp.tool()` decorator** - Don't manually register tools
2. **FastMCP http_app() has /mcp built-in** - Don't double-mount
3. **Return plain dicts** - Keep responses JSON-serializable
4. **Docstrings matter** - They become tool descriptions in ChatGPT
5. **Type hints auto-generate schemas** - Use them correctly
6. **CORS is required** - Allow ChatGPT domains
7. **Error responses as dicts** - `{"error": "message"}` format

## Success Indicators

When working correctly:
- ✅ ChatGPT shows your tools in developer mode
- ✅ Tool descriptions appear from docstrings
- ✅ ChatGPT can invoke tools with parameters
- ✅ Results display in chat
- ✅ Server logs show successful tool calls

## Resources

- FastMCP Docs: https://gofastmcp.com
- MCP Protocol: https://modelcontextprotocol.io
- OpenAI MCP Guide: https://platform.openai.com/docs/mcp

---

**Created from real debugging experience** - This guide documents actual issues encountered and solutions that worked in production.
