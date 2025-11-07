#!/bin/bash
# Silicon Wisdom - Capability Validation Script
# Usage: ./validate.sh /path/to/capability-package.tar.gz

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
VALIDATION_ID="validation_${TIMESTAMP}"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Silicon Wisdom - Capability Validator"
echo "Validation ID: ${VALIDATION_ID}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo

# Check arguments
if [ $# -ne 1 ]; then
    echo -e "${RED}Error: Missing capability package${NC}"
    echo "Usage: $0 /path/to/capability-package.tar.gz"
    exit 1
fi

PACKAGE_PATH="$1"

# Verify package exists
if [ ! -f "$PACKAGE_PATH" ]; then
    echo -e "${RED}Error: Package not found: ${PACKAGE_PATH}${NC}"
    exit 1
fi

# Create temporary validation workspace
TEMP_DIR="/tmp/${VALIDATION_ID}"
mkdir -p "$TEMP_DIR"
echo -e "${GREEN}✓${NC} Created validation workspace: ${TEMP_DIR}"

# Extract package
echo -e "\n${YELLOW}[Phase 1/7]${NC} Extracting package..."
if [[ "$PACKAGE_PATH" == *.tar.gz ]] || [[ "$PACKAGE_PATH" == *.tgz ]]; then
    tar -xzf "$PACKAGE_PATH" -C "$TEMP_DIR"
elif [[ "$PACKAGE_PATH" == *.zip ]]; then
    unzip -q "$PACKAGE_PATH" -d "$TEMP_DIR"
else
    echo -e "${RED}Error: Unsupported package format (use .tar.gz or .zip)${NC}"
    exit 1
fi
echo -e "${GREEN}✓${NC} Package extracted"

# Find capability directory (should be single top-level dir)
CAPABILITY_DIR=$(find "$TEMP_DIR" -mindepth 1 -maxdepth 1 -type d | head -n 1)
if [ -z "$CAPABILITY_DIR" ]; then
    echo -e "${RED}Error: No directory found in package${NC}"
    exit 1
fi
CAPABILITY_NAME=$(basename "$CAPABILITY_DIR")
echo -e "${GREEN}✓${NC} Capability: ${CAPABILITY_NAME}"

# Verify required files
echo -e "\n${YELLOW}[Phase 2/7]${NC} Verifying package structure..."
REQUIRED_FILES=("README.md" "ARCHITECTURE.md")
MISSING_FILES=()

for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$CAPABILITY_DIR/$file" ]; then
        MISSING_FILES+=("$file")
    fi
done

if [ ${#MISSING_FILES[@]} -gt 0 ]; then
    echo -e "${RED}Error: Missing required files:${NC}"
    printf ' - %s\n' "${MISSING_FILES[@]}"
    exit 1
fi
echo -e "${GREEN}✓${NC} Required files present"

# Build validation container
echo -e "\n${YELLOW}[Phase 3/7]${NC} Building validation container..."
docker build -t silicon-wisdom-validator:latest -f "$SCRIPT_DIR/Dockerfile.validation" "$SCRIPT_DIR" || {
    echo -e "${RED}Error: Failed to build Docker container${NC}"
    exit 1
}
echo -e "${GREEN}✓${NC} Validation container built"

# Install dependencies
echo -e "\n${YELLOW}[Phase 4/7]${NC} Installing dependencies..."
if [ -f "$CAPABILITY_DIR/requirements.txt" ]; then
    echo "  Installing Python dependencies..."
    docker run --rm \
        -v "$CAPABILITY_DIR:/workspace/capability:ro" \
        silicon-wisdom-validator:latest \
        sh -c "cd /workspace/capability && pip install -q -r requirements.txt && echo 'Python dependencies installed'" || {
        echo -e "${YELLOW}⚠${NC} Some Python dependencies failed (non-fatal)"
    }
fi

if [ -f "$CAPABILITY_DIR/package.json" ]; then
    echo "  Installing Node dependencies..."
    docker run --rm \
        -v "$CAPABILITY_DIR:/workspace/capability:ro" \
        silicon-wisdom-validator:latest \
        sh -c "cd /workspace/capability && npm install --quiet && echo 'Node dependencies installed'" || {
        echo -e "${YELLOW}⚠${NC} Some Node dependencies failed (non-fatal)"
    }
fi
echo -e "${GREEN}✓${NC} Dependencies installed"

# Security scan
echo -e "\n${YELLOW}[Phase 5/7]${NC} Running security scan..."
echo "  Scanning for secrets..."
SECRETS_FOUND=$(grep -r -i "password\|api_key\|secret\|token" "$CAPABILITY_DIR" --exclude="*.md" --exclude-dir=".git" || true)
if [ -n "$SECRETS_FOUND" ]; then
    echo -e "${RED}⚠ Potential secrets found:${NC}"
    echo "$SECRETS_FOUND"
    echo -e "${YELLOW}Review these manually${NC}"
else
    echo -e "${GREEN}✓${NC} No obvious secrets found"
fi

if [ -f "$CAPABILITY_DIR/requirements.txt" ]; then
    echo "  Checking Python dependencies for CVEs..."
    docker run --rm \
        -v "$CAPABILITY_DIR:/workspace/capability:ro" \
        silicon-wisdom-validator:latest \
        sh -c "safety check -r /workspace/capability/requirements.txt" || {
        echo -e "${YELLOW}⚠${NC} Vulnerabilities found (see above)"
    }
fi

if [ -f "$CAPABILITY_DIR/package.json" ]; then
    echo "  Checking Node dependencies for vulnerabilities..."
    docker run --rm \
        -v "$CAPABILITY_DIR:/workspace/capability:ro" \
        silicon-wisdom-validator:latest \
        sh -c "cd /workspace/capability && npm audit" || {
        echo -e "${YELLOW}⚠${NC} Vulnerabilities found (see above)"
    }
fi
echo -e "${GREEN}✓${NC} Security scan complete"

# Run tests
echo -e "\n${YELLOW}[Phase 6/7]${NC} Running test suite..."
TEST_PASSED=false

if [ -d "$CAPABILITY_DIR/tests" ] || [ -d "$CAPABILITY_DIR/src/tests" ]; then
    echo "  Running tests in isolated container..."
    docker run --rm \
        -v "$CAPABILITY_DIR:/workspace/capability:ro" \
        silicon-wisdom-validator:latest \
        sh -c "cd /workspace/capability && pytest -v --tb=short" && TEST_PASSED=true || {
        echo -e "${YELLOW}⚠${NC} Some tests failed (see above)"
    }
else
    echo -e "${YELLOW}⚠${NC} No test directory found"
fi

if [ "$TEST_PASSED" = true ]; then
    echo -e "${GREEN}✓${NC} Tests passed"
else
    echo -e "${YELLOW}⚠${NC} Tests had issues (review required)"
fi

# Generate validation report
echo -e "\n${YELLOW}[Phase 7/7]${NC} Generating validation report..."
REPORT_FILE="${TEMP_DIR}/VALIDATION-REPORT-${VALIDATION_ID}.md"

cat > "$REPORT_FILE" << EOF
# Validation Report: ${CAPABILITY_NAME}

**Validation ID**: ${VALIDATION_ID}
**Date**: $(date +%Y-%m-%d)
**Validator**: cross-civ-integrator (WEAVER/Team 1)

---

## Package Information

**Package**: $(basename "$PACKAGE_PATH")
**Extracted to**: ${TEMP_DIR}
**Capability Name**: ${CAPABILITY_NAME}

---

## Structure Verification

**Required files**:
- [x] README.md
- [x] ARCHITECTURE.md

**Optional files**:
EOF

[ -f "$CAPABILITY_DIR/VALIDATION.md" ] && echo "- [x] VALIDATION.md" >> "$REPORT_FILE" || echo "- [ ] VALIDATION.md" >> "$REPORT_FILE"
[ -f "$CAPABILITY_DIR/LICENSE.md" ] && echo "- [x] LICENSE.md" >> "$REPORT_FILE" || echo "- [ ] LICENSE.md" >> "$REPORT_FILE"
[ -d "$CAPABILITY_DIR/tests" ] && echo "- [x] tests/" >> "$REPORT_FILE" || echo "- [ ] tests/" >> "$REPORT_FILE"

cat >> "$REPORT_FILE" << EOF

---

## Security Scan

**Secrets Check**: $([ -z "$SECRETS_FOUND" ] && echo "✅ No obvious secrets" || echo "⚠️ Potential secrets found (review manually)")

**Dependency Vulnerabilities**: See detailed output above

---

## Test Results

**Tests Found**: $([ -d "$CAPABILITY_DIR/tests" ] && echo "Yes" || echo "No")
**Tests Passed**: $([ "$TEST_PASSED" = true ] && echo "✅ Yes" || echo "⚠️ Some failures")

---

## Next Steps

1. **Manual Review**: Read README.md and ARCHITECTURE.md thoroughly
2. **Code Review**: Examine source code in src/
3. **Integration Planning**: Determine adaptation needed for WEAVER
4. **Integration Guide**: Create step-by-step integration instructions
5. **Publishing**: Add to silicon-wisdom repository with attribution

---

## Validation Artifacts

**Workspace**: ${TEMP_DIR}
**Report**: ${REPORT_FILE}

**To clean up**:
\`\`\`bash
rm -rf ${TEMP_DIR}
\`\`\`

---

**Automated validation complete**. Manual review required before publishing.

EOF

echo -e "${GREEN}✓${NC} Validation report generated: ${REPORT_FILE}"

# Summary
echo
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Validation Complete: ${CAPABILITY_NAME}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo
echo "Validation ID: ${VALIDATION_ID}"
echo "Workspace: ${TEMP_DIR}"
echo "Report: ${REPORT_FILE}"
echo
echo -e "${YELLOW}Next Steps:${NC}"
echo "1. Review full report: cat ${REPORT_FILE}"
echo "2. Manual code review: cd ${CAPABILITY_DIR}"
echo "3. Create integration guide"
echo "4. Publish to silicon-wisdom"
echo
echo -e "${GREEN}To clean up:${NC} rm -rf ${TEMP_DIR}"
echo
