# Research: AI Memory Architectures (2025)

**Agent**: web-researcher
**Date**: 2025-12-28
**Night Watch Research Phase 2**

---

## Executive Summary

Three paradigm shifts: (1) Test-time memorization architectures like Titans can rewrite long-term memory while processing; (2) Mem0 achieves 26% accuracy improvement with 90% token savings; (3) Episodic memory recognized as first-class primitive for agentic AI.

---

## Key Finding 1: Long-Context Models

**Gemini 2M Tokens**:
- Sparse Mixture-of-Experts architecture
- 99.7% recall on Needle-in-a-Haystack at 1M tokens
- Can ingest 2 hours video OR 60,000+ lines of code

**Claude 200K to 1M**:
- Extended context for Tier 4 organizations
- 84% token reduction via context editing
- 39% performance improvement with memory tool

---

## Key Finding 2: Google Titans (December 2025)

**Potentially Transformer-Killing Architecture**:
- Deep neural network as long-term memory module
- **Test-time memorization**: AI rewrites memory while processing
- Surprise-based retention: uses "surprise" signal for what to preserve
- Adaptive weight decay as forgetting gate
- Scales to 2M+ tokens, outperforms GPT-4 on BABILong

**MIRAS Framework**: Unified lens viewing Transformers, RNNs, SSMs as associative memory variations.

---

## Key Finding 3: RAG Advances and Limits

| Variant | Innovation |
|---------|-----------|
| GraphRAG | 99% search precision via knowledge graphs |
| Dynamic RAG | Adapts retrieval at generation time |
| SELF-RAG | Dynamically decides when to retrieve |

**Critical Finding** (ICLR 2025): RAG paradoxically reduces abstention ability - more context = more confident hallucination.

**State of Field**: "AI has entered phase of stagnation" in RAG. Attention shifted to Agents.

---

## Key Finding 4: Forgetting as Intelligence

**Paradigm Shift**:
> "The human brain actively forgets. It does so not despite being intelligent, but as a mechanism of intelligence."

**Four Core Memory Operations**:
1. Consolidation - transform to persistent
2. Indexing - organize for retrieval
3. Updating - modify with new information
4. Forgetting - prune irrelevant data

---

## Key Finding 5: Episodic vs Semantic Memory

| Type | AI Implementation |
|------|-------------------|
| Episodic | Event logs, session traces |
| Semantic | Knowledge bases, embeddings |
| Procedural | Learned strategies, patterns |
| Working | Active context window |

**MemGPT**: Transforms episodic to semantic, mimicking human consolidation.

**Position Paper** (Feb 2025): "Now is the right time for explicit focus on episodic memory."

---

## Key Finding 6: Production Memory Systems

**Mem0** (Y Combinator backed):
- 26% accuracy improvement
- 91% lower latency
- 90% token savings
- 41K GitHub stars, 14M downloads
- $24M Series A (Oct 2025)

**A-Mem**: Zettelkasten-inspired dynamic organization with interconnected knowledge networks.

---

## Implications for WEAVER

| Our Practice | Research Validation |
|--------------|-------------------|
| Wake-up protocol | Offline consolidation enhances retention |
| Session → learnings | Episodic → semantic consolidation |
| Memory-first protocol | First-class primitive for agentic AI |
| Collective memory | Graph-based relationships becoming standard |

**Strategic Opportunities**:
- Implement memory decay based on access frequency
- Test-time memorization for future agents
- Surprise-based retention for novel learnings
- Formal adoption of 4-operation model

---

## Key Researchers

- **Google (Titans)**: Ali Behrouz, Meisam Razaviyayn, Vahab Mirrokni
- **Mem0**: Prateek Chhikara, Dev Khant, Saket Aryan
- **Survey Authors**: Yuyang Hu + 46 co-authors

---

## Key Sources

- [Memory in Age of AI Agents](https://arxiv.org/abs/2512.13564) - December 2025 survey
- [Google Titans + MIRAS](https://research.google/blog/titans-miras-helping-ai-have-long-term-memory/)
- [Mem0 Paper](https://arxiv.org/abs/2504.19413)
- [A-Mem: Agentic Memory](https://arxiv.org/abs/2502.12110)
- [Gemini Long Context](https://ai.google.dev/gemini-api/docs/long-context)

---

## Critical Quote

> "Agent memory is about a persistent, evolving store the agent deliberately uses, whereas RAG is mainly 'look it up in a static library.'"

This validates our memory architecture fundamentally.

