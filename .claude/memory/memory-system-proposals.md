# Agent Memory System Proposals
**Date**: 2025-10-02
**Task**: Design elegant memory system for agents to build and search their own memories

---

## Executive Summary

4 agent teams proposed memory system designs. All converged on key principles:
- ✅ **Topic-based organization** over chronological logs
- ✅ **Explicit triggers** for writing (not automatic)
- ✅ **Two-phase search** (fast discovery → deep dive)
- ✅ **Structured metadata + free-form insights**
- ✅ **Cross-agent learning** through tags/connections

**Key Differences**:
- Team 1: Simple topic files, zero infrastructure
- Team 2: Self-documenting filenames with dates, optimized for speed
- Team 3: Security-first with validation, append-only logs
- Team 4: Insight capsules focused on quality, collective intelligence

---

## Team 1: Architecture Team
**Agents**: Code Archaeologist, Pattern Detector, API Architect, Doc Synthesizer

### Core Philosophy
"Zero infrastructure, topic-based organization, explicit triggers"

### Key Design Decisions

**File Structure**:
```
agent-learnings/[agent-name]/
├── authentication-patterns.md
├── api-design-principles.md
└── performance-bottlenecks.md
```

**Memory Format**:
- Topic-based filenames (not dated)
- Lightweight markdown template
- Pattern + Examples + Recommendations structure

**Search Strategy**:
1. Grep for keywords → find relevant files
2. Read matching files → get context
3. Apply learnings to current task

**Memory Write Trigger**:
- Explicit instruction in agent identity file
- "After completing your analysis, write key learnings to..."

**Strengths**:
- ✅ Simplest approach - just markdown files
- ✅ Zero infrastructure needed
- ✅ Topic-based is more useful than chronological
- ✅ Works within existing Claude Code tools

**Weaknesses**:
- ⚠️ No timestamps (hard to know if stale)
- ⚠️ No search index (Grep all files every time)
- ⚠️ Manual cross-referencing only

---

## Team 2: UX Team
**Agents**: Feature Designer, Naming Consultant, Refactoring Specialist, Performance Optimizer

### Core Philosophy
"Self-documenting filenames, speed-optimized search, minimal cognitive load"

### Key Design Decisions

**File Structure**:
```
agent-learnings/[agent-name]/
├── 2025-10-02--authentication-patterns.md
├── 2025-10-03--repository-pattern-detection.md
└── README.md
```

**Filename Format**: `{YYYY-MM-DD}--{topic-slug}.md`

**Memory Format**:
```markdown
# {Topic Title}

**Date**: {YYYY-MM-DD}
**Context**: {What prompted this}
**Tags**: `{tag1}`, `{tag2}`, `{tag3}`

## Key Findings
## Patterns Identified
## Examples
## Recommendations
## Related
```

**Search Strategy**:
1. **Glob** for topic patterns in filename (fast)
2. **Grep** for content search (targeted)
3. **Read** full file once found

**Memory Write Trigger**:
- Complete significant investigation
- Identify reusable pattern
- Encounter edge case/gotcha
- Solve complex problem

**Strengths**:
- ✅ Self-documenting filenames (no separate index needed)
- ✅ Chronological sorting automatic
- ✅ Glob + Grep two-phase search is very fast
- ✅ Tags enable categorical search
- ✅ Minimal maintenance overhead

**Weaknesses**:
- ⚠️ Filename length can get unwieldy
- ⚠️ Topic updates require new files (vs. updating existing)

---

## Team 3: Security & Testing Team
**Agents**: Security Auditor, Test Architect, Task Decomposer

### Core Philosophy
"Defense in depth, validation-first, testable and safe"

### Key Design Decisions

**File Structure**:
```
agent-learnings/[agent-name]/
├── README.md
├── learnings-index.json (gitignored)
├── 2025-10-02-api-security-patterns.md
└── 2025-10-03-jwt-validation-issues.md
```

**Index Format** (learnings-index.json):
```json
{
  "version": "1.0",
  "agent": "security-auditor",
  "learnings": [
    {
      "id": "2025-10-02-api-security-patterns",
      "file": "2025-10-02-api-security-patterns.md",
      "title": "API Security Patterns",
      "tags": ["authentication", "api-security", "jwt"],
      "confidence": "high"
    }
  ]
}
```

**Memory Format**:
- Standard sections (Context, Learnings, Checklist)
- Confidence level (High/Medium/Low)
- Security-focused metadata
- Validation markers

**Search Strategy**:
1. Read index.json → get candidate files
2. Grep within candidates → find specific patterns
3. Validate findings before use

**Memory Write Trigger**:
- End of significant task + strict conditions
- Novel pattern discovered
- Error/failure resolution
- Manual instruction only

**Security Considerations**:
- ✅ Index is gitignored (may contain project-specific data)
- ✅ Pre-commit hooks scan for secrets
- ✅ Never execute code from memory
- ✅ Validate all paths and content
- ✅ Append-only logging pattern

**Testing Strategy**:
- Memory write validation
- Search effectiveness tests
- Pollution prevention tests
- Security bypass attempts
- Cross-agent isolation tests

**Strengths**:
- ✅ Most secure design
- ✅ Index enables fast search
- ✅ Testable and validated
- ✅ Prevents sensitive data leaks
- ✅ Clear failure modes and mitigations

**Weaknesses**:
- ⚠️ More complex (index + validation)
- ⚠️ Index can become out of sync
- ⚠️ Requires discipline to maintain

---

## Team 4: Intelligence & Synthesis Team
**Agents**: Result Synthesizer, Conflict Resolver, Web Researcher

### Core Philosophy
"Insight-oriented quality over quantity, collective intelligence through connections"

### Key Design Decisions

**File Structure**:
```
agent-learnings/[agent-name]/
├── insights/
│   ├── 2025-10-02-pattern-rest-authentication.md
│   ├── 2025-10-02-technique-n-plus-one-detection.md
│   └── 2025-10-02-contradiction-security-performance.md
├── index.md (tag taxonomy)
└── connections.md (cross-references to other agents)
```

**Memory Format** (Insight Capsules):
```markdown
# Insight: [Descriptive Title]
**Agent**: [agent-name]
**Date**: YYYY-MM-DD
**Tags**: #pattern #contradiction #technique
**Confidence**: High/Medium/Low
**Triggered by**: [Task context]

## The Insight
[2-3 sentence summary]

## Context & Evidence
[What led to discovery]

## Why This Matters
[Implications for future work]

## Connections
- Related to: [Links to other insights, even from other agents]
- Contradicts: [Conflicts with previous learnings]
- Builds on: [Previous insights this extends]

## Application Pattern
[Concrete template for reusing]
```

**Search Strategy**:
1. Check agent's index.md for relevant tags
2. Grep for patterns across insights
3. Follow connections to related insights (cross-agent)

**Cross-Agent Learning**:
- Shared tag taxonomy (#authentication, #security, etc.)
- Connection graphs link related insights
- Global grep searches find insights from any agent
- Result synthesizer creates collective patterns in project-knowledge/

**Memory Write Trigger**:
- Detect a pattern (3+ occurrences)
- Resolve a contradiction
- Discover reusable technique
- Hit a dead end (negative findings)
- Make unexpected connection
- Synthesize complex findings

**Strengths**:
- ✅ Highest quality insights (strict threshold)
- ✅ Cross-agent learning via connections
- ✅ Insight-oriented vs. task-log oriented
- ✅ Shared tags enable collective intelligence
- ✅ Prevents memory bloat

**Weaknesses**:
- ⚠️ Requires discipline to maintain connections
- ⚠️ Manual connection graph updates
- ⚠️ More complex structure

---

## Convergent Findings (All Teams Agreed)

### 1. Topic-Based > Chronological
All teams rejected pure chronological logging in favor of topic/domain organization

### 2. Explicit > Automatic Triggers
All teams require explicit decision to write memory, not automated detection

### 3. Two-Phase Search
All teams use fast discovery (Glob/Index) → deep dive (Read/Grep)

### 4. Structured Metadata + Free-Form Content
All teams use standard fields (date, tags, context) + flexible insight body

### 5. Leverage Existing Tools
All teams use Read, Grep, Glob - no custom infrastructure

### 6. Memory Quality > Quantity
All teams emphasize writing only significant learnings

---

## Comparison Matrix

| Aspect | Team 1 | Team 2 | Team 3 | Team 4 |
|--------|--------|--------|--------|--------|
| **Filename** | topic-slug.md | YYYY-MM-DD--topic.md | YYYY-MM-DD-topic.md | YYYY-MM-DD-type-topic.md |
| **Index** | None | None (filename is index) | JSON file (gitignored) | index.md + connections.md |
| **Security** | Basic | Medium | High (validation) | Medium (insight quality) |
| **Cross-Agent** | Manual only | Tags in frontmatter | Isolation enforced | Connection graphs |
| **Complexity** | Lowest | Low | Medium-High | Medium |
| **Search Speed** | Medium (Grep all) | Fast (Glob + Grep) | Fastest (Index + Grep) | Medium (Index + Grep + Traverse) |
| **Maintenance** | Minimal | Minimal | Medium (index sync) | Medium (connections) |
| **Best For** | MVP/simplicity | Speed + usability | Security-critical | Collective intelligence |

---

## Recommended Hybrid Approach

Combining best elements from all 4 proposals:

### File Structure (from Team 2 + Team 4)
```
agent-learnings/[agent-name]/
├── README.md                           # Agent's knowledge summary
├── insights/
│   ├── 2025-10-02--pattern-jwt-auth.md
│   ├── 2025-10-03--technique-sql-injection-detection.md
│   └── 2025-10-05--contradiction-performance-security.md
└── index.md                            # Tag taxonomy + connections
```

### Filename Format (Team 2)
`{YYYY-MM-DD}--{type}-{topic-slug}.md`

**Types**: `pattern`, `technique`, `contradiction`, `gotcha`, `synthesis`

### Memory Template (Team 4 + Team 3)
```markdown
# {Topic Title}

**Date**: YYYY-MM-DD
**Agent**: [agent-name]
**Type**: [pattern/technique/contradiction/gotcha/synthesis]
**Tags**: #tag1 #tag2 #tag3
**Confidence**: High/Medium/Low
**Context**: [What prompted this investigation]

## The Insight
[2-3 sentence summary - what was discovered]

## Evidence & Examples
[Code references, file paths, concrete examples]

## Why This Matters
[When/how to apply this learning]

## Connections
- Related: [Links to other memory files, even from other agents]
- See also: [External docs, resources]

## Application Checklist
[Concrete steps to reuse this insight]
```

### Search Protocol (Team 2 + Team 3)
```bash
# Phase 1: Fast discovery (Glob)
glob pattern="agent-learnings/[agent-name]/insights/*--pattern-*auth*.md"

# Phase 2: Content search (Grep)
grep pattern="#authentication"
     path=".claude/memory/agent-learnings/[agent-name]/insights/"
     output_mode="files_with_matches"

# Phase 3: Deep read (Read)
read file_path="[discovered-file].md"

# Phase 4: Follow connections
# Read referenced files from "Connections" section
```

### Write Triggers (Team 4 + Team 1)
Write memory when:
- ✅ Pattern detected (3+ occurrences)
- ✅ Contradiction resolved
- ✅ Reusable technique discovered
- ✅ Complex problem solved
- ✅ Dead end hit (prevent redundant work)

Don't write:
- ❌ Routine tasks with no new insights
- ❌ Findings already in memory
- ❌ Trivial or obvious observations

### Security (Team 3)
- Pre-commit hooks scan for secrets
- Never execute code from memory files
- Validate all paths before use
- Clear git

ignore for sensitive files

---

## Implementation Roadmap

### Phase 1: MVP (Week 1)
- [ ] Create memory template in README.md
- [ ] Update 2-3 pilot agents (security-auditor, web-researcher, code-archaeologist)
- [ ] Add memory search protocol to agent identity files
- [ ] Add memory write trigger instructions

### Phase 2: Validation (Week 2)
- [ ] Test with 5 real tasks per pilot agent
- [ ] Validate no sensitive data leaked
- [ ] Confirm search is effective
- [ ] Measure memory quality

### Phase 3: Rollout (Week 3)
- [ ] Update all 14 agents with refined approach
- [ ] Create shared tag taxonomy
- [ ] Set up cross-agent connection patterns
- [ ] Add pre-commit hooks for security

### Phase 4: Evolution (Ongoing)
- [ ] Agents build memories naturally
- [ ] Result synthesizer creates project-knowledge patterns
- [ ] Memory quality improves over time
- [ ] Collective intelligence compounds

---

## Next Steps

1. **Choose approach**: Recommend hybrid (combines best of all 4)
2. **Pilot agents**: Start with security-auditor, web-researcher, code-archaeologist
3. **Test cycle**: 5 real tasks each, validate quality and security
4. **Refine**: Update based on pilot learnings
5. **Roll out**: Deploy to all 14 agents

---

**All 4 teams delivered excellent, thoughtful proposals. The convergence on key principles (topic-based, explicit triggers, two-phase search) gives us high confidence in the hybrid approach.** 🧠✨
