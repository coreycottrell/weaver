#!/usr/bin/env python3
"""
Memory System Integration Test

End-to-end test of the complete memory system:
- Core operations
- Security validation
- Quality scoring
- Search performance
- Federation

Author: The Conductor
Version: 1.0.0
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path
from datetime import datetime

# Import all memory system components
from memory_core import MemoryStore, MemoryEntry
from memory_security import MemorySecurityValidator, SensitiveDataDetector
from memory_quality import MemoryQuality, MemoryTriggerDetector
from memory_search import MemoryIndexer, QueryRouter
from memory_federation import FederationClient


def test_full_workflow():
    """Test complete memory workflow."""
    print("=" * 60)
    print("MEMORY SYSTEM INTEGRATION TEST")
    print("=" * 60)

    # Create temporary directory
    temp_dir = tempfile.mkdtemp()
    knowledge_dir = tempfile.mkdtemp()

    try:
        print(f"\n📁 Test directory: {temp_dir}")

        # Initialize components
        print("\n1️⃣  Initializing components...")
        store = MemoryStore(temp_dir)
        validator = MemorySecurityValidator(temp_dir)
        quality = MemoryQuality()
        indexer = MemoryIndexer(temp_dir)
        router = QueryRouter(temp_dir)
        federation = FederationClient(temp_dir, knowledge_dir)
        print("   ✅ All components initialized")

        # Test 1: Write high-quality memory
        print("\n2️⃣  Writing high-quality memory...")

        excellent_content = """# JWT Authentication Pattern

**Context**: Discovered during security audit of 5 production systems across multiple projects.

## The Pattern

All JWT endpoints MUST validate three critical properties:

1. **Signature Verification** - Validate token signature with correct secret/public key
2. **Expiration Check** - Verify `exp` claim to ensure token is not expired
3. **Issuer Validation** - Check `iss` claim matches expected issuer

Missing ANY of these creates a critical security vulnerability.

## Evidence

**Example 1** (auth.py:45) - Validates all 3 properties ✅

```python
def verify_jwt(token):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=['RS256'],
            options={'verify_exp': True, 'verify_iss': True}
        )
        return payload
    except jwt.InvalidTokenError:
        raise AuthenticationError("Invalid token")
```

**Example 2** (api.py:89) - Missing issuer check ❌

```python
# VULNERABLE: No issuer validation
payload = jwt.decode(token, SECRET_KEY)
```

Found in 40% of audited endpoints (2 out of 5 systems).

## Impact

- **Severity**: HIGH - Allows token forgery and privilege escalation
- **Frequency**: Common (40% of systems had this issue)
- **Time to exploit**: <1 hour for skilled attacker
- **Fix time**: 5 minutes per endpoint

## Application Checklist

When implementing JWT validation:

- [ ] Verify signature with correct secret/public key
- [ ] Check `exp` claim (token not expired)
- [ ] Validate `iss` claim (matches expected issuer)
- [ ] Use algorithm whitelist (prevent algorithm confusion attacks)
- [ ] Test with tampered tokens (comprehensive unit tests)
- [ ] Monitor for validation failures (detect attacks)

## Related Patterns

- OAuth2 token validation (similar principles)
- API key validation (alternative approach)
- Session management (contrasting approach)

## References

- RFC 7519: JSON Web Token (JWT) specification
- OWASP JWT Security Cheat Sheet
- Auth0 JWT Best Practices Guide
"""

        entry = MemoryEntry(
            date=datetime.now().strftime("%Y-%m-%d"),
            agent="security-auditor",
            type="pattern",
            topic="jwt-authentication",
            tags=["authentication", "security", "jwt", "api"],
            confidence="high",
            visibility="public",
            content=excellent_content
        )

        # Score quality
        score = quality.score_memory(excellent_content)
        entry.quality_score = score.total

        print(f"   Quality score: {score.total}/33 ({score.tier})")
        print(f"   Dimensions: R={score.reusability} I={score.impact} C={score.clarity} E={score.evidence} N={score.novelty}")
        assert score.passed, "High-quality memory should pass"
        assert score.total >= 24, f"Expected score >=24, got {score.total}"
        print("   ✅ Quality validation passed")

        # Validate security
        filepath = str(Path(store._get_agent_dir("security-auditor")) / store._generate_filename(entry))
        validator.validate_before_write("security-auditor", excellent_content, filepath)
        print("   ✅ Security validation passed")

        # Write memory
        filepath = store.write_entry("security-auditor", entry)
        print(f"   ✅ Memory written: {Path(filepath).name}")

        # Test 2: Block low-quality memory
        print("\n3️⃣  Testing quality filtering...")

        poor_content = "Fixed a bug in auth.py line 45."
        poor_score = quality.score_memory(poor_content)

        print(f"   Poor content score: {poor_score.total}/33 ({poor_score.tier})")
        assert not poor_score.passed, "Low-quality memory should fail"
        print("   ✅ Low-quality content correctly rejected")

        # Test 3: Block secret leakage
        print("\n4️⃣  Testing secret detection...")

        secret_content = "API key: ghp_123456789012345678901234567890123456"
        detector = SensitiveDataDetector()
        findings = detector.scan(secret_content)

        assert len(findings) > 0, "Should detect secret"
        print(f"   Found {len(findings)} secrets")
        print(f"   Type: {findings[0]['type']}")
        print("   ✅ Secret detection working")

        # Test 4: Write second memory for search testing
        print("\n5️⃣  Writing second memory...")

        oauth_content = """# OAuth2 Authorization Flow Pattern

**Context**: OAuth2 implementation across multiple client applications.

## The Pattern

Standard OAuth2 authorization code flow with PKCE:

1. Client generates code_verifier and code_challenge
2. Redirect to authorization endpoint with challenge
3. User authenticates and approves
4. Authorization server returns code
5. Client exchanges code + verifier for tokens

## Evidence

Implemented in 3 production applications with 99.9% uptime.

## Impact

Provides secure delegated access without exposing credentials.

## Related

- JWT tokens (used as access tokens)
- Refresh token rotation
"""

        oauth_entry = MemoryEntry(
            date=datetime.now().strftime("%Y-%m-%d"),
            agent="security-auditor",
            type="pattern",
            topic="oauth2-flow",
            tags=["authentication", "oauth2", "security"],
            confidence="high",
            visibility="public",
            content=oauth_content
        )

        oauth_score = quality.score_memory(oauth_content)
        oauth_entry.quality_score = oauth_score.total

        oauth_filepath = store.write_entry("security-auditor", oauth_entry)
        print(f"   ✅ Second memory written: {Path(oauth_filepath).name}")

        # Test 5: Build indexes
        print("\n6️⃣  Building search indexes...")

        index_stats = indexer.build_all_indexes()
        print(f"   Inverted index: {index_stats['inverted']} entries")
        print(f"   Chronological: {index_stats['chronological']} entries")
        print(f"   Agent index: {index_stats['agent']} entries")
        assert index_stats['inverted'] == 2, "Should have 2 memories indexed"
        print("   ✅ Indexes built successfully")

        # Test 6: Search memories
        print("\n7️⃣  Testing search...")

        # Search by keyword
        result1 = router.search("authentication")
        print(f"   Search 'authentication': {len(result1['results'])} results (tier {result1['tier']}, {result1['elapsed_ms']:.1f}ms)")
        assert len(result1['results']) == 2, "Should find both memories"

        # Search by tag
        result2 = router.search("jwt")
        print(f"   Search 'jwt': {len(result2['results'])} results (tier {result2['tier']}, {result2['elapsed_ms']:.1f}ms)")
        assert len(result2['results']) >= 1, "Should find JWT memory"

        # Test cache hit
        result3 = router.search("authentication")
        assert result3['tier'] == 1, "Second search should hit cache"
        print(f"   Cache hit: tier {result3['tier']}, {result3['elapsed_ms']:.1f}ms")

        # Get search stats
        stats = router.get_stats()
        print(f"   Cache hit rate: {stats['cache_hit_rate']:.1%}")
        print("   ✅ Search working efficiently")

        # Test 7: Federation (export)
        print("\n8️⃣  Testing knowledge export...")

        package = federation.export_memories(
            agent="security-auditor",
            visibility="public",
            topics=["authentication"],
            sign=False  # Skip signing for test
        )

        print(f"   Package ID: {package['package_id']}")
        print(f"   Insights: {len(package['insights'])}")
        print(f"   Topics: {', '.join(package['topics'])}")
        assert len(package['insights']) == 2, "Should export 2 memories"
        print("   ✅ Export successful")

        # Save package
        package_file = federation.save_package(package, "test-export.json")
        print(f"   Saved to: {Path(package_file).name}")

        # Test 8: Federation (import)
        print("\n9️⃣  Testing knowledge import...")

        imported = federation.import_memories(
            package_file,
            verify=False,
            quarantine=True
        )

        print(f"   Imported: {imported} memories")
        assert imported == 2, "Should import 2 memories"
        print("   ✅ Import successful")

        # Test 9: Read and verify imported memory
        print("\n🔟 Verifying imported memory...")

        # List memories in quarantine
        quarantine_dir = Path(knowledge_dir) / "federated" / "quarantine" / "ai-civ-team-1"
        imported_files = list(quarantine_dir.glob("*.md"))

        print(f"   Files in quarantine: {len(imported_files)}")
        assert len(imported_files) == 2, "Should have 2 imported files"

        # Read one
        imported_memory = imported_files[0].read_text()
        assert "federated-" in imported_memory, "Should be marked as federated"
        print("   ✅ Imported memories verified")

        # Summary
        print("\n" + "=" * 60)
        print("✅ ALL INTEGRATION TESTS PASSED")
        print("=" * 60)

        print("\n📊 System Capabilities Verified:")
        print("   ✅ High-quality memory writing")
        print("   ✅ Quality filtering (blocks low-value content)")
        print("   ✅ Secret detection (prevents leaks)")
        print("   ✅ Search indexing and routing")
        print("   ✅ Multi-tier search (cache → index → grep)")
        print("   ✅ Knowledge export (federation)")
        print("   ✅ Knowledge import (federation)")
        print("   ✅ Quarantine workflow")

        print(f"\n📈 Performance:")
        print(f"   - Index build: {index_stats['elapsed_seconds']:.2f}s for 2 memories")
        print(f"   - Search latency: {result1['elapsed_ms']:.1f}ms (tier {result1['tier']})")
        print(f"   - Cache latency: {result3['elapsed_ms']:.1f}ms (tier {result3['tier']})")
        print(f"   - Cache hit rate: {stats['cache_hit_rate']:.1%}")

        return True

    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        # Cleanup
        shutil.rmtree(temp_dir)
        shutil.rmtree(knowledge_dir)
        print(f"\n🧹 Cleanup complete")


if __name__ == "__main__":
    success = test_full_workflow()
    sys.exit(0 if success else 1)
