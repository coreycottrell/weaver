# 🏛️ Test Debt: Immediate Action Plan

**Status**: 🔴 CRITICAL - 85/100 Test Debt Score
**Current Coverage**: 4.2% (847 lines tests / 19,918 lines code)
**Target**: 90/100 readiness for 1000+ nodes

---

## 🚨 CRITICAL ACTIONS (This Week)

### 1. Fix Broken Signing Test (0.5 days)
**Status**: 🔴 BLOCKING - Ed25519 authentication broken
**Command**:
```bash
cd /home/user/weaver
# Fix cryptography dependency
pip install --upgrade cryptography cffi
python3 tools/test_signing.py
# Should see: ✅ All tests passed
```
**Success Criteria**: All 15+ test cases pass

### 2. Create tests/ Directory (0.5 days)
**Status**: ❌ Directory doesn't exist (pytest can't run)
**Command**:
```bash
cd /home/user/weaver
mkdir -p tests/{unit,integration,e2e,fixtures}
touch tests/conftest.py
touch tests/__init__.py
```
**Structure**:
```
tests/
├── unit/              # Individual component tests
├── integration/       # Cross-component tests
├── e2e/              # End-to-end flow tests
├── fixtures/         # Test data
└── conftest.py       # Pytest configuration
```

### 3. Move Existing Tests (0.25 days)
**Status**: Tests in wrong location (tools/ not tests/)
**Command**:
```bash
cd /home/user/weaver
# Move to correct location
mv tools/test_memory_integration.py tests/integration/
mv tools/test_signing.py tests/integration/
mv tools/test_dashboard_install.py tests/integration/

# Verify pytest can find them
pytest --collect-only
```

### 4. Set Up CI/CD (1 day)
**Status**: ❌ No automated testing
**File**: `.github/workflows/test.yml`
**Command**:
```bash
cd /home/user/weaver
mkdir -p .github/workflows
```
**Content**:
```yaml
name: Test Suite

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.9", "3.10", "3.11", "3.12"]

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e .[dev]

    - name: Run tests with pytest
      run: |
        pytest --cov=tools --cov=web --cov-report=html --cov-report=term-missing

    - name: Check code formatting
      run: black --check .

    - name: Lint with flake8
      run: flake8 tools/ web/ --max-line-length=120

    - name: Security scan
      run: bandit -r tools/ web/

    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        files: ./coverage.xml
```

---

## 🔥 URGENT (Next 2 Weeks)

### 5. Agent Invocation Tests (2 days)
**File**: `tests/integration/test_agent_invocation.py`
**Why Critical**: 27 agents completely untested
**Pseudocode**:
```python
import pytest
from pathlib import Path

def get_all_agent_manifests():
    """Load all 27 agent manifests."""
    agent_dir = Path(".claude/agents")
    return list(agent_dir.glob("*.md"))

@pytest.mark.parametrize("agent_manifest", get_all_agent_manifests())
def test_agent_invocation(agent_manifest):
    """Test that each agent can be invoked via manifest."""
    agent_name = agent_manifest.stem

    # Parse agent manifest
    agent = parse_agent_manifest(agent_manifest)

    # Create test task appropriate for agent domain
    task = generate_test_task(agent.domain)

    # Invoke agent
    result = invoke_agent(agent_name, task)

    # Validate response
    assert result is not None
    assert result.agent == agent_name
    assert result.output_format_valid()
    assert result.completed
```

### 6. Memory Security Tests (1 day)
**File**: `tests/unit/test_memory_security.py`
**Why Critical**: Secret leakage = ecosystem breach
**Pseudocode**:
```python
from memory_security import SensitiveDataDetector, MemorySecurityValidator

def test_api_key_detection():
    detector = SensitiveDataDetector()

    # Test various API key formats
    assert detector.has_secrets("OPENAI_API_KEY=sk-proj-abc123")
    assert detector.has_secrets("Bearer sk-abc123")
    assert detector.has_secrets("api_key: 'sk-12345'")

    # Should not flag safe content
    assert not detector.has_secrets("This is a safe string")
    assert not detector.has_secrets("API documentation")

def test_password_detection():
    detector = SensitiveDataDetector()
    assert detector.has_secrets("password=myP@ssw0rd123")
    assert detector.has_secrets("PASSWORD: supersecret")
    assert not detector.has_secrets("password field documentation")

def test_token_detection():
    detector = SensitiveDataDetector()
    assert detector.has_secrets("ghp_1234567890abcdef")  # GitHub token
    assert detector.has_secrets("Authorization: Bearer eyJ...")  # JWT
```

### 7. Skills Infrastructure Tests (2 days)
**File**: `tests/integration/test_skills.py`
**Why Critical**: 60-70% efficiency multiplier at risk
**Pseudocode**:
```python
import pytest
from pathlib import Path

def get_all_skills():
    """Get all available skills."""
    skills_dir = Path(".claude/skills")
    return [s.name for s in skills_dir.iterdir() if s.is_dir()]

@pytest.mark.parametrize("skill_name", get_all_skills())
def test_skill_loads(skill_name):
    """Test that each skill can be loaded."""
    skill = load_skill(skill_name)
    assert skill is not None
    assert skill.can_execute()

def test_pdf_skill():
    """Test PDF processing skill."""
    skill = load_skill("pdf")

    # Test with fixture PDF
    test_pdf = Path("tests/fixtures/test.pdf")
    result = skill.process(test_pdf)

    assert result.success
    assert len(result.text) > 0
    assert result.page_count > 0

def test_docx_skill():
    """Test DOCX processing skill."""
    skill = load_skill("docx")

    test_docx = Path("tests/fixtures/test.docx")
    result = skill.process(test_docx)

    assert result.success
    assert len(result.text) > 0

def test_xlsx_skill():
    """Test XLSX processing skill."""
    skill = load_skill("xlsx")

    test_xlsx = Path("tests/fixtures/test.xlsx")
    result = skill.process(test_xlsx)

    assert result.success
    assert result.sheet_count > 0
    assert len(result.data) > 0
```

### 8. Flow Execution Tests (3 days)
**File**: `tests/e2e/test_flows.py`
**Why Critical**: Coordination patterns for 1M agents
**Pseudocode**:
```python
import pytest
from pathlib import Path

def get_all_flows():
    """Get all coordination flows."""
    flows_dir = Path(".claude/flows")
    return [f.stem for f in flows_dir.glob("*.md")
            if not f.name.endswith("-needs-testing.md")]

@pytest.mark.parametrize("flow_name", get_all_flows())
@pytest.mark.slow
def test_flow_execution(flow_name):
    """Test that each flow executes successfully."""
    flow = load_flow(flow_name)

    # Create test agents
    test_agents = get_test_agents_for_flow(flow)

    # Create test query/task
    test_query = generate_test_query(flow.domain)

    # Execute flow
    result = flow.execute(agents=test_agents, query=test_query)

    # Validate all agents completed
    assert all(agent.completed for agent in result.agents)

    # Validate synthesis produced
    assert result.synthesis is not None
    assert len(result.synthesis) > 0

    # Validate output format
    assert result.output_format_valid()
```

---

## ⚠️ HIGH PRIORITY (Week 3-4)

### 9. Hub Communication Tests (1.5 days)
**File**: `tests/integration/test_hub.py`
**Pseudocode**:
```python
import pytest
from unittest.mock import Mock, patch

@patch('hub_client.requests.post')
def test_send_hub_message(mock_post):
    """Test sending message to hub."""
    mock_post.return_value.status_code = 200

    message = create_hub_message("test", "test content")
    result = send_to_hub(message)

    assert result.delivered
    assert result.signed
    assert mock_post.called

@patch('hub_client.git.Repo')
def test_check_hub_messages(mock_repo):
    """Test checking for new hub messages."""
    mock_repo.return_value.head.commit.hexsha = "abc123"

    count = check_hub_messages()

    assert isinstance(count, int)
    assert count >= 0
```

### 10. Email System Tests (1.5 days)
**File**: `tests/integration/test_email.py`
**Pseudocode**:
```python
import pytest
from unittest.mock import Mock, patch

@patch('smtplib.SMTP')
def test_send_email(mock_smtp):
    """Test email sending."""
    email = create_email(
        to="test@example.com",
        subject="Test",
        body="Test email"
    )

    result = send_email(email)

    assert result.sent
    assert mock_smtp.return_value.sendmail.called

@patch('imaplib.IMAP4_SSL')
def test_check_email_inbox(mock_imap):
    """Test checking for unread emails."""
    mock_imap.return_value.search.return_value = ('OK', [b'1 2 3'])

    count = check_email_inbox()

    assert count == 3
```

### 11. Memory Federation Tests (2 days)
**File**: `tests/integration/test_memory_federation.py`
**Pseudocode**:
```python
import pytest
from memory_federation import FederationClient

def test_knowledge_sync(tmp_path):
    """Test knowledge synchronization."""
    client = FederationClient(
        memory_dir=tmp_path / "memory",
        knowledge_dir=tmp_path / "knowledge"
    )

    result = client.sync_knowledge()

    assert result.entries_synced >= 0
    assert result.conflicts_resolved >= 0

def test_cross_civ_query(tmp_path):
    """Test querying across CIVs."""
    client = FederationClient(tmp_path, tmp_path)

    results = client.federated_query("test query")

    assert isinstance(results, list)
```

---

## 📊 Progress Tracking

### Test Coverage Goals

| Phase | Target Coverage | Target Score | Deadline | Status |
|-------|----------------|--------------|----------|--------|
| **Phase 0** (Current) | 4% | 15/100 | - | ✅ Baseline |
| **Phase 1** (Blockers) | 25% | 40/100 | Week 2 | 🔴 TODO |
| **Phase 2** (High Priority) | 50% | 70/100 | Week 4 | ⏳ Pending |
| **Phase 3** (Medium Priority) | 75% | 90/100 | Week 6 | ⏳ Pending |
| **Phase 4** (Scale Ready) | 90% | 95/100 | Week 8 | ⏳ Pending |

### Component Testing Status

| Component | Status | Tests Written | Coverage | Priority |
|-----------|--------|---------------|----------|----------|
| **Agent Invocation** | 🔴 Not Started | 0 | 0% | P0 |
| **Ed25519 Signing** | 🔴 Broken | 1 (broken) | 0% | P0 |
| **Skills Infrastructure** | 🔴 Not Started | 0 | 0% | P0 |
| **Memory System** | 🟢 Partial | 1 | 30% | P0 |
| **Flow Execution** | 🔴 Not Started | 0 | 0% | P1 |
| **Hub Communication** | 🔴 Not Started | 0 | 0% | P1 |
| **Email System** | 🔴 Not Started | 0 | 0% | P1 |
| **Memory Federation** | 🔴 Not Started | 0 | 0% | P1 |
| **Dashboard** | 🟡 Installation Only | 1 | 10% | P2 |
| **Telegram** | 🔴 Not Started | 0 | 0% | P2 |

---

## 🎯 Success Metrics

### Week 1 Goals
- ✅ Fix test_signing.py (all tests pass)
- ✅ Create tests/ directory structure
- ✅ Move existing tests to tests/
- ✅ Set up CI/CD pipeline
- ✅ First CI/CD run passes

### Week 2 Goals
- ✅ Agent invocation tests (27 agents tested)
- ✅ Memory security tests (secret detection validated)
- ✅ Skills infrastructure tests (PDF/DOCX/XLSX working)
- ✅ Test coverage: 25%+
- ✅ Test score: 40/100

### Week 4 Goals
- ✅ Flow execution tests (15+ flows validated)
- ✅ Hub communication tests (send/receive working)
- ✅ Email system tests (SMTP/IMAP mocked)
- ✅ Memory federation tests (cross-CIV sync)
- ✅ Test coverage: 50%+
- ✅ Test score: 70/100
- ✅ **Production ready for 100 nodes**

### Week 6 Goals
- ✅ All P2 components tested
- ✅ Test coverage: 75%+
- ✅ Test score: 90/100
- ✅ **Production ready for 1000 nodes**

### Week 8 Goals
- ✅ Load testing complete
- ✅ Stress testing complete
- ✅ Performance benchmarks established
- ✅ Chaos engineering validated
- ✅ Test coverage: 90%+
- ✅ Test score: 95/100
- ✅ **Ready for 1M agents**

---

## 📝 Daily Checklist Template

### Morning (Test Development)
- [ ] Run full test suite: `pytest -v`
- [ ] Check coverage report: `pytest --cov --cov-report=term`
- [ ] Write 3-5 new tests
- [ ] Fix any failing tests
- [ ] Update test documentation

### Afternoon (Test Quality)
- [ ] Run code quality tools: `black . && flake8 . && mypy .`
- [ ] Run security scan: `bandit -r tools/ web/`
- [ ] Review test failures in CI/CD
- [ ] Update test fixtures as needed
- [ ] Document test patterns discovered

### Evening (Progress Update)
- [ ] Update progress tracking (coverage %, score)
- [ ] Commit test code to repository
- [ ] Trigger CI/CD pipeline
- [ ] Review coverage report
- [ ] Plan tomorrow's test targets

---

## 🚀 Quick Commands

### Run All Tests
```bash
cd /home/user/weaver
pytest -v --cov=tools --cov=web --cov-report=html
```

### Run Specific Test Category
```bash
# Unit tests only
pytest tests/unit/ -v

# Integration tests only
pytest tests/integration/ -v

# End-to-end tests (slow)
pytest tests/e2e/ -v -m slow
```

### Check Coverage
```bash
# Terminal report
pytest --cov --cov-report=term-missing

# HTML report (detailed)
pytest --cov --cov-report=html
open htmlcov/index.html
```

### Code Quality
```bash
# Format code
black .

# Lint
flake8 tools/ web/ --max-line-length=120

# Type check
mypy tools/

# Security scan
bandit -r tools/ web/
```

### Generate Coverage Badge
```bash
coverage-badge -o coverage.svg -f
```

---

## 📚 Resources

### Test Writing Guide
- **pytest docs**: https://docs.pytest.org/
- **unittest.mock**: https://docs.python.org/3/library/unittest.mock.html
- **pytest fixtures**: https://docs.pytest.org/en/stable/fixture.html
- **pytest parametrize**: https://docs.pytest.org/en/stable/parametrize.html

### Test Patterns
- **AAA Pattern**: Arrange, Act, Assert
- **Given-When-Then**: BDD-style tests
- **Test Doubles**: Mocks, stubs, fakes, spies
- **Fixtures**: Reusable test data setup

### Coverage Goals
- **Unit tests**: 80%+ coverage
- **Integration tests**: 70%+ coverage
- **E2E tests**: 60%+ coverage (slower, harder to maintain)
- **Overall**: 70-90% coverage (diminishing returns after 90%)

---

## 🎓 Test-First Culture

### Principles
1. **Write tests BEFORE code** (TDD when possible)
2. **Test behavior, not implementation**
3. **Keep tests simple and readable**
4. **One assertion per test** (when possible)
5. **Fast tests run often** (unit tests < 1s each)
6. **Slow tests run nightly** (e2e tests can be slow)

### Test Naming
```python
def test_<component>_<scenario>_<expected_result>():
    """Test that <component> <does something> when <scenario>."""
    pass

# Examples:
def test_memory_store_creates_entry_successfully()
def test_agent_invocation_fails_with_invalid_manifest()
def test_skills_loading_raises_error_when_skill_missing()
```

### Test Structure (AAA Pattern)
```python
def test_example():
    # Arrange - Set up test data
    store = MemoryStore(temp_dir)
    entry = MemoryEntry(content="test")

    # Act - Execute the code being tested
    result = store.write_entry("agent", entry)

    # Assert - Verify the result
    assert result.success
    assert result.entry_id is not None
```

---

**Next**: Execute Phase 1 (Week 1-2) to achieve 40/100 test score

**Goal**: Safe scaling to 1M agents across 1000+ nodes

**Timeline**: 8 weeks to production readiness

**Let's build tests that scale. 🏛️**
