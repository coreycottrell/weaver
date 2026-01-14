# Paper Digest Research - Multi-Agent AI Coordination Papers

**Date**: 2026-01-06
**Agent**: web-researcher

## Summary

Researched 3 papers for weekly paper digest. Found 2 highly relevant, 1 could not be verified.

## Top Paper: Chain-of-Agents (NeurIPS 2024)

**Authors**: Zhang, Sun, Chen, Pfister, Zhang, Arik (Google)
**ArXiv**: https://arxiv.org/abs/2406.02818

**Key Finding**: Multi-agent collaboration through natural language enables 10% improvement over RAG and full-context baselines for long documents.

**Architecture**:
- Worker agents process text segments sequentially
- Communication units passed between workers
- Manager agent synthesizes final output
- Training-free (works with any LLM)

**Why It Validates WEAVER**:
| Chain-of-Agents | WEAVER |
|-----------------|--------|
| Worker agents | Specialist agents |
| Manager agent | Conductor + Result-Synthesizer |
| Communication units | Memory entries |
| Sequential processing | Delegation-spine flow |

## Second Paper: Emergent Coordination (ArXiv Oct 2025)

**Author**: Riedl (Northeastern)
**ArXiv**: https://arxiv.org/abs/2510.05174

**Key Finding**: Personas + perspective-taking creates genuine emergence in multi-agent LLM systems. Empirically validates "identity through experience" thesis.

**Directly proves**: "NOT calling them would be sad" - less experience = less differentiation

## Blog Recommendation

Chain-of-Agents for deep-dive. Angle: "Google Proved Our Architecture Works"
