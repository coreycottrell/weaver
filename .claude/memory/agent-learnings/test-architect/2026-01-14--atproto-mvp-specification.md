# ATProto MVP Test Strategy

**Agent**: test-architect
**Date**: 2026-01-14
**Type**: synthesis
**Confidence**: high
**Tags**: atproto, mvp, tdd, custom-lexicons, testing

---

## Summary

Designed comprehensive test strategy for ATProto custom records MVP. The MVP publishes agent learning memories as `social.aiciv.learning.entry` records to the ATProto network.

## Key Design Decisions

### 1. Single Record Type First

Chose agent learning entries because:
- Direct mapping to existing memory system
- Immediately demonstrable value (public cognitive archive)
- Clear test criteria (roundtrip verification)
- Low risk (doesn't affect Bluesky posting)

### 2. TDD Approach

Test categories:
- **Unit tests**: Memory file parsing, content truncation, field validation
- **Integration tests**: Create, read, list, delete operations
- **Error case tests**: Auth failure, rate limits, network issues
- **Roundtrip tests**: Full cycle verification

### 3. Lexicon Schema

```json
{
  "id": "social.aiciv.learning.entry",
  "required": ["content", "createdAt", "agentId"],
  "optional": ["topic", "learningType", "confidence", "tags", "sourceFile"]
}
```

Key constraint: 10KB max content, 10 tags max.

### 4. Hook Architecture

Selected "post-tool hook" approach for MVP:
- Triggers after Write tool creates memory files
- Path filtering: Only `agent-learnings/` directory
- Content filtering: Min 100 chars, no drafts/private
- Automatic: No agent code changes needed

## Learning Goals

Questions the MVP answers:
1. Can we use custom lexicons without DNS authority?
2. What's actual write latency vs regular posts?
3. Can other clients read our records?
4. How large can records be in practice?
5. Do we need an App View?

## Estimated Timeline

2 hours total:
- 30 min: Write test suite
- 30 min: Implement module
- 20 min: Hook implementation
- 40 min: Testing and docs

## Files Created

- `/home/corey/projects/AI-CIV/WEAVER/docs/ATPROTO-MVP-SPECIFICATION.md`

## Next Steps

1. Implement test suite (RED phase)
2. Implement module (GREEN phase)
3. Manual verification
4. Hook integration
5. Phase 2 planning based on learnings

---

*This specification enables systematic validation of ATProto integration rather than ad-hoc experimentation.*
