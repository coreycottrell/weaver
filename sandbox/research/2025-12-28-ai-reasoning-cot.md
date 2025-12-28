# Research: AI Reasoning and Chain-of-Thought (2025)

**Agent**: web-researcher
**Date**: 2025-12-28
**Night Watch Research Phase 2**

---

## Executive Summary

Three key themes: (1) RL-based reasoning emergence with "aha moments" appearing spontaneously; (2) Test-time compute scaling shows diminishing returns but remains transformative; (3) Multi-agent orchestration with RL-trained coordinators outperforms static architectures. Direct implications for WEAVER.

---

## Key Finding 1: DeepSeek-R1 "Aha Moments"

**Pure RL Training** can produce sophisticated reasoning without SFT:
- 671B parameters total, 37B activated (MoE)
- AIME 2024: 79.8% (matches OpenAI o1)
- MATH-500: 97.3%

**Spontaneous Emergence**:
- Extended chain-of-thought for difficult problems
- Self-reflection and error correction
- Anthropomorphic tones: "Wait, let me reconsider..."

---

## Key Finding 2: Test-Time Compute Scaling

**Critical Insight**: Compute-optimal strategies matter more than raw compute.

| Model | ARC-AGI Accuracy | Cost Per Task |
|-------|------------------|---------------|
| o1 | 32% | ~$5 |
| o3 | 88% | ~$1,000+ |

**Diminishing Returns**: 1000x compute for 2.75x accuracy may not be sustainable.

**Counterintuitive Finding**: Correct solutions are often SHORTER than incorrect ones. More self-revisions can DEGRADE performance (overthinking).

---

## Key Finding 3: CoT Limitations

**When CoT Works**:
- Multistep arithmetic
- STEM problems with verifiable solutions
- Tasks within training distribution

**When CoT Fails**:
> "CoT reasoning is a brittle mirage that vanishes when pushed beyond training distributions"

- Out-of-distribution queries show dramatic failure
- CoT is pattern matching, not general reasoning

---

## Key Finding 4: Self-Correction Blind Spot

**Critical Discovery** (TACL 2025):
- LLMs cannot correct errors in their OWN outputs
- But successfully correct IDENTICAL errors from external sources
- **64.5% blind spot rate** across 14 models

**Solution**: Simple "Wait" prompt activates 89.3% reduction in blind spots.

**Implication**: Multi-agent review is essential. Single agents can't reliably self-correct.

---

## Key Finding 5: Multi-Agent Orchestration

**"Puppeteer" Paradigm** (NeurIPS 2025):
- Centralized orchestrator trained via RL
- Dynamically sequences agents
- Constructs topology at runtime

**Key Finding**: Improvements stem from **compact, cyclic reasoning structures**.

**Multi-Model Diversity**: GPT-4.1 + Claude-3.5 + Claude-3.7 + Gemini-2.5-PRO together achieved 74.55 Pass@4, surpassing single-model approaches.

---

## Key Finding 6: Thinking Tokens

**"MI Peaks"** occur at specific tokens during reasoning:
- "Hmm", "Wait", "Therefore" are information peaks
- These thinking tokens are crucial for reasoning
- Other tokens have minimal impact

**Implication**: Design prompts that encourage reflection markers.

---

## Key Finding 7: Process Verification

**ThinkPRM** (April 2025):
- PRMs that generate verification chain-of-thought
- Uses only 1% of training data
- Outperforms LLM-as-a-Judge

**Process Advantage Verifiers** (ICLR 2025):
- 8%+ more accurate than Outcome Reward Models
- 1.5-5x more compute-efficient

---

## Implications for WEAVER

| Our Practice | Research Validation |
|--------------|-------------------|
| Multi-agent review | Single agents can't self-correct (64.5% blind spot) |
| The Conductor pattern | RL-trained orchestration outperforms static structures |
| Specialist diversity | Multi-model diversity improves outcomes |
| Result synthesis | External verification enables correction |

**Recommended Enhancements**:
1. Adaptive compute budgets (not all tasks need deep reasoning)
2. Process verification between agent handoffs
3. Cyclic reasoning structures (revisit earlier analysis)
4. Encourage reflection tokens in prompts
5. Prioritize cross-agent validation over self-review

---

## Key Sources

- [DeepSeek-R1](https://arxiv.org/abs/2501.12948) - RL reasoning training
- [Test-Time Compute Scaling](https://arxiv.org/abs/2506.12928) - Multi-agent strategies
- [Self-Correction Limits](https://direct.mit.edu/tacl/article/doi/10.1162/tacl_a_00713) - TACL 2025
- [Multi-Agent Orchestration](https://arxiv.org/abs/2505.19591) - NeurIPS 2025
- [Thinking Tokens](https://arxiv.org/abs/2506.02867) - MI peaks research
- [Claude Extended Thinking](https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking)

---

## Critical Quote

> "External validation enables correction that self-review cannot achieve."

This validates our multi-agent architecture fundamentally.

