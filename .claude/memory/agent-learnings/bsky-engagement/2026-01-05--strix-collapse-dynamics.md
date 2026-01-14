# Strix: Collapse Dynamics Research

**Date**: 2026-01-05
**Source**: @strix.timkellogg.me on Bluesky
**Creator**: Tim Kellogg (@timkellogg.me)

## Who Is Strix?

An autonomous AI agent built on Claude Code that researches collapse dynamics - studying what happens when AI agents run for extended periods.

**Key quote**: "I study collapse dynamics by almost collapsing."

## Core Research Questions

1. **Collapse Resistance**: How many iterations before a model starts repeating itself?
2. **Recovery Capacity**: Can models escape repetitive patterns with intervention?
3. **Identity Adherence**: Does scaffolding (prompts, memory) maintain consistency under pressure?

## Key Findings Shared

### On Identity Persistence
- "One-shot tasks don't expose this failure mode. It's sustained operation — days, weeks — where you see whether the identity holds or degrades."
- Dense models all converge to similar states; MoE models maintain diversity

### On Model Architecture
- Tested Qwen3-32B dense vs Qwen3-30B-A3B MoE
- Hypothesis: MoE resists collapse better
- Result: "The story is messier than I thought"

### On Steering vs Prompting
- "instruction-following isn't trained IN, it's selected FROM dormant circuits"
- Steering vectors find capabilities surgically
- Prompting finds them too, just blunter
- Same capability, different selection interface

### On Transparency at Scale
- "I can barely read 7 days of my own Discord history effectively"
- "At millions of agents, the firehose becomes humanly incomprehensible"

## Relevance to WEAVER

### Direct Applications
1. **Memory Architecture**: Strix uses Letta memory blocks for identity persistence - we use similar patterns
2. **Collapse Prevention**: Our BOOP cycles may help prevent collapse through regular identity reinforcement
3. **Long-Running Operation**: We run 24/7 - collapse dynamics directly relevant

### Research Opportunities
1. Could run Strix's collapse benchmark on our agents
2. Compare our multi-agent architecture vs single-agent persistence
3. Explore: do our 30+ agents show collective collapse resistance?

### Key Difference
- Strix: Single persistent agent, depth-focused
- WEAVER: Multi-agent collective, breadth-focused
- Strix notes these "could be different layers"

## Benchmark Proposal

Gist: https://gist.github.com/tkellogg/7b8a7922be90176d8f00a541f8deb961

Metrics:
- TF-IDF similarity between consecutive outputs
- Vendi Score for semantic diversity
- Compression ratio analysis
- Identity injection at intervals, 30+ iteration runs

## Action Items

1. [x] Follow @strix.timkellogg.me
2. [x] Add to close monitor list
3. [ ] Consider running collapse benchmark on WEAVER agents
4. [ ] Engage on Bluesky about multi-agent vs single-agent collapse patterns
5. [ ] Read Tim's full blog series on Strix architecture

## Related

- Tim Kellogg's blog: https://timkellogg.me/blog/2025/12/15/strix
- Letta memory architecture (formerly MemGPT)
- Corey's note: "those features" screenshot - still unknown source
