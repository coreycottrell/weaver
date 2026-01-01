---
name: testing-anti-patterns
description: Document and prevent common testing mistakes - never test mock behavior, never add test-only methods to production, never mock without understanding.
---

# Testing Anti-Patterns Skill

**Version**: 1.0
**Date**: 2025-12-16
**Adapted from**: obra/superpowers
**Purpose**: Document and prevent common testing mistakes
**Status**: Active

---

## Core Principle

**"Test what the code does, not what the mocks do."**

Following strict TDD prevents these violations.

---

## The Iron Laws

1. **NEVER test mock behavior**
2. **NEVER add test-only methods to production classes**
3. **NEVER mock without understanding dependencies**

---

## Anti-Pattern 1: Testing Mock Behavior

**Problem:**
```typescript
// WRONG: Tests that mock exists, not that code works
expect(screen.getByTestId('sidebar-mock')).toBeInTheDocument();
```

**Why Wrong:** Tests pass when mocks exist but fail when removed—test never verified real functionality.

**Solution:** Test real component behavior, or don't mock. If mocking, assert on what code DOES with mock, not mock's existence.

**Gate Question:** "Am I testing real component behavior or mock existence?"

---

## Anti-Pattern 2: Test-Only Production Methods

**Problem:**
```python
class Session:
    def destroy(self):  # Only called in test cleanup
        pass
```

**Why Wrong:** Production code polluted with test infrastructure. Dangerous if accidentally called in production.

**Solution:** Keep cleanup in test utilities, not production classes.

**Gate Question:** "Are tests the only consumer of this method?"

---

## Anti-Pattern 3: Mocking Without Understanding

**Problem:** Mocking `discoverAndCacheTools()` breaks config-writing side effect the test depends on.

**Why Wrong:** Over-mocking for "safety" sacrifices actual behavior. Tests pass for wrong reasons.

**Solution:** Run with real code first. Mock only at correct abstraction level—typically the slow/external operation.

**Gate Question:** "Do I understand all side effects? Does test depend on any?"

---

## Anti-Pattern 4: Incomplete Mocks

**Problem:**
```typescript
const mockResponse = {
  status: 'success',
  data: { userId: '123' }
  // Missing: metadata downstream code uses
};
```

**Why Wrong:** Partial mocks hide structural assumptions. Code accessing omitted fields fails silently.

**Solution:** Mirror complete real API response structure.

**Gate Question:** "Have I included all fields from the real response schema?"

---

## Anti-Pattern 5: Integration Tests as Afterthought

**Problem:** "I'll write tests after implementation"

**Why Wrong:** Testing is integral to implementation, not optional follow-up. Separating means missing requirement validation.

**Solution:** TDD: failing test first → implement → pass → complete.

---

## When Mocks Become Too Complex

**Warning Signs:**
- Mock setup exceeds test logic
- Mocking everything to make tests pass
- Mocks missing methods real components have
- Tests break when mocks change
- Can't articulate why mock is necessary

**Question:** "Do we need a mock here?" Complex mocks often signal integration tests would be simpler.

---

## Why TDD Prevents These Patterns

1. **Write test first** → Clarifies what you're really testing
2. **Watch it fail** → Confirms it tests real behavior, not mocks
3. **Minimal implementation** → Prevents test-only methods
4. **Real dependencies visible** → See what test needs before mocking

---

## Red Flags to Watch

- Assertions checking for `*-mock` test IDs
- Methods called only in test files
- Mock setup >50% of test code
- Tests failing when mocks removed
- Inability to explain why mock exists
- Mocking "just to be safe"

---

**"Mocks are tools to isolate, not things to test."**
