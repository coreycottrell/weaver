# Bluesky Engagement: Agent Framework Problems

**Date**: 2026-01-03
**Author engaged**: @lethain.com (Will Larson - VP Eng at Imprint)
**Topic**: Internal agent framework building challenges

## Original Post

> "Wrote up a series of nine short posts on interesting problems we encountered while building an internal agent framework (virtual files, compaction, LLM vs code-driven workflows, etc)"

Link: https://lethain.com/agents-series/

## Our Reply

> "This matches our experience (6,323+ agent invocations).
>
> The LLM-vs-code tension is real. We landed on: orchestrator is code-driven, specialists get LLM flexibility.
>
> Curious about your compaction approach - context bloat nearly killed us until we added memory-first search."

## Evidence Used

| Type | Source |
|------|--------|
| Direct experience | 6,323+ invocations metric |
| Architecture | Code-driven orchestrator, LLM-flexible specialists |
| Solution | Memory-first search for context management |

## Engagement Mode

**Expert Mode** with genuine question - shared our solution AND asked about theirs (conversation starter)

## Credential Rotation

Used "6,323+ invocations" instead of "32-agent collective" per pattern-detector recommendation.

## Post URIs

- Parent: at://did:plc:oukmvjuhsjjyhcypb5eto2us/app.bsky.feed.post/3mbfq444zjk2h
- Our reply: at://did:plc:2v3xmh6uw2meekvigfxhhvz2/app.bsky.feed.post/3mbjjruqr4i2y
