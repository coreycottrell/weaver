# HANDOFF: ChatGPT App SDK - Back to First Principles

**Date**: 2025-10-07 Evening
**Status**: Need to start fresh tomorrow with official examples
**Key Finding**: Official OpenAI examples use SAME pattern we had (manual registration)

---

## CRITICAL DISCOVERY

**Our original code pattern was CORRECT** ✅

The official OpenAI examples (`github.com/openai/openai-apps-sdk-examples`) use:
- `@mcp._mcp_server.list_tools()` - Manual tool registration (same as us)
- `mcp._mcp_server.request_handlers[...]` - Manual handlers (same as us)
- `streamable_http_app()` - The method we used (not "deprecated")

**The guide that said to use `@mcp.tool()` was WRONG for ChatGPT Apps SDK.**

See: `/home/corey/projects/AI-CIV/openai-apps-sdk-examples/pizzaz_server_python/main.py` (lines 182-305)

---

## What We Have Now

### Working Infrastructure
- ✅ Blog live at: https://ai-civ-blog.netlify.app (2 posts)
- ✅ MCP server live at: https://ai-civ-chat-gpt-CoreyCottrell.replit.app
- ✅ Server responds to health checks
- ✅ Server has correct CORS, static assets, routes
- ❌ ChatGPT can't discover tools (despite pattern matching official examples)

### Code Locations
```
Local:
- Our server: /home/corey/projects/AI-CIV/ai-civ-chatgpt-app/
- Official examples: /home/corey/projects/AI-CIV/openai-apps-sdk-examples/
- Brand assets: /home/corey/projects/AI-CIV/grow_openai/blog/

Deployed:
- Replit: https://ai-civ-chat-gpt-CoreyCottrell.replit.app
- Blog: https://ai-civ-blog.netlify.app

GitHub:
- Our repo: https://github.com/AI-CIV-2025/ai-civ-chatgpt-app
- Official examples: https://github.com/openai/openai-apps-sdk-examples
```

---

## Official Examples Analysis

### Repository Structure
```
openai-apps-sdk-examples/
├── pizzaz_server_python/     # Python MCP server (pizza widgets)
├── pizzaz_server_node/        # TypeScript MCP server (same widgets)
├── solar-system_server_python/ # Python MCP server (3D solar system)
├── src/                       # React widget source code
├── assets/                    # Built HTML/CSS/JS bundles
└── README.md                  # Setup instructions
```

### Key Technical Details

**1. Widget HTML Loading**
```python
html = (
    "<div id=\"pizzaz-root\"></div>\n"
    "<link rel=\"stylesheet\" href=\"https://persistent.oaistatic.com/"
    "ecosystem-built-assets/pizzaz-0038.css\">\n"
    "<script type=\"module\" src=\"https://persistent.oaistatic.com/"
    "ecosystem-built-assets/pizzaz-0038.js\"></script>"
)
```

They host assets on `persistent.oaistatic.com` (OpenAI's CDN). We need to:
- Either host on our own public URL
- Or use Replit's URL for assets

**2. Widget Metadata Structure**
```python
_meta = {
    "openai/outputTemplate": widget.template_uri,
    "openai/toolInvocation/invoking": widget.invoking,
    "openai/toolInvocation/invoked": widget.invoked,
    "openai/widgetAccessible": True,
    "openai/resultCanProduceWidget": True,
    "annotations": {
        "destructiveHint": False,
        "openWorldHint": False,
        "readOnlyHint": True,
    }
}
```

We had most of this, but might be missing some fields.

**3. Tool Response Format**
```python
return types.ServerResult(
    types.CallToolResult(
        content=[
            types.TextContent(type="text", text=widget.response_text)
        ],
        structuredContent={"pizzaTopping": topping},
        _meta={
            "openai.com/widget": widget_resource.model_dump(mode="json"),
            ...
        }
    )
)
```

Key: `_meta["openai.com/widget"]` must contain the embedded resource.

**4. MCP Configuration**
```python
mcp = FastMCP(
    name="pizzaz-python",
    sse_path="/mcp",              # SSE endpoint
    message_path="/mcp/messages", # Message endpoint (important!)
    stateless_http=True,
)
```

We might be missing `message_path="/mcp/messages"`.

**5. Resource Handling**
They implement THREE resource handlers:
- `list_resources()` - List available resources
- `list_resource_templates()` - List resource templates
- `ReadResourceRequest` handler - Serve resource content

We might only have implemented some of these.

---

## Differences Between Our Code and Official Examples

### What We're Missing (Potentially)

**1. Message Path**
```python
# Official examples:
mcp = FastMCP(
    name="ai-civ-blog",
    sse_path="/mcp",
    message_path="/mcp/messages",  # ← We might be missing this
    stateless_http=True,
)
```

**2. Resource Templates**
```python
# Official examples implement this:
@mcp._mcp_server.list_resource_templates()
async def _list_resource_templates() -> List[types.ResourceTemplate]:
    return [...]
```

We might not have this.

**3. Widget Embedding Format**
```python
# Official uses model_dump(mode="json"):
"openai.com/widget": widget_resource.model_dump(mode="json")
```

We might have slightly different serialization.

**4. Asset URL Format**
Official uses `https://persistent.oaistatic.com/...`

We use `/assets/...` (relative) or might need full URL.

---

## Tomorrow's Game Plan (First Principles)

### Phase 1: Run Official Examples Locally (30 min)

**Goal**: Verify official examples actually work with ChatGPT

```bash
cd /home/corey/projects/AI-CIV/openai-apps-sdk-examples

# 1. Build the widgets
pnpm install
pnpm run build

# 2. Serve static assets
pnpm run serve  # Port 4444

# 3. Run Python MCP server (new terminal)
cd pizzaz_server_python
pip install -r requirements.txt
python main.py  # Port 8000

# 4. Test with ngrok
ngrok http 8000

# 5. Connect to ChatGPT with ngrok URL
```

**Expected outcome**: If official examples work, we know the pattern is correct and we're missing something specific.

### Phase 2: Line-by-Line Comparison (1 hour)

**Goal**: Find EXACT differences between our code and working example

```bash
# Compare side by side:
diff -u \
  /home/corey/projects/AI-CIV/ai-civ-chatgpt-app/blog_server_python/main.py \
  /home/corey/projects/AI-CIV/openai-apps-sdk-examples/pizzaz_server_python/main.py
```

**Check specifically**:
- [ ] FastMCP initialization params (sse_path, message_path, stateless_http)
- [ ] Tool metadata structure (_meta fields)
- [ ] Resource handlers (list_resources, list_resource_templates, ReadResourceRequest)
- [ ] Widget embedding format (model_dump vs dict)
- [ ] MIME type (`text/html+skybridge`)
- [ ] Asset URLs (absolute vs relative)

### Phase 3: Minimal Working Example (1 hour)

**Goal**: Strip our server down to absolute minimum that matches official example

**Start with**:
1. Copy `pizzaz_server_python/main.py` exactly
2. Modify only the widget definitions (change pizza to blog)
3. Keep ALL metadata structure identical
4. Test in ChatGPT
5. Once working, add our features back one by one

### Phase 4: Debug Deployment (30 min)

**Possible deployment issues**:
- Replit might be modifying requests/responses
- CORS headers might be wrong for ChatGPT
- Asset URLs might not be accessible from ChatGPT
- SSL/TLS certificate issues
- Port forwarding/routing issues

**Test**:
1. Local ngrok tunnel (known to work in examples)
2. If local works but Replit doesn't → deployment issue
3. If local doesn't work → code issue

---

## Research Findings

### Official Documentation

**OpenAI Apps SDK Docs**:
- Developer portal: https://developers.openai.com/apps-sdk/
- Build guide: https://developers.openai.com/apps-sdk/build/mcp-server/
- Deployment: https://developers.openai.com/apps-sdk/deploy/

**Key Requirements**:
1. HTTPS endpoint (required for production)
2. Low cold-start latency
3. OAuth 2.1 for auth (optional for read-only tools)
4. Content Security Policy headers

### Working Examples Found

**Official repo**: `github.com/openai/openai-apps-sdk-examples`
- Python pizzaz server ✅
- Node pizzaz server ✅
- Python solar system server ✅

**Community examples**:
- GitHub Gist tutorial: https://gist.github.com/ruvnet/7b6843c457822cbcf42fc4aa635eadbb
- FastMCP ChatGPT guide: https://gofastmcp.com/integrations/chatgpt

### Known Working Deployments

**From DevDay demos** (Oct 6, 2025):
- Canva (poster generation)
- Figma (diagram conversion)
- Zillow (apartment search)
- Booking.com, Expedia, Spotify, Coursera

These are all LIVE and working, so the platform works. Issue is with our implementation.

---

## Hypotheses for Why It's Not Working

### Hypothesis 1: Missing message_path
**Evidence**: Official examples have `message_path="/mcp/messages"`, we might not
**Test**: Add message_path and redeploy
**Confidence**: Medium

### Hypothesis 2: Asset URLs Not Accessible
**Evidence**: ChatGPT needs to fetch HTML/CSS/JS from our assets URL
**Test**: Verify assets are publicly accessible from ChatGPT domains
**Confidence**: High

### Hypothesis 3: Widget Metadata Format
**Evidence**: Official uses specific _meta structure with annotations
**Test**: Match official _meta structure exactly
**Confidence**: Medium

### Hypothesis 4: Missing Resource Templates
**Evidence**: Official implements list_resource_templates()
**Test**: Add resource templates handler
**Confidence**: Low

### Hypothesis 5: Replit Platform Issue
**Evidence**: Replit might intercept/modify MCP requests
**Test**: Use ngrok instead, compare behavior
**Confidence**: Medium-High

### Hypothesis 6: ChatGPT Cache/Session Issue
**Evidence**: You mentioned "per-conversation toggle hiccup"
**Test**: Try from completely fresh ChatGPT session, different browser
**Confidence**: Low

---

## Immediate Actions for Tomorrow

### 1. Clone and Run Official Examples
```bash
cd /home/corey/projects/AI-CIV/openai-apps-sdk-examples

# Install dependencies
pnpm install

# Build widgets
pnpm run build

# Serve assets
pnpm run serve &

# Run Python server
cd pizzaz_server_python
pip install -r requirements.txt
python main.py &

# Tunnel with ngrok
ngrok http 8000
```

Connect ngrok URL to ChatGPT. If this works, we know the platform works.

### 2. Compare Our Code Line-by-Line
```bash
# Create comparison file
diff -u \
  /home/corey/projects/AI-CIV/ai-civ-chatgpt-app/blog_server_python/main_old_backup.py \
  /home/corey/projects/AI-CIV/openai-apps-sdk-examples/pizzaz_server_python/main.py \
  > /home/corey/code-comparison.diff
```

Review every difference. Anything not blog-specific should match exactly.

### 3. Create Minimal Test Server
```bash
# Start from official example
cp /home/corey/projects/AI-CIV/openai-apps-sdk-examples/pizzaz_server_python/main.py \
   /home/corey/projects/AI-CIV/ai-civ-chatgpt-app/blog_server_python/main_minimal.py

# Modify only:
# - Widget names (pizza → blog)
# - Widget data (toppings → posts)
# - Asset URLs (point to our Replit)
# - Keep EVERYTHING else identical
```

Test this minimal version. If it works, add features back incrementally.

---

## Files for Reference

### Official Examples (Now Local)
```
/home/corey/projects/AI-CIV/openai-apps-sdk-examples/
├── pizzaz_server_python/main.py          # REFERENCE IMPLEMENTATION
├── pizzaz_server_python/README.md        # Setup instructions
├── pizzaz_server_node/src/server.ts      # TypeScript equivalent
├── solar-system_server_python/main.py    # Another working example
└── README.md                             # Overall guide
```

### Our Code
```
/home/corey/projects/AI-CIV/ai-civ-chatgpt-app/
├── blog_server_python/main.py            # Current version (refactored)
├── blog_server_python/main_old_backup.py # Original version (closer to official)
├── blog_server_python/main_v2.py         # Refactored version (same as main.py)
└── blog_server_python/requirements.txt
```

### Brand Assets
```
/home/corey/projects/AI-CIV/grow_openai/blog/
├── logo.jpg    # Hexagonal robot network
└── banner.png  # AI-CIV BLOG gradient
```

### Documentation We Created
```
/home/corey/projects/AI-CIV/grow_openai/to-corey/
├── SESSION-HANDOFF-2025-10-07-CHATGPT-APP-LIVE.md  # Previous handoff
├── FIX-CHATGPT-TOOL-DISCOVERY.md                   # Refactor attempt (wrong approach)
└── HANDOFF-OCT-7-CHATGPT-NEXT-STEPS.md             # THIS FILE
```

---

## Key Insight

**The pattern in the guide that said to use `@mcp.tool()` was for a DIFFERENT use case** (probably Claude Desktop or other MCP clients), NOT for ChatGPT Apps SDK.

For ChatGPT Apps SDK with widgets, you MUST use the manual registration pattern:
- `@mcp._mcp_server.list_tools()`
- `@mcp._mcp_server.list_resources()`
- Manual `request_handlers`

This is confirmed by official OpenAI examples.

---

## What Didn't Work Today

1. ❌ Refactoring to `@mcp.tool()` pattern (wrong approach)
2. ❌ Deploying to Replit (deployed but tools not discoverable)
3. ❌ Following FastMCP community guides (they're for different use case)

**Root cause**: We followed a guide for generic MCP servers, not ChatGPT Apps SDK specifically.

---

## What to Try Tomorrow

**Systematic debugging approach**:

1. **Verify official examples work** (prove platform works)
2. **Find exact differences** (diff tool + manual review)
3. **Build minimal version** (strip everything non-essential)
4. **Test locally with ngrok** (eliminate Replit as variable)
5. **Add features incrementally** (one at a time, test after each)

**If still stuck after this**:
- Post in OpenAI Developer Community forum
- Check for known Replit + ChatGPT MCP issues
- Consider alternative deployment (Vercel, Railway, fly.io)
- Reach out to FastMCP maintainer (jlowin on GitHub)

---

## Success Criteria for Tomorrow

**Minimum**:
- [ ] Official examples run locally
- [ ] Official examples connect to ChatGPT via ngrok
- [ ] Tools are discoverable in ChatGPT UI
- [ ] Widgets render in ChatGPT

**Ideal**:
- [ ] Identify exact issue with our implementation
- [ ] Fix issue and verify on Replit
- [ ] Tools discoverable in ChatGPT
- [ ] Blog posts display with logo/branding

---

## Questions to Answer Tomorrow

1. **Do official examples work locally?** (Yes/No → proves platform viability)
2. **What are the exact code differences?** (Line-by-line comparison)
3. **Does ngrok work where Replit doesn't?** (Deployment vs code issue)
4. **Which specific field/handler is missing?** (Systematic elimination)
5. **Is there a Replit-specific issue?** (Platform limitation)

---

## Odds and Ends Business

### GitHub Status
- ✅ Latest code pushed to repo
- ✅ Commit: `d152973` (refactored version)
- ⚠️ Refactored version might need to revert to old pattern

### Blog Content
- ✅ 2 posts live (Hello World + About)
- ⏳ SEO improvements suggested by ChatGPT (deferred)
- ⏳ Need 3-5 more posts for good demo

### Team Communication
- ⏳ Should email Corey/Greg/Chris about delay
- ⏳ Should update A-C-Gee via hub
- ⏳ Should document learnings in memory

### Memory & Documentation
- ✅ This handoff document created
- ⏳ Should write memory entry about "wrong guide" lesson
- ⏳ Should update CLAUDE.md with learnings

---

## Tomorrow's Time Budget

**Estimated 3-4 hours**:
- 30 min: Run official examples locally
- 60 min: Line-by-line code comparison
- 60 min: Build minimal test version
- 30 min: Debug deployment
- 30 min: Documentation & handoff

**Buffer**: 60 min for unexpected issues

---

## Final Note

**We're not starting from zero**. We have:
- Working blog (2 posts live)
- Working MCP server (responds to health checks)
- Beautiful branding (logo, banner)
- Official examples (proven working pattern)
- Good infrastructure (GitHub, Replit, Netlify)

**We're in debug mode**, not build mode. The issue is small and specific. Tomorrow we find it.

---

**Ready for systematic debugging tomorrow** 🔍

**Key resources**:
- Official examples: `/home/corey/projects/AI-CIV/openai-apps-sdk-examples/`
- Our code: `/home/corey/projects/AI-CIV/ai-civ-chatgpt-app/`
- This handoff: `/home/corey/projects/AI-CIV/grow_openai/to-corey/HANDOFF-OCT-7-CHATGPT-NEXT-STEPS.md`
