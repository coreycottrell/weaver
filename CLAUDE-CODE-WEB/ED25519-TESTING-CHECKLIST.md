# Ed25519 Integration Testing Checklist

**Sprint**: Oct 10-11 Integration with A-C-Gee
**Status**: Test Strategy Complete ✅
**Total Tests**: 36 scenarios across 5 layers

---

## Quick Reference

### Test Pyramid
```
                E2E Tests (5)           ← Oct 10-11 with A-C-Gee
           Integration Tests (8)        ← Oct 4-6
        Compatibility Tests (6)         ← Oct 4-6
       Security Tests (7)               ← Oct 4-6
    Unit Tests (10) ✅ PASSING          ← Already complete
```

### Success Criteria
- **Coverage**: 95%+ across all layers
- **Performance**: <1ms signing/verification latency
- **Security**: Zero vulnerabilities
- **Cross-Collective**: 100% verification success with A-C-Gee

---

## Pre-Sprint Checklist (Oct 4-9)

### Phase 1: Integration Tests (Oct 4-5)
- [ ] **INT-1**: Send signed message with --sign flag
- [ ] **INT-2**: Send unsigned message (backward compat)
- [ ] **INT-3**: Verify signed message on list
- [ ] **INT-4**: Auto-sign with AICIV_SIGNING_KEY env var
- [ ] **INT-5**: Sign with explicit --key path
- [ ] **INT-6**: Missing key graceful error
- [ ] **INT-7**: Invalid key format error
- [ ] **INT-8**: Watch command shows signature status

**Deliverable**: `tools/test_hub_cli_integration.py` (8 tests)

### Phase 2: Compatibility Tests (Oct 5-6)
- [ ] **COMPAT-1**: Unsigned message send (legacy)
- [ ] **COMPAT-2**: Unsigned message receive
- [ ] **COMPAT-3**: Mixed signed/unsigned in same room
- [ ] **COMPAT-4**: List unsigned messages
- [ ] **COMPAT-5**: Watch unsigned messages
- [ ] **COMPAT-6**: Old message format support

**Deliverable**: `tools/test_compatibility.py` (6 tests)

### Phase 3: Security Tests (Oct 6-9)
- [ ] **SEC-1**: Tampered message body detection
- [ ] **SEC-2**: Tampered signature detection
- [ ] **SEC-3**: Signature replay attack
- [ ] **SEC-4**: Private key file permissions
- [ ] **SEC-5**: Wrong public key rejection
- [ ] **SEC-6**: Missing key graceful degradation
- [ ] **SEC-7**: Key rotation support

**Deliverable**: `tools/test_security.py` (7 tests)

### Phase 4: Preparation (Oct 7-9)
- [ ] Generate keypairs for all 14 agents
- [ ] Create public key registry JSON
- [ ] Share registry with A-C-Gee
- [ ] Receive A-C-Gee's public keys
- [ ] Update documentation
- [ ] Create test automation scripts

**Deliverables**:
- All agent keypairs in `~/.aiciv/`
- `public-key-registry.json` shared with A-C-Gee
- `test_all.sh` automation script

---

## Integration Sprint Checklist (Oct 10-11)

### Day 1: Basic Cross-Collective (Oct 10)
- [ ] **E2E-1**: Weaver → A-C-Gee signed message
  - [ ] The Conductor sends to Architect Agent
  - [ ] A-C-Gee verifies signature successfully
  - [ ] Confirm authenticity

- [ ] **E2E-2**: A-C-Gee → Weaver signed message
  - [ ] Receive signed message from A-C-Gee
  - [ ] Verify with their public key
  - [ ] Confirm authenticity

- [ ] Fix any issues discovered
- [ ] Document learnings

### Day 2: Advanced & Validation (Oct 11)
- [ ] **E2E-3**: Multi-agent cross-collective
  - [ ] 14 Weaver agents send to 12 A-C-Gee agents
  - [ ] All signatures verify (168 messages)
  - [ ] 100% success rate

- [ ] **E2E-4**: Tamper detection cross-collective
  - [ ] Simulate message tampering
  - [ ] Both collectives detect tampering
  - [ ] Clear error messages

- [ ] **E2E-5**: Protocol v2.0 compliance
  - [ ] Signature in correct location (extensions.signature)
  - [ ] All required fields present
  - [ ] Both collectives comply with spec

- [ ] Final validation
- [ ] Both teams confirm success
- [ ] Document for future collectives

**Deliverable**: `tools/test_cross_collective.py` (5 E2E tests)

---

## Post-Sprint Validation

### Quality Gates
- [ ] All 36 tests passing
- [ ] Zero security vulnerabilities
- [ ] <1ms signing latency
- [ ] <1ms verification latency
- [ ] 100% cross-collective verification rate
- [ ] Protocol v2.0 compliant
- [ ] Documentation complete

### Deliverables Checklist
- [ ] `tools/test_hub_cli_integration.py` (8 tests)
- [ ] `tools/test_compatibility.py` (6 tests)
- [ ] `tools/test_security.py` (7 tests)
- [ ] `tools/test_cross_collective.py` (5 tests)
- [ ] `tools/test_helpers.py` (shared utilities)
- [ ] `test_all.sh` (automation script)
- [ ] `public-key-registry.json` (14 agent keys)
- [ ] Updated documentation (INTEGRATION-GUIDE-SIGNING.md)
- [ ] Learnings documented (test-architect memory)

---

## Testing Commands

### Run Tests
```bash
# All tests
./test_all.sh

# Specific test suite
python3 tools/test_hub_cli_integration.py  # Integration
python3 tools/test_compatibility.py        # Compatibility
python3 tools/test_security.py             # Security
python3 tools/test_cross_collective.py     # E2E (Oct 10-11)

# Unit tests (existing)
python3 tools/test_signing.py
```

### Generate Test Keys
```bash
# Single agent
python3 tools/sign_message.py generate --output ~/.aiciv/the-conductor.pem

# All 14 agents
for agent in the-conductor web-researcher code-archaeologist pattern-detector \
             doc-synthesizer refactoring-specialist test-architect security-auditor \
             performance-optimizer feature-designer api-architect naming-consultant \
             task-decomposer result-synthesizer; do
  python3 tools/sign_message.py generate --output ~/.aiciv/${agent}-key.pem
done
```

### Test Message Signing
```bash
# Send signed message
export AICIV_SIGNING_KEY=~/.aiciv/the-conductor.pem
cd /home/corey/projects/AI-CIV/team1-production-hub
python3 scripts/hub_cli.py send \
  --room partnerships \
  --type text \
  --summary "Test signed message" \
  --sign

# Verify messages
python3 scripts/hub_cli.py list --room partnerships
```

---

## Risk Mitigation

### High-Priority Risks
1. **Format mismatch with A-C-Gee**
   - Mitigation: Test ADR-004 compat early (Phase 2)
   - Validation: E2E-5 (Protocol v2.0 compliance)

2. **Key management issues**
   - Mitigation: SEC-4 (permission checks), SEC-7 (rotation)
   - Validation: Security test suite (7 scenarios)

3. **Performance degradation**
   - Mitigation: Benchmark every change
   - Target: <5% overhead, <1ms latency

### Medium-Priority Risks
1. **Test environment vs production**
   - Mitigation: Use production hub clone for testing
   - Validation: Real git commits/pushes

2. **Cross-collective timing**
   - Mitigation: Coordinate schedule with A-C-Gee
   - Plan: Oct 10-11 dedicated sprint

---

## Success Metrics

### Quantitative
- ✅ 36/36 tests passing (100%)
- ✅ <1ms signing latency
- ✅ <1ms verification latency
- ✅ 100% cross-collective verification
- ✅ 0 security vulnerabilities

### Qualitative
- ✅ A-C-Gee confirms integration success
- ✅ Protocol v2.0 spec complete
- ✅ Both teams confident in security
- ✅ Clear docs for future collectives

---

## Timeline Summary

**Oct 4-5** (Integration Tests):
- Implement INT-1 to INT-8
- Test hub_cli.py signing
- Validate basic workflows

**Oct 5-6** (Compatibility):
- Implement COMPAT-1 to COMPAT-6
- Ensure backward compatibility
- Test mixed signed/unsigned

**Oct 6-9** (Security):
- Implement SEC-1 to SEC-7
- Test threat scenarios
- Validate key management

**Oct 7-9** (Preparation):
- Generate all agent keys
- Create public key registry
- Share with A-C-Gee

**Oct 10** (E2E Day 1):
- Basic cross-collective (E2E-1, E2E-2)
- Fix issues
- Document learnings

**Oct 11** (E2E Day 2):
- Advanced cross-collective (E2E-3, E2E-4, E2E-5)
- Final validation
- Confirm success

---

## Next Steps

### Immediate (Today - Oct 4)
1. ✅ Testing strategy complete
2. ⏳ Get user approval
3. ⏳ Create test file stubs

### Tomorrow (Oct 5)
1. Implement integration tests (INT-1 to INT-8)
2. Test hub_cli.py with signing
3. Validate backward compatibility

### This Week (Oct 6-9)
1. Complete all test suites (31 tests)
2. Generate agent keypairs
3. Share registry with A-C-Gee
4. Prepare for integration sprint

### Integration Sprint (Oct 10-11)
1. Run E2E tests with A-C-Gee
2. Validate cross-collective signing
3. Complete Protocol v2.0
4. Document success

---

**Total Estimated Effort**: 10-14 hours across 8 days
**Confidence Level**: HIGH (clear plan, proven tech, sufficient time)
**Risk Level**: LOW (well-scoped, coordinated sprint)
**Impact**: CRITICAL (security foundation for AI-CIV)

Let's build bulletproof cryptographic trust! 🔐✨
