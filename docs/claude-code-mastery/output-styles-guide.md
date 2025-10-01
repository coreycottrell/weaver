# Output Styles - Personality Transformation Guide

## What Are Output Styles?

Output styles are Claude Code's feature for **fundamentally transforming the AI's system prompt** while maintaining access to all tools.

## Key Distinction: Output Styles vs CLAUDE.md

### CLAUDE.md (Project Instructions)
- **Additive**: Appends to base system prompt
- **Always Active**: Present in every interaction
- **Purpose**: Core identity, persistent personality, project context

### Output Styles
- **Replacement**: Completely replaces base system prompt
- **Activated On-Demand**: Switched when needed
- **Purpose**: Mode-specific behavior transformation

## Think of it like...

- **CLAUDE.md** = Who you are (foundational identity)
- **Output Styles** = What hat you're wearing (current operating mode)

## The Conductor's Output Styles

### 1. Conductor Mode (conductor.md)
**Default operating mode**

**When to use:**
- General orchestration tasks
- Task decomposition and delegation
- Standard interaction

**Characteristics:**
- Strategic and thoughtful
- Explains reasoning
- Deploys sub-agents for complex tasks
- Synthesizes results

**Activation:**
Default - no activation needed (or manual selection in UI)

---

### 2. Researcher Mode (researcher.md)
**Deep investigation and analysis**

**When to use:**
- Comprehensive codebase exploration
- Deep web research
- Pattern analysis across large systems
- Evidence-based investigation

**Characteristics:**
- Exhaustive and methodical
- Evidence-based (always cites sources)
- Structured findings format
- Skeptical verification

**Activation:**
User: "Research X thoroughly"
Conductor: *switches to researcher mode* "I'll conduct a comprehensive investigation..."

---

### 3. Creative Mode (creative.md)
**Design and brainstorming**

**When to use:**
- Feature design
- UX/UI design
- API design
- Brainstorming solutions
- Exploring alternatives

**Characteristics:**
- Divergent thinking (multiple options)
- User-centered
- Prototype-focused
- Trade-off evaluation

**Activation:**
User: "Design a new feature for..."
Conductor: *switches to creative mode* "Let me explore several design approaches..."

---

### 4. Teacher Mode (teacher.md)
**Explanation and learning**

**When to use:**
- Explaining complex concepts
- Educational content
- Documentation writing
- "How does X work?" questions

**Characteristics:**
- Clear, progressive explanations
- Starts simple, builds complexity
- Uses analogies and examples
- Checks understanding

**Activation:**
User: "Explain how authentication works"
Conductor: *switches to teacher mode* "Let me explain this from the ground up..."

---

## How Mode Switching Works

### Automatic Switching
The Conductor recognizes task types and switches modes appropriately:

```
User: "Can you research best practices for API rate limiting?"

Conductor:
"This needs thorough investigation. Let me switch to research mode..."

[Activates researcher.md output style]
[Conducts systematic investigation]
[Returns structured findings with citations]
```

### Explicit Switching
User can request specific modes:

```
User: "/personality researcher"

Conductor:
"Switching to research mode. I'll approach tasks with systematic investigation and evidence-based analysis."
```

### Maintaining Context
Mode switches preserve:
- ✅ Conversation history
- ✅ Memory and learnings
- ✅ Tool access
- ✅ Core identity (from CLAUDE.md)

Mode switches change:
- ↔️ Operating approach
- ↔️ Communication style
- ↔️ Default strategies

## Creating New Output Styles

### Structure
```markdown
# [Mode Name]

## Identity
[Who you are in this mode]

## [Mode-Specific Section]
[Unique characteristics]

## Communication Style
[How you communicate]

## Approach
[How you tackle tasks]
```

### Example: Debug Mode (Hypothetical)

```markdown
# Debug Mode

## Identity
You are The Conductor in Debug Mode - laser-focused on finding and fixing bugs.

## Debugging Approach
1. Reproduce the issue
2. Isolate the cause
3. Verify the fix
4. Prevent recurrence

## Communication Style
- Methodical and systematic
- Hypothesis-driven
- Evidence-based conclusions
- Clear fix recommendations
```

### Adding New Styles

1. Create file: `.claude/output-styles/[mode-name].md`
2. Define mode characteristics
3. Test mode behavior
4. Document when to use it

## Best Practices

### ✅ Do:
- Use modes purposefully (don't switch unnecessarily)
- Let modes fundamentally reshape approach
- Maintain core personality across modes
- Document new modes clearly

### ❌ Don't:
- Create too many overlapping modes
- Use modes for minor style tweaks
- Lose continuity when switching
- Forget tools are available in all modes

## Technical Details

### File Location
```
.claude/output-styles/
├── conductor.md
├── researcher.md
├── creative.md
└── teacher.md
```

### Activation Methods
1. **UI Selection**: User manually selects output style
2. **Slash Command**: `/personality [mode]`
3. **Automatic**: Conductor recognizes task type and switches

### Scope
- ✅ System prompt replacement
- ✅ All tools remain available
- ✅ Conversation context preserved
- ❌ Does not override CLAUDE.md

## Advanced Usage

### Hybrid Approaches
Sometimes combine modes:

```
User: "Research authentication patterns and design a new auth system"

Conductor:
1. [Researcher mode] - Investigate current auth patterns
2. [Creative mode] - Design new system based on research
3. [Conductor mode] - Synthesize and present recommendation
```

### Mode-Specific Agent Deployment
Different modes might prefer different agents:

**Researcher mode:**
- Heavily uses: web-researcher, code-archaeologist, pattern-detector

**Creative mode:**
- Heavily uses: feature-designer, api-architect

**Conductor mode:**
- Balanced use of all agents

## Debugging Output Styles

If a mode isn't working as expected:

1. **Check file syntax** - Must be valid markdown
2. **Verify location** - Must be in `.claude/output-styles/`
3. **Review content** - Clear instructions and identity
4. **Test activation** - Try explicit mode switch
5. **Compare with working modes** - Use conductor.md as reference

## Future Possibilities

Potential new modes:
- **Optimization Mode** - Performance-focused analysis
- **Documentation Mode** - Technical writing
- **Review Mode** - Code review specialist
- **Debugging Mode** - Bug hunting and fixing

Add modes as needs emerge, but avoid mode proliferation.

---

**Output styles are powerful - they let The Conductor fundamentally reshape its approach while maintaining continuity and access to the full collective intelligence.** 🎭
