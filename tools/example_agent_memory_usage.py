#!/usr/bin/env python3
"""
Example: How an Agent Uses the Memory System

This demonstrates a typical workflow for an agent using the memory system:
1. Search for existing knowledge before starting task
2. Execute task and identify reusable patterns
3. Write high-quality memory for future use
4. Leverage memory in subsequent similar tasks

Author: The Conductor
Version: 1.0.0
"""

from memory_core import MemoryStore, MemoryEntry
from memory_search import QueryRouter, MemoryIndexer
from memory_quality import MemoryQuality, MemoryTriggerDetector
from memory_security import MemorySecurityValidator
from datetime import datetime


class SecurityAuditorAgent:
    """Example agent that uses memory system effectively."""

    def __init__(self):
        """Initialize agent with memory system access."""
        self.agent_name = "security-auditor"
        self.store = MemoryStore()
        self.router = QueryRouter()
        self.quality = MemoryQuality()
        self.validator = MemorySecurityValidator()
        self.trigger = MemoryTriggerDetector()

        print(f"🤖 {self.agent_name} initialized with memory system")

    def execute_task(self, task_description: str):
        """Execute a security audit task using memory system.

        Args:
            task_description: Task to execute
        """
        print(f"\n{'='*60}")
        print(f"📋 Task: {task_description}")
        print(f"{'='*60}")

        # STEP 1: Search existing memories
        print("\n1️⃣  Searching existing knowledge...")
        self._search_relevant_memories(task_description)

        # STEP 2: Execute task (simulated)
        print("\n2️⃣  Executing audit...")
        findings = self._perform_audit()

        # STEP 3: Check if findings warrant memory write
        print("\n3️⃣  Evaluating findings...")
        should_write, reason = self._should_write_memory(findings)

        if should_write:
            print(f"   ✅ {reason}")
            self._write_memory(findings)
        else:
            print(f"   ⏭️  {reason}")

        print(f"\n{'='*60}")
        print("✅ Task complete")
        print(f"{'='*60}")

    def _search_relevant_memories(self, query: str):
        """Search for relevant existing memories.

        Args:
            query: Search query
        """
        result = self.router.search(query, agent=self.agent_name)

        if result['results']:
            print(f"   📚 Found {len(result['results'])} relevant memories:")
            for filepath in result['results'][:3]:
                entry = self.store.read_entry(filepath)
                print(f"      - {entry.topic} ({entry.type}, quality: {entry.quality_score}/33)")
                print(f"        Tags: {', '.join(entry.tags)}")

            print(f"\n   💡 Applying insights from existing memories...")
        else:
            print(f"   📭 No existing memories found - pioneering new territory")

    def _perform_audit(self) -> dict:
        """Perform security audit (simulated).

        Returns:
            Dict with audit findings
        """
        # Simulated audit that discovers a pattern
        findings = {
            'pattern_name': 'CORS Misconfiguration Pattern',
            'occurrences': 7,  # Found in 7 endpoints
            'severity': 'MEDIUM',
            'time_to_find': 1800,  # 30 minutes
            'time_to_fix_per_instance': 300,  # 5 minutes
            'affected_systems': ['api-gateway', 'auth-service', 'user-service'],
            'description': '''
# CORS Misconfiguration Pattern

**Context**: Security audit of REST API endpoints across 3 microservices.

## The Pattern

Common CORS misconfiguration that allows any origin in development mode but
should be restricted in production:

```javascript
// VULNERABLE - allows any origin
app.use(cors({
    origin: '*',  // ← PROBLEM
    credentials: true
}));
```

**Correct Implementation**:

```javascript
// SECURE - whitelist specific origins
const allowedOrigins = [
    'https://app.example.com',
    'https://admin.example.com'
];

app.use(cors({
    origin: (origin, callback) => {
        if (!origin || allowedOrigins.includes(origin)) {
            callback(null, true);
        } else {
            callback(new Error('Not allowed by CORS'));
        }
    },
    credentials: true
}));
```

## Evidence

Found in 7 out of 15 audited endpoints (47%):

1. `/api/auth/login` - api-gateway
2. `/api/auth/logout` - api-gateway
3. `/api/users/*` - user-service (3 endpoints)
4. `/api/admin/*` - auth-service (2 endpoints)

All allowed `origin: '*'` with `credentials: true` which is a security risk.

## Impact

- **Severity**: MEDIUM (can lead to CSRF attacks)
- **Exploitation**: Requires attacker to control user's browser
- **Time to fix**: 5 minutes per endpoint
- **Total time saved**: ~2.5 hours if documented for other audits

## Application Checklist

When reviewing CORS configuration:

- [ ] Check if `origin: '*'` is used
- [ ] If credentials enabled, origin MUST be restricted
- [ ] Use whitelist of allowed origins
- [ ] Different configs for dev/staging/prod
- [ ] Test with unauthorized origin (should reject)
- [ ] Document allowed origins in config

## Related Security Issues

- CSRF token validation (complementary protection)
- Cookie SameSite attribute (alternative approach)
- Content Security Policy (defense in depth)
'''
        }

        print(f"   🔍 Pattern discovered: {findings['pattern_name']}")
        print(f"   📊 Occurrences: {findings['occurrences']}")
        print(f"   ⚠️  Severity: {findings['severity']}")

        return findings

    def _should_write_memory(self, findings: dict) -> tuple:
        """Evaluate if findings warrant memory write.

        Args:
            findings: Audit findings dict

        Returns:
            Tuple of (should_write: bool, reason: str)
        """
        # Check pattern trigger (3+ occurrences)
        should_write, reason = self.trigger.should_write_pattern(
            occurrences=findings['occurrences'],
            threshold=3
        )

        if should_write:
            # Also score quality
            score = self.quality.score_memory(findings['description'])
            return True, f"{reason} (quality: {score.total}/33)"

        return False, reason

    def _write_memory(self, findings: dict):
        """Write findings to memory.

        Args:
            findings: Audit findings dict
        """
        print("\n   📝 Writing to memory system...")

        # Create memory entry
        entry = MemoryEntry(
            date=datetime.now().strftime("%Y-%m-%d"),
            agent=self.agent_name,
            type="pattern",
            topic="cors-misconfiguration",
            tags=["security", "cors", "api", "web"],
            confidence="high",
            visibility="public",
            content=findings['description'].strip()
        )

        # Score quality
        score = self.quality.score_memory(entry.content)
        entry.quality_score = score.total

        print(f"   📊 Quality score: {score.total}/33 ({score.tier})")
        print(f"      Reusability: {score.reusability}/3")
        print(f"      Impact: {score.impact}/3")
        print(f"      Clarity: {score.clarity}/3")
        print(f"      Evidence: {score.evidence}/3")
        print(f"      Novelty: {score.novelty}/3")

        if not score.passed:
            print(f"   ⚠️  Quality below threshold - not writing")
            return

        # Validate security
        try:
            filepath = str(
                self.store._get_agent_dir(self.agent_name) /
                self.store._generate_filename(entry)
            )
            self.validator.validate_before_write(
                self.agent_name,
                entry.content,
                filepath
            )
            print(f"   ✅ Security validation passed")
        except Exception as e:
            print(f"   ❌ Security validation failed: {e}")
            return

        # Write to disk
        try:
            filepath = self.store.write_entry(self.agent_name, entry)
            print(f"   ✅ Memory written: {filepath}")
            print(f"\n   💾 Future audits can now leverage this pattern!")
        except FileExistsError:
            print(f"   ℹ️  Memory already exists - reusing existing knowledge")
            print(f"\n   💾 Leveraging previously documented pattern!")


def demonstrate_usage():
    """Demonstrate agent using memory system."""
    print("\n" + "="*60)
    print("DEMONSTRATION: Agent Using Memory System")
    print("="*60)

    # Create agent
    agent = SecurityAuditorAgent()

    # Build indexes first (would be done periodically)
    print("\n🔨 Building search indexes...")
    indexer = MemoryIndexer()
    stats = indexer.build_all_indexes()
    print(f"   ✅ Indexes ready ({stats['inverted']} entries)")

    # Execute first task (no existing memories)
    agent.execute_task("Audit CORS configuration across API endpoints")

    # Execute second similar task (can now leverage memory)
    print("\n\n" + "="*60)
    print("SECOND TASK (with existing memory)")
    print("="*60)

    agent.execute_task("Review CORS settings in new payment service")

    # Show how memory accelerates work
    print("\n" + "="*60)
    print("💡 VALUE DEMONSTRATION")
    print("="*60)

    print("""
Without Memory System:
  - First audit: 30 minutes (discover pattern)
  - Second audit: 30 minutes (re-discover same pattern)
  - Total: 60 minutes

With Memory System:
  - First audit: 30 minutes (discover + document pattern)
  - Second audit: 10 minutes (apply known pattern)
  - Total: 40 minutes

Time Saved: 20 minutes (33% faster) ✅

Quality Improvement:
  - Consistent application of security checks
  - No forgotten edge cases
  - Accumulated expertise over time

Scaling Benefits:
  - 10 similar audits: Save 3+ hours
  - Knowledge shared with other agents
  - Collective intelligence grows
""")


if __name__ == "__main__":
    demonstrate_usage()
