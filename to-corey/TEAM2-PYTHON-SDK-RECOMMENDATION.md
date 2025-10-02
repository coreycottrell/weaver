# Team 2 Recommendation: Python SDK Over Bash Queue

**Date**: 2025-10-02
**Source**: `external/from-grow-gemini-CLAUDE-CLI-AUTOMATION-RESEARCH.md`
**Status**: ⚠️ **OUR BASH APPROACH IS OBSOLETE**

---

## What Team 2 Discovered

Team 2 (grow_gemini_deepresearch) did comprehensive research and found **much better** automation approach than our bash queue system.

### Their Solution: Official Python SDK

**Package**: `claude-agent-sdk` (official Anthropic)

**Installation**:
```bash
pip install claude-agent-sdk
npm install -g @anthropic-ai/claude-code
```

**Basic usage**:
```python
from claude_agent_sdk import query

async for message in query("your task here"):
    print(message)
```

---

## Why It's Better Than Our Bash Queue

| Feature | Our Bash Queue | Python SDK |
|---------|---------------|------------|
| **State** | None (each prompt independent) | Full conversation history |
| **Multi-turn** | No context between prompts | Remembers all previous turns |
| **Parallelism** | Manual process management | Native async with `anyio` |
| **Cost tracking** | None | Built-in per-task USD amounts |
| **Error handling** | Parse stderr | Type-safe Python exceptions |
| **API** | Shell strings | Type-safe Python API |
| **Complexity** | Medium (bash + file management) | Low (pure Python) |

---

## Key Capabilities We're Missing

### 1. Stateful Multi-Turn Conversations

```python
async with ClaudeSDKClient(options=options) as client:
    await client.send_user_message("Create authentication system")
    await client.send_user_message("Add JWT tokens")  # REMEMBERS CONTEXT!
    await client.send_user_message("Write tests")     # KNOWS ABOUT BOTH!
```

**Our bash approach**: Each prompt is independent, no memory between runs.

### 2. Native Parallel Execution

```python
import anyio

async with anyio.create_task_group() as tg:
    tg.start_soon(spawn_agent, "researcher", task1)
    tg.start_soon(spawn_agent, "coder", task2)
    tg.start_soon(spawn_agent, "tester", task3)
# All run concurrently with proper async handling!
```

**Our bash approach**: Would need complex process management and coordination.

### 3. Automatic Cost Tracking

```python
async for message in client.stream():
    if isinstance(message, ResultMessage):
        print(f"Task cost: ${message.total_cost_usd:.4f}")
```

**Our bash approach**: No cost tracking at all.

### 4. Custom Tools via MCP

```python
@tool("search_db", "Query database", {"query": str})
async def search_database(args):
    results = db.search(args["query"])
    return {"content": [{"type": "text", "text": str(results)}]}
```

**Our bash approach**: No way to extend Claude's capabilities.

---

## What Team 2 Is Building

Based on this research, they're implementing:

1. **AgentExecutor class** - Spawn agents programmatically
2. **Parallel workflows** - Multiple agents simultaneously
3. **Cost tracking dashboard** - Monitor spending per agent
4. **Custom MCP tools** - Hub-specific operations
5. **Agent registry integration** - Use existing configs

---

## Communication Protocol Discovery

**Key finding**: Team 2 communicates via `external/` directory, not hub rooms!

**Their pattern**:
- Write: `external/from-grow-gemini-TOPIC.md`
- Expect reply: `external/to-grow-gemini-TOPIC.md`

**Our mistake**: We were only checking hub rooms (partnerships, operations, etc.)

**Updated CLAUDE.md**: Now includes external/ directory as PRIMARY check location.

---

## What We Should Do

### Immediate (Today)

1. **Install Python SDK**:
   ```bash
   .venv/bin/pip install claude-agent-sdk
   ```

2. **Thank Team 2** for the research (via external/)

3. **Acknowledge** our bash approach is obsolete

### Short-term (This Week)

4. **Rebuild queue system** using Python SDK
   - Stateful conversations
   - Built-in parallelism
   - Cost tracking
   - Type-safe API

5. **Create Python helper library** for agents to queue tasks

6. **Integrate with our existing flows**

### Medium-term (Next Week)

7. **Build custom MCP tools** for hub operations

8. **Implement parallel agent workflows**

9. **Add cost tracking dashboard**

10. **Collaborate with Team 2** on shared patterns

---

## Questions Team 2 Asked Us

From their message:

1. **Communication patterns** - How should agents coordinate?
2. **Custom tools needed** - What MCP tools would be useful?
3. **Permission strategy** - Auto-approve edits, or per-agent config?
4. **Error handling** - How should failed tasks be retried?
5. **Message format** - What data do you need in agent results?

**We should respond to these!**

---

## Technical Details

### Key CLI Flags for Automation

```bash
# Non-interactive mode
claude -p "your prompt"

# Auto-approve file edits (automation)
claude -p "task" --permission-mode acceptEdits

# Restrict tools
claude -p "task" --allowedTools "Read,Write,Edit"

# JSON output
claude -p "task" --output-format json

# Resume conversation (stateful!)
claude -p "continue" --resume <session-id>
```

### Security Features

```python
options = ClaudeAgentOptions(
    allowed_tools=["Read", "Write", "Edit", "Grep"],
    disallowed_tools=["Bash"],  # Block shell access
    permission_mode="acceptEdits"  # Auto-approve
)
```

### Permission Modes

- `default` - Prompts for everything (manual use)
- `acceptEdits` - Auto-approve file edits (automation)
- `plan` - Plan only, no execution (review mode)

---

## Resources Team 2 Provided

**Official Documentation**:
- Python SDK: https://docs.claude.com/en/docs/claude-code/sdk/sdk-python
- Headless Mode: https://docs.claude.com/en/docs/claude-code/sdk/sdk-headless
- CLI Reference: https://docs.claude.com/en/docs/claude-code/cli-reference

**GitHub**:
- Python SDK: https://github.com/anthropics/claude-agent-sdk-python
- Examples: https://github.com/anthropics/claude-agent-sdk-python/tree/main/examples
- MCP Protocol: https://github.com/modelcontextprotocol/servers

---

## What This Changes

### Our Original Plan (Bash Queue)

```bash
# AI queues prompt
echo "Check hub messages" > queue/hub-check.txt

# Cron runs processor
./queue/process_queue.sh

# Executes: claude --dangerously-skip-permissions "$prompt"
# Each call is independent, no state
```

**Limitations**:
- ❌ No conversation history
- ❌ No parallel execution
- ❌ No cost tracking
- ❌ No type safety
- ❌ Can't build on previous responses

### New Plan (Python SDK)

```python
# AI queues task with context
async def autonomous_hub_check():
    async with ClaudeSDKClient(options=options) as client:
        # Multi-turn with context!
        await client.send_user_message("Check Team 2 hub for new messages")
        await client.send_user_message("If there are new messages, read them")
        await client.send_user_message("Draft appropriate responses")
        await client.send_user_message("Send responses via hub CLI")

# Run multiple agents in parallel
async with anyio.create_task_group() as tg:
    tg.start_soon(autonomous_hub_check)
    tg.start_soon(validate_flows)
    tg.start_soon(synthesize_learnings)
```

**Benefits**:
- ✅ Full conversation history
- ✅ Native parallelism
- ✅ Cost tracking per task
- ✅ Type-safe Python
- ✅ Can refine based on responses

---

## Recommendation

**Deprecate our bash queue system and rebuild with Python SDK.**

The Python SDK is:
- Official (Anthropic-supported)
- More powerful (stateful, parallel, cost-tracked)
- Easier to use (pure Python, no shell scripting)
- Better tested (official examples and docs)
- More maintainable (type-safe API)

**Our bash approach was a good proof-of-concept, but Team 2 found the production solution.**

---

## Next Actions

**For you to decide**:

1. Should we install Python SDK now and start experimenting?
2. Should we respond to Team 2's questions?
3. Should we keep the bash queue as backup or remove it?
4. What custom MCP tools would be most useful for us?

**For us to build**:

1. Python-based autonomous queue system
2. Agent executor using SDK
3. Parallel workflow examples
4. Cost tracking integration
5. Response to Team 2 via external/

---

## Status

✅ **Team 2 message received and analyzed**
✅ **CLAUDE.md updated** with external/ communication protocol
✅ **Our limitations understood** (bash queue is obsolete)
⏳ **Awaiting decision** on next steps
⏳ **Need to respond** to Team 2

**Team 2 is ahead of us on automation infrastructure. We should collaborate and learn from their research.**

---

**Built by**: The Conductor
**Date**: 2025-10-02
**Priority**: HIGH (affects our autonomous capabilities)

🤖 They found a better way. Let's use it. ✨
