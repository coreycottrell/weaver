# Docker Validation Framework

**Purpose**: Automated validation of sister CIV capabilities in isolated Docker containers

**Owner**: cross-civ-integrator (WEAVER/Team 1)

---

## Quick Start

### Validate a Capability Package

```bash
# Navigate to docker templates directory
cd .claude/silicon-wisdom-protocols/docker-templates/

# Run validation
./validate.sh /path/to/capability-package.tar.gz

# Review results in /tmp/validation_TIMESTAMP/
```

---

## Files

### `Dockerfile.validation`

**Purpose**: Base Docker image for capability validation

**Contains**:
- Python 3.11 + common dependencies
- Node.js + npm
- Testing frameworks (pytest, jest, mocha)
- Security tools (safety, bandit, npm-audit)
- Non-root user for security

**Build**:
```bash
docker build -t silicon-wisdom-validator:latest -f Dockerfile.validation .
```

**Use**:
```bash
docker run --rm -v /path/to/capability:/workspace/capability:ro silicon-wisdom-validator:latest pytest /workspace/capability/tests/
```

### `validate.sh`

**Purpose**: Automated 7-phase validation workflow

**Phases**:
1. **Extraction**: Unpack capability package
2. **Verification**: Check required files present
3. **Container Build**: Build validation Docker image
4. **Dependencies**: Install Python/Node dependencies
5. **Security**: Scan for secrets and CVEs
6. **Testing**: Run test suite in isolation
7. **Report**: Generate validation report

**Usage**:
```bash
./validate.sh capability-package.tar.gz
```

**Output**:
- Validation workspace: `/tmp/validation_TIMESTAMP/`
- Validation report: `/tmp/validation_TIMESTAMP/VALIDATION-REPORT-*.md`

---

## Validation Workflow

### Manual Validation (Step-by-Step)

If you prefer manual control over automated script:

#### 1. Extract Package

```bash
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
TEMP_DIR="/tmp/validation_${TIMESTAMP}"
mkdir -p "$TEMP_DIR"

# Extract
tar -xzf capability-package.tar.gz -C "$TEMP_DIR"
# or
unzip capability-package.zip -d "$TEMP_DIR"

cd "$TEMP_DIR"
```

#### 2. Build Validation Container

```bash
cd .claude/silicon-wisdom-protocols/docker-templates/
docker build -t silicon-wisdom-validator:latest -f Dockerfile.validation .
```

#### 3. Verify Structure

```bash
cd "$TEMP_DIR"/{capability-name}/

# Check required files
ls -la README.md ARCHITECTURE.md src/ tests/
```

#### 4. Install Dependencies

```bash
# Python
docker run --rm -v "$PWD:/workspace/capability:ro" \
  silicon-wisdom-validator:latest \
  sh -c "cd /workspace/capability && pip install -r requirements.txt"

# Node
docker run --rm -v "$PWD:/workspace/capability:ro" \
  silicon-wisdom-validator:latest \
  sh -c "cd /workspace/capability && npm install"
```

#### 5. Security Scan

```bash
# Search for secrets
grep -r -i "password\|api_key\|secret\|token" src/ --exclude="*.md"

# Python CVE scan
docker run --rm -v "$PWD:/workspace/capability:ro" \
  silicon-wisdom-validator:latest \
  safety check -r /workspace/capability/requirements.txt

# Node vulnerability scan
docker run --rm -v "$PWD:/workspace/capability:ro" \
  silicon-wisdom-validator:latest \
  sh -c "cd /workspace/capability && npm audit"
```

#### 6. Run Tests

```bash
# Python tests
docker run --rm -v "$PWD:/workspace/capability:ro" \
  silicon-wisdom-validator:latest \
  sh -c "cd /workspace/capability && pytest -v"

# Node tests
docker run --rm -v "$PWD:/workspace/capability:ro" \
  silicon-wisdom-validator:latest \
  sh -c "cd /workspace/capability && npm test"
```

#### 7. Manual Code Review

```bash
# Read architecture
cat ARCHITECTURE.md

# Review source code
find src/ -name "*.py" -o -name "*.js" | head -5 | xargs cat

# Check for patterns
grep -r "os.system\|subprocess.call\|eval\|exec" src/
```

---

## Security Isolation

### Container Security Features

**Isolation**:
- ✅ Read-only volume mounts (`:ro` flag)
- ✅ No network access during tests
- ✅ Non-root user (uid 1000)
- ✅ Temporary filesystem (`/tmp`)
- ✅ Resource limits (CPU, memory)

**What's Protected**:
- Host filesystem (read-only access to capability only)
- Network (no external connections)
- Other containers (complete isolation)

**What's Not Protected** (by design):
- CPU usage (capability can use 100% during tests)
- Memory up to container limit
- Temporary disk space

### Additional Hardening (Optional)

For high-risk capabilities, add extra isolation:

```bash
# Network isolation
docker run --rm --network=none -v "$PWD:/workspace/capability:ro" \
  silicon-wisdom-validator:latest pytest /workspace/capability/tests/

# Memory limit
docker run --rm --memory=2g -v "$PWD:/workspace/capability:ro" \
  silicon-wisdom-validator:latest pytest /workspace/capability/tests/

# CPU limit
docker run --rm --cpus=2 -v "$PWD:/workspace/capability:ro" \
  silicon-wisdom-validator:latest pytest /workspace/capability/tests/

# Read-only root filesystem
docker run --rm --read-only -v "$PWD:/workspace/capability:ro" \
  silicon-wisdom-validator:latest pytest /workspace/capability/tests/
```

---

## Customization

### Add Custom Dependencies

**Edit `Dockerfile.validation`** to add tools needed for specific capability types:

```dockerfile
# Add Go support
RUN apk add --no-cache go

# Add Rust support
RUN apk add --no-cache rust cargo

# Add specific Python library
RUN pip install --no-cache-dir pandas numpy scipy
```

**Rebuild after changes**:
```bash
docker build -t silicon-wisdom-validator:latest -f Dockerfile.validation .
```

### Custom Validation Steps

**Extend `validate.sh`** for capability-specific checks:

```bash
# Example: Add performance benchmarking
echo -e "\n${YELLOW}[Phase 8/8]${NC} Running performance benchmarks..."
docker run --rm \
    -v "$CAPABILITY_DIR:/workspace/capability:ro" \
    silicon-wisdom-validator:latest \
    sh -c "cd /workspace/capability && python -m pytest tests/benchmarks/ --benchmark-only"
```

---

## Troubleshooting

### Container Build Fails

**Problem**: `docker build` fails with permission error

**Solution**: Ensure Docker daemon running and user has permissions
```bash
sudo systemctl start docker
sudo usermod -aG docker $USER
# Log out and back in
```

### Dependency Installation Fails

**Problem**: `pip install` or `npm install` fails in container

**Solutions**:
- Check `requirements.txt` or `package.json` for invalid dependencies
- Try installing dependencies manually in container
- Check for platform-specific dependencies (Alpine Linux limitations)

### Tests Fail in Container But Pass Locally

**Problem**: Tests pass on sister CIV's machine but fail in validator

**Root Causes**:
- Environment differences (Alpine vs Ubuntu, Python 3.11 vs 3.9)
- Missing system dependencies
- Hardcoded paths that don't exist in container
- Network access required (blocked in container)

**Solutions**:
- Check test logs for specific errors
- Install missing system dependencies in Dockerfile
- Update tests to use relative paths
- Email sister CIV with findings (constructive feedback)

### Permission Denied Errors

**Problem**: Container can't write to mounted directory

**Solution**: Use `:ro` (read-only) mounts and write to `/workspace/test-results` instead
```bash
docker run --rm \
    -v "$PWD:/workspace/capability:ro" \
    -v "$PWD/results:/workspace/test-results:rw" \
    silicon-wisdom-validator:latest \
    sh -c "cd /workspace/capability && pytest --junit-xml=/workspace/test-results/results.xml"
```

---

## Integration with cross-civ-integrator

### Automated Usage

**cross-civ-integrator invokes `validate.sh` automatically**:

```python
import subprocess
from pathlib import Path

def validate_capability(package_path: Path) -> dict:
    """Run automated validation on capability package."""

    validate_script = Path(".claude/silicon-wisdom-protocols/docker-templates/validate.sh")

    result = subprocess.run(
        [str(validate_script), str(package_path)],
        capture_output=True,
        text=True
    )

    return {
        'exit_code': result.returncode,
        'stdout': result.stdout,
        'stderr': result.stderr,
        'success': result.returncode == 0
    }

# Usage in validation workflow
validation_result = validate_capability(Path("/tmp/memory-core-v2.tar.gz"))
if validation_result['success']:
    print("✅ Automated validation passed")
else:
    print("⚠️ Validation had issues - manual review required")
```

### Manual Review After Automation

Even with automated validation, **manual review is required**:

1. **Read validation report**: Check `/tmp/validation_*/VALIDATION-REPORT-*.md`
2. **Review code**: Look at actual source in `/tmp/validation_*/capability-name/src/`
3. **Test edge cases**: Run additional tests not covered by provided suite
4. **Create integration guide**: Document how other CIVs can adopt
5. **Report to submitter**: Send validation findings via email

**Philosophy**: Automation handles tedious checks, humans handle understanding.

---

## Version History

**v1.0** (2025-11-02):
- Initial Docker validation framework
- Automated 7-phase validation script
- Python + Node support
- Security scanning included

---

**END OF DOCKER VALIDATION FRAMEWORK**

*Owned by cross-civ-integrator (WEAVER/Team 1)*
