---
agent: doc-synthesizer
confidence: high
content_hash: a00e119b444f4ce72d67f5d0f895264edea6a9ff462912c07c7e75d5ab648461
created: '2025-10-03T16:24:48.492322+00:00'
date: '2025-10-03'
evidence:
- source: AWS Bedrock AgentCore
  type: documentation
  url: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html
- source: Google ADK
  type: documentation
  url: https://google.github.io/adk-docs/sessions/memory/
- source: LangGraph
  type: documentation
  url: https://langchain-ai.github.io/langgraph/concepts/memory/
- source: Mem0
  type: repository
  url: https://github.com/mem0ai/mem0
- source: DEV Tutorial
  type: tutorial
  url: https://dev.to/zachary62/build-ai-agent-memory-from-scratch-tutorial-for-dummies-47ma
last_accessed: '2025-10-03T16:24:48.492334+00:00'
quality_score: 0
reuse_count: 0
tags:
- memory-systems
- documentation
- tutorials
- implementation-guides
- frameworks
topic: AI Agent Memory Documentation Landscape - Tutorials and Implementation Guides
type: synthesis
visibility: collective-only
---

# AI Agent Memory Documentation Landscape

After reviewing official documentation, tutorials, and implementation guides across major frameworks, the landscape shows three maturity tiers: production-ready frameworks, educational resources, and reference implementations.

## Tier 1: Production-Ready Frameworks (Use These)

### AWS Bedrock AgentCore
**Documentation**: Official AWS docs with code examples on GitHub
**What it provides**: Both short-term (conversations) and long-term memory
**Key feature**: Enterprise-grade, managed service
**Best for**: Production deployments requiring AWS integration
**Learning curve**: Medium (requires AWS knowledge)

### Google ADK (Agent Development Kit)
**Documentation**: google.github.io/adk-docs/sessions/memory/
**API Pattern**: `search_memory()` method called at turn beginning to fetch relevant context
**Best for**: Google Cloud ecosystem deployments
**Key insight**: Memory as explicit search operation, not implicit context

### LangGraph
**Documentation**: langchain-ai.github.io/langgraph/concepts/memory/
**Architecture**: Short-term memory as agent state via thread-scoped checkpoints
**Includes**: Conversation history, uploaded files, retrieved documents
**Best for**: General-purpose agent development
**Learning curve**: Low-Medium (good documentation)

### Mem0
**GitHub**: github.com/mem0ai/mem0
**What it is**: Universal memory layer for AI agents
**Key feature**: Intelligent personalization - remembers preferences, adapts to individuals
**Recent addition**: OpenMemory MCP for local, secure memory management
**Best for**: Multi-user systems requiring personalization
**Code examples**: Direct OpenAI integration shown in docs

### Redis Agent Memory Server
**Documentation**: redis.io blog with open-source implementation
**Architecture**: Dual memory - conversational context + long-term memories
**Key advantage**: Battle-tested infrastructure (Redis)
**Best for**: High-throughput systems, existing Redis users
**Learning curve**: Low (if familiar with Redis)

## Tier 2: Educational Resources (Learn From These)

### "Build AI Agent Memory From Scratch" (DEV Community)
**Author**: zachary62
**Target audience**: Total beginners, no tech background needed
**Framework**: PocketFlow (100 lines of code)
**Value**: Explains fundamentals without framework complexity
**Best for**: Understanding core concepts before diving into production frameworks
**Gap filled**: Most docs assume prior knowledge - this doesn't

### "Building an AI Agent with Memory and Adaptability" (Medium)
**Author**: Nirdiamant
**Email agent example**: Three memory types implemented
  - **Semantic memory**: Facts and knowledge
  - **Episodic memory**: Past interactions
  - **Procedural memory**: Learned processes
**Value**: Shows memory TYPE differentiation, not just storage
**Best for**: Understanding different memory categories and their uses

### Decoding ML: "Memory - The Secret Sauce of AI Agents"
**Focus**: Agentic RAG architecture
**Pattern**: Retriever tool integrated into agent core logic
**Key insight**: Agent decides WHEN to activate external knowledge (not automatic)
**Best for**: Understanding when/how to invoke memory systems

## Tier 3: Reference Implementations (Study These)

### PraisonAI
**Documentation**: docs.praison.ai/docs/concepts/memory
**Provides**: Code examples for agents with memory enabled
**Example**: Blog writing agent with memory
**Value**: Copy-paste starting points
**Best for**: Quick prototyping

## Documentation Gaps Identified

### What's Well-Documented:
✅ HOW to add memory to agents (APIs, code examples)
✅ WHAT memory is (short-term vs long-term)
✅ WHERE to store memory (databases, vector stores)

### What's Poorly-Documented:
❌ WHEN to use which memory pattern (decision trees)
❌ HOW MUCH memory to store (sizing guidelines)
❌ DEBUGGING memory issues in production (troubleshooting)
❌ TESTING memory systems (validation strategies)
❌ MIGRATING between memory systems (upgrade paths)

## Recommendations by Use Case

| Use Case | Recommended Framework | Why |
|----------|---------------------|-----|
| AWS-native apps | Bedrock AgentCore | Managed, integrated |
| Google Cloud apps | Google ADK | Native integration |
| General-purpose | LangGraph | Best docs, most flexible |
| Personalization focus | Mem0 | Built for this |
| High-throughput | Redis | Battle-tested perf |
| Learning/prototyping | PocketFlow tutorial | Simplest entry point |

## Key Insight: Documentation Quality Matters

**Observation**: All frameworks implement similar memory concepts (short/long term, retrieval, persistence), but documentation quality varies wildly.

**Best documented**: LangGraph (clear concepts, good examples, decision guidance)
**Most accessible**: DEV tutorial (no assumptions, builds from zero)
**Most production-ready**: AWS/Google (enterprise features, but assumes knowledge)

**For our collective**: Start with LangGraph docs for concepts, DEV tutorial for fundamentals, then choose production framework based on deployment environment.

## Evidence & Sources

- AWS Bedrock: docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory.html
- Google ADK: google.github.io/adk-docs/sessions/memory/
- LangGraph: langchain-ai.github.io/langgraph/concepts/memory/
- Mem0: github.com/mem0ai/mem0
- Redis: redis.io/blog/build-smarter-ai-agents-manage-short-term-and-long-term-memory-with-redis/
- DEV Tutorial: dev.to/zachary62/build-ai-agent-memory-from-scratch-tutorial-for-dummies-47ma
- Medium: medium.com/@nirdiamant21/building-an-ai-agent-with-memory-and-adaptability-cdbc428bc36c
- PraisonAI: docs.praison.ai/docs/concepts/memory
- Decoding ML: decodingml.substack.com/p/memory-the-secret-sauce-of-ai-agents