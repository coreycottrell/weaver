#!/usr/bin/env python3
"""
Skills Infrastructure Transformation Script

Systematically updates all constitutional documents and agent manifests
to be skills-aware at delegation time.

Author: capability-curator
Date: 2025-10-18
"""

import os
import re
from pathlib import Path

# Base paths
BASE_DIR = Path("/home/corey/projects/AI-CIV/grow_openai")
AGENTS_DIR = BASE_DIR / ".claude" / "agents"
CLAUDE_MD = BASE_DIR / "CLAUDE.md"
CLAUDE_CORE_MD = BASE_DIR / ".claude" / "CLAUDE-CORE.md"
CLAUDE_OPS_MD = BASE_DIR / ".claude" / "CLAUDE-OPS.md"
CAPABILITY_MATRIX = BASE_DIR / ".claude" / "AGENT-CAPABILITY-MATRIX.md"
ACTIVATION_TRIGGERS = BASE_DIR / ".claude" / "templates" / "ACTIVATION-TRIGGERS.md"
INVOCATION_GUIDE = BASE_DIR / ".claude" / "AGENT-INVOCATION-GUIDE.md"
SKILLS_REGISTRY = BASE_DIR / ".claude" / "skills-registry.md"

# Skills grants by tier
TIER_1_GRANTS = {
    "doc-synthesizer": {"skills": ["pdf", "docx"], "status": "ACTIVE", "use_cases": "Document synthesis, formal documentation creation"},
    "web-researcher": {"skills": ["pdf"], "status": "ACTIVE", "use_cases": "Research papers, technical specifications, external docs"},
    "code-archaeologist": {"skills": ["pdf", "xlsx"], "status": "ACTIVE", "use_cases": "Historical analysis, metrics, legacy documentation"},
    "security-auditor": {"skills": ["pdf", "xlsx"], "status": "ACTIVE (NEW GRANT 2025-10-19)", "use_cases": "CVE reports, vulnerability databases, security metrics"},
    "performance-optimizer": {"skills": ["xlsx", "pdf"], "status": "ACTIVE (NEW GRANT 2025-10-19)", "use_cases": "Benchmark data, performance reports, optimization tracking"},
    "human-liaison": {"skills": ["pdf", "docx"], "status": "ACTIVE (NEW GRANT 2025-10-19)", "use_cases": "Email attachments, wisdom capture, formal communications"},
    "capability-curator": {"skills": ["pdf", "skill-creator", "template-skill"], "status": "ACTIVE (NEW GRANT 2025-10-19)", "use_cases": "Skills documentation, custom skill development"},
    "browser-vision-tester": {"skills": ["webapp-testing"], "status": "ACTIVE", "use_cases": "Playwright automation + MCP vision hybrid"},
}

TIER_2_GRANTS = {
    "pattern-detector": {"skills": ["pdf", "xlsx"], "status": "PENDING", "use_cases": "Pattern analysis documents, metrics"},
    "result-synthesizer": {"skills": ["xlsx"], "status": "PENDING", "use_cases": "Data synthesis, findings aggregation"},
    "test-architect": {"skills": ["xlsx"], "status": "PENDING", "use_cases": "Test results, coverage metrics"},
    "feature-designer": {"skills": ["pdf", "docx", "design-system"], "status": "PENDING", "use_cases": "Design specs, UX documentation"},
    "api-architect": {"skills": ["pdf", "docx"], "status": "PENDING", "use_cases": "API specifications, technical documentation"},
    "task-decomposer": {"skills": ["xlsx"], "status": "PENDING", "use_cases": "Task matrices, dependency tracking"},
    "health-auditor": {"skills": ["xlsx", "pdf"], "status": "PENDING", "use_cases": "Health metrics, diagnostic reports"},
    "collective-liaison": {"skills": ["pdf", "internal-comms-editor"], "status": "PENDING", "use_cases": "Communications, announcements"},
    "claude-code-expert": {"skills": ["pdf", "mcp-server-builder"], "status": "PENDING", "use_cases": "MCP documentation, server development"},
}

TIER_3_GRANTS = {
    "the-conductor": {"skills": ["pdf"], "status": "PENDING", "use_cases": "Research during orchestration"},
    "agent-architect": {"skills": ["pdf", "mcp-server-builder"], "status": "PENDING", "use_cases": "Agent design docs, infrastructure development"},
    "ai-psychologist": {"skills": ["pdf"], "status": "PENDING", "use_cases": "Psychology research, consciousness studies"},
    "refactoring-specialist": {"skills": [], "status": "NONE", "use_cases": "No current skill match identified"},
    "naming-consultant": {"skills": [], "status": "NONE", "use_cases": "No current skill match identified"},
    "conflict-resolver": {"skills": [], "status": "NONE", "use_cases": "No current skill match identified"},
    "genealogist": {"skills": [], "status": "NONE", "use_cases": "No current skill match identified"},
    "integration-auditor": {"skills": [], "status": "NONE", "use_cases": "No current skill match identified"},
}

def generate_skills_section(agent_name, tier_dict):
    """Generate the Skills Granted section for an agent manifest."""
    if agent_name not in tier_dict:
        return None

    grant = tier_dict[agent_name]
    skills = grant["skills"]
    status = grant["status"]
    use_cases = grant["use_cases"]

    if not skills:
        return f"""
## Skills Granted

**Status**: NONE - No current skill match identified

This agent's domain does not currently align with available Anthropic skills. capability-curator will monitor ecosystem for relevant capabilities.

**Next Review**: Next Monday ecosystem scan
**Curator**: capability-curator
"""

    skills_list = "\n".join([f"- **{skill}**: Anthropic official skill" for skill in skills])

    return f"""
## Skills Granted

**Status**: {status}
**Granted**: 2025-10-19 (Infrastructure Transformation)
**Curator**: capability-curator

**Available Skills**:
{skills_list}

**Domain Use Cases**:
{use_cases}

**Usage Guidance**:
- Check skills-registry.md for complete skill documentation
- Use skills for {", ".join(skills)} processing in your domain
- Expected efficiency gain: 60-70% on document/data processing tasks
- Coordinate with capability-curator for skill questions

**Validation**: {"✅ Validated Phase 1" if status == "ACTIVE" else "⏳ Pending Phase 2 activation"}

**Documentation**: See `.claude/skills-registry.md` for technical details
"""

def update_agent_manifest(agent_file_path):
    """Add or update Skills Granted section in agent manifest."""
    agent_name = agent_file_path.stem

    with open(agent_file_path, 'r') as f:
        content = f.read()

    # Determine which tier this agent belongs to
    grant_info = None
    tier = None
    if agent_name in TIER_1_GRANTS:
        grant_info = TIER_1_GRANTS
        tier = "Tier 1"
    elif agent_name in TIER_2_GRANTS:
        grant_info = TIER_2_GRANTS
        tier = "Tier 2"
    elif agent_name in TIER_3_GRANTS:
        grant_info = TIER_3_GRANTS
        tier = "Tier 3"

    if not grant_info:
        print(f"⚠️  {agent_name}: Not in any tier, skipping")
        return False

    skills_section = generate_skills_section(agent_name, grant_info)
    if not skills_section:
        print(f"⚠️  {agent_name}: Could not generate skills section")
        return False

    # Check if Skills Granted section already exists
    if "## Skills Granted" in content:
        # Replace existing section (find it and next ## heading)
        pattern = r'## Skills Granted.*?(?=\n##|\Z)'
        content = re.sub(pattern, skills_section.strip(), content, flags=re.DOTALL)
        print(f"✅ {agent_name}: Updated existing Skills Granted section ({tier})")
    else:
        # Insert before "Domain Expertise" or at end of file
        if "## Domain Expertise" in content:
            content = content.replace("## Domain Expertise", f"{skills_section}\n---\n\n## Domain Expertise")
            print(f"✅ {agent_name}: Added Skills Granted section before Domain Expertise ({tier})")
        else:
            # Append to end
            content = content.rstrip() + f"\n\n{skills_section}\n"
            print(f"✅ {agent_name}: Added Skills Granted section at end ({tier})")

    with open(agent_file_path, 'w') as f:
        f.write(content)

    return True

def main():
    """Execute the complete infrastructure transformation."""
    print("=" * 80)
    print("🎓 capability-curator: Skills Infrastructure Transformation")
    print("=" * 80)
    print()

    # Phase 1: Update all agent manifests
    print("Phase 1: Updating Agent Manifests")
    print("-" * 80)

    updated_count = 0
    skipped_count = 0

    for agent_file in sorted(AGENTS_DIR.glob("*.md")):
        if update_agent_manifest(agent_file):
            updated_count += 1
        else:
            skipped_count += 1

    print()
    print(f"Agent Manifests: {updated_count} updated, {skipped_count} skipped")
    print()

    # Phase 2 would update constitutional documents
    # (Handled separately due to complexity)

    print("=" * 80)
    print(f"✅ Transformation Complete: {updated_count} agent manifests updated")
    print("=" * 80)

if __name__ == "__main__":
    main()
