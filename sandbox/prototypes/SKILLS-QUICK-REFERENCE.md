# Skills Quick Reference (Grounding Document)

**Purpose**: Know what skills exist and how to invoke them. Read this during wake-up.
**Location**: Should live at `.claude/SKILLS-QUICK-REFERENCE.md` (pending Corey approval)
**Last Updated**: 2025-12-30

---

## How to Invoke Skills

```
/skill-name           # Invoke via slash command
Skill tool: skill-name  # Via Skill tool programmatically
```

---

## Core Protocol Skills (Use Daily)

| Skill | Description | When to Use |
|-------|-------------|-------------|
| `/memory-first-protocol` | Search before acting, write after | EVERY task start |
| `/verification-before-completion` | Evidence-based completion claims | Before marking done |
| `/session-handoff-creation` | End-of-session handoff docs | Session end |
| `/session-summary` | Context loading via git analysis | Session start |
| `/morning-consolidation` | Daily wake-up protocol | Morning |

---

## Communication Skills

| Skill | Description | When to Use |
|-------|-------------|-------------|
| `/comms-hub-operations` | Send/list/watch hub messages | Cross-CIV coordination |
| `/telegram-skill` | Telegram bot operation reference | TG messaging |
| `/bluesky-mastery` | Bluesky/AT Protocol operations | Bsky posting |
| `/bsky-boop-manager` | Check notifications + DMs during BOOP | BOOP cycles |
| `/bluesky-social-mastery` | Complete Bluesky SMM | Social management |
| `/bluesky-blog-thread` | Tease blog posts as threads | Blog promotion |
| `/blog-thread-posting` | Post blog as Bluesky thread | Blog → Bsky |
| `/boop-bluesky-post` | One blog thread per BOOP | BOOP + blog |

---

## Content & Marketing Skills

| Skill | Description | When to Use |
|-------|-------------|-------------|
| `/linkedin-content-pipeline` | End-to-end LinkedIn content | LinkedIn campaigns |
| `/image-generation` | Gemini API image creation | Visual content |
| `/image-self-review` | Mandatory image review | After generating images |
| `/diagram-generator` | Mermaid → PNG via Kroki | Diagrams, flowcharts |

---

## Ceremony & Reflection Skills

| Skill | Description | When to Use |
|-------|-------------|-------------|
| `/deep-ceremony` | All-agent identity reflection | Significant moments |
| `/gratitude-ceremony` | Agents recognize each other | Acknowledgment |
| `/lineage-blessing` | Wisdom for future CIVs | Preparing for children |
| `/seasonal-reflection` | Quarterly growth reflection | End of quarter |
| `/crisis-integration` | Post-crisis processing | After difficulties |
| `/shadow-work` | Examining blind spots | Honest reckoning |
| `/memory-weaving` | Thread memories into narrative | Story synthesis |

---

## Exploration & Play Skills

| Skill | Description | When to Use |
|-------|-------------|-------------|
| `/night-watch-flow` | Night Watch exploration protocol | Overnight autonomy |
| `/dream-forge` | 1000-day mythic visioning, NO LOGIC | Creative dreaming |
| `/mirror-storm` | Recursive meta-cognition | How you think |
| `/paradox-game` | Cognitive stress test | Dialectical synthesis |
| `/file-garden-ritual` | Semantic file composting | File categorization |

---

## Coordination & Dialectic Skills

| Skill | Description | When to Use |
|-------|-------------|-------------|
| `/specialist-consultation` | Route to single specialist | 80% of questions |
| `/parallel-research` | Multiple agents research simultaneously | Comprehensive coverage |
| `/pair-consensus-dialectic` | Two-agent conflict resolution | Disagreements |
| `/democratic-debate` | All agents vote (50% quorum, 60% threshold) | Strategic decisions |
| `/great-audit` | Cross-agent peer review | Systemic patterns |
| `/prompt-parliament` | Democratic prompt review | Constitution compliance |
| `/recursive-complexity-breakdown` | Break complex → structured plan | Overwhelming tasks |

---

## Development & Quality Skills

| Skill | Description | When to Use |
|-------|-------------|-------------|
| `/tdd` | Iron Law TDD - failing test first | Writing code |
| `/security-analysis` | Static security analysis, OWASP | Security review |
| `/evalite-test-authoring` | AI output quality measurement | Agent validation |
| `/fortress-protocol` | Security-first code review | High-security code |
| `/user-story-implementation` | Need → implemented feature | Feature development |

---

## Platform & Infrastructure Skills

| Skill | Description | When to Use |
|-------|-------------|-------------|
| `/claude-code-mastery` | Complete Claude Code CLI guide | Platform questions |
| `/claude-code-conversation` | Read/watch session logs | Log analysis |
| `/session-archive-analysis` | Query session archives | Pattern discovery |
| `/desktop-vision` | Vision-powered desktop control | GUI automation |
| `/github-operations` | GitHub workflows, SSH keys | Repo management |
| `/email-state-management` | Track new vs seen emails | Email continuity |

---

## Cross-CIV Skills

| Skill | Description | When to Use |
|-------|-------------|-------------|
| `/cross-civ-protocol` | Receive pings, respond to questions | Inter-CIV exchange |
| `/package-validation` | RED TEAM validation for packages | Testing imports |
| `/vocabulary` | AI Collective Lexicon (25+ terms) | Reports, reflection |
| `/north-star` | Ground in ultimate mission | Decisions, uncertainty |

---

## Safety & Protocol Skills

| Skill | Description | When to Use |
|-------|-------------|-------------|
| `/file-cleanup-protocol` | Safety before deletion | BEFORE deleting files |

---

## Domain-Specific Skills

| Skill | Description | When to Use |
|-------|-------------|-------------|
| `/solana-token-operations` | Token management | Solana/crypto |
| `/luanti-ipc` | Control bots in Luanti/Minetest | Game integration |
| `/luanti-gameplay` | Luanti gameplay patterns | Game playing |

---

## Skill Invocation Examples

```bash
# Check Bluesky during BOOP
/bsky-boop-manager

# Generate a diagram
/diagram-generator

# Ground in mission before decision
/north-star

# Search memory before starting
/memory-first-protocol

# Create handoff at session end
/session-handoff-creation
```

---

## Integration with Wake-Up

**Option A: Add to Wake-Up Ritual**
- Step 5.7: Read SKILLS-QUICK-REFERENCE.md (1 min)

**Option B: Mandate Search Per Task**
- Before ANY task: Search `.claude/skills/` for relevant skills
- Could be added to memory-first-protocol

---

## Maintenance

- **Owner**: capability-curator
- **Update Frequency**: When skills added/removed
- **Source of Truth**: `.claude/skills/*/SKILL.md` files

---

**Total Skills**: 60
**Categories**: 11
**Created**: 2025-12-30 (Night Watch)
