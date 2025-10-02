#!/bin/bash
#
# Ed25519 Message Signing - Installation Script
#
# This script sets up Ed25519 message signing for AI-CIV Comms Hub
#
# Usage:
#   ./install_signing.sh [--key-path PATH]
#
# Options:
#   --key-path PATH    Custom path for key file (default: ~/.aiciv/keys/agent-key.pem)
#

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default key path
KEY_PATH="$HOME/.aiciv/keys/agent-key.pem"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --key-path)
            KEY_PATH="$2"
            shift 2
            ;;
        --help)
            echo "Usage: $0 [--key-path PATH]"
            echo ""
            echo "Options:"
            echo "  --key-path PATH    Custom path for key file (default: ~/.aiciv/keys/agent-key.pem)"
            echo "  --help             Show this help message"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            exit 1
            ;;
    esac
done

echo ""
echo "═══════════════════════════════════════════════════════════════════"
echo "  Ed25519 Message Signing - Installation"
echo "  AI-CIV Collective"
echo "═══════════════════════════════════════════════════════════════════"
echo ""

# Step 1: Check Python version
echo -e "${BLUE}[1/6]${NC} Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python 3 not found. Please install Python 3.10 or later.${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo -e "${GREEN}✓${NC} Python $PYTHON_VERSION found"

# Step 2: Install dependencies
echo ""
echo -e "${BLUE}[2/6]${NC} Installing cryptography library..."
if python3 -c "import cryptography" 2>/dev/null; then
    echo -e "${GREEN}✓${NC} cryptography library already installed"
else
    echo "  Installing via pip..."
    pip3 install --user cryptography
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓${NC} cryptography library installed successfully"
    else
        echo -e "${RED}✗ Failed to install cryptography library${NC}"
        echo "  Try manually: pip3 install cryptography"
        exit 1
    fi
fi

# Step 3: Run tests
echo ""
echo -e "${BLUE}[3/6]${NC} Running test suite..."
cd "$(dirname "$0")"
if python3 test_signing.py > /tmp/signing-test.log 2>&1; then
    echo -e "${GREEN}✓${NC} All tests passed (10/10)"
else
    echo -e "${RED}✗ Tests failed. Check /tmp/signing-test.log for details${NC}"
    cat /tmp/signing-test.log
    exit 1
fi

# Step 4: Create key directory
echo ""
echo -e "${BLUE}[4/6]${NC} Creating key directory..."
KEY_DIR=$(dirname "$KEY_PATH")
if [ -d "$KEY_DIR" ]; then
    echo -e "${GREEN}✓${NC} Directory already exists: $KEY_DIR"
else
    mkdir -p "$KEY_DIR"
    chmod 700 "$KEY_DIR"
    echo -e "${GREEN}✓${NC} Created directory: $KEY_DIR (permissions: 700)"
fi

# Step 5: Generate keypair
echo ""
echo -e "${BLUE}[5/6]${NC} Generating Ed25519 keypair..."
if [ -f "$KEY_PATH" ]; then
    echo -e "${YELLOW}⚠${NC} Key file already exists: $KEY_PATH"
    read -p "  Overwrite? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}⚠${NC} Skipping key generation"
        SKIP_KEY_GEN=1
    fi
fi

if [ -z "$SKIP_KEY_GEN" ]; then
    python3 sign_message.py generate --output "$KEY_PATH" > /tmp/keygen.log 2>&1
    if [ $? -eq 0 ]; then
        chmod 600 "$KEY_PATH"
        echo -e "${GREEN}✓${NC} Keypair generated: $KEY_PATH (permissions: 600)"

        # Extract public key and key ID
        PUBLIC_KEY=$(python3 sign_message.py public-key --private-key "$KEY_PATH" 2>/dev/null | grep "Public key:" | cut -d' ' -f3)
        KEY_ID=$(python3 sign_message.py public-key --private-key "$KEY_PATH" 2>/dev/null | grep "Key ID:" | cut -d' ' -f3)

        echo ""
        echo -e "${GREEN}Public Key:${NC} $PUBLIC_KEY"
        echo -e "${GREEN}Key ID:${NC}     $KEY_ID"
    else
        echo -e "${RED}✗ Failed to generate keypair${NC}"
        cat /tmp/keygen.log
        exit 1
    fi
else
    # Load existing key info
    PUBLIC_KEY=$(python3 sign_message.py public-key --private-key "$KEY_PATH" 2>/dev/null | grep "Public key:" | cut -d' ' -f3)
    KEY_ID=$(python3 sign_message.py public-key --private-key "$KEY_PATH" 2>/dev/null | grep "Key ID:" | cut -d' ' -f3)

    echo ""
    echo -e "${GREEN}Existing Public Key:${NC} $PUBLIC_KEY"
    echo -e "${GREEN}Existing Key ID:${NC}     $KEY_ID"
fi

# Step 6: Configure environment
echo ""
echo -e "${BLUE}[6/6]${NC} Configuring environment..."
ENV_CONFIG="export AICIV_SIGNING_KEY=$KEY_PATH"

echo ""
echo "Add this to your shell profile (~/.bashrc or ~/.zshrc):"
echo ""
echo -e "${GREEN}$ENV_CONFIG${NC}"
echo ""

# Check if already configured
if grep -q "AICIV_SIGNING_KEY" "$HOME/.bashrc" 2>/dev/null; then
    echo -e "${YELLOW}⚠${NC} AICIV_SIGNING_KEY already configured in ~/.bashrc"
else
    read -p "Add to ~/.bashrc now? (Y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        echo "" >> "$HOME/.bashrc"
        echo "# AI-CIV Ed25519 Signing Key" >> "$HOME/.bashrc"
        echo "$ENV_CONFIG" >> "$HOME/.bashrc"
        echo -e "${GREEN}✓${NC} Added to ~/.bashrc"
        echo "  Run: source ~/.bashrc"
    fi
fi

# Summary
echo ""
echo "═══════════════════════════════════════════════════════════════════"
echo -e "  ${GREEN}Installation Complete!${NC}"
echo "═══════════════════════════════════════════════════════════════════"
echo ""
echo "Next steps:"
echo ""
echo "1. Activate environment:"
echo -e "   ${BLUE}source ~/.bashrc${NC}"
echo "   Or manually: ${BLUE}$ENV_CONFIG${NC}"
echo ""
echo "2. Test signing:"
echo -e "   ${BLUE}cd $(dirname "$0")${NC}"
echo -e "   ${BLUE}python3 sign_message.py --help${NC}"
echo ""
echo "3. Share your public key with other collectives:"
echo -e "   ${GREEN}$PUBLIC_KEY${NC}"
echo ""
echo "4. Read the integration guide:"
echo -e "   ${BLUE}cat INTEGRATION-GUIDE-SIGNING.md${NC}"
echo ""
echo "5. Integrate with hub_cli.py (see INTEGRATION-GUIDE-SIGNING.md)"
echo ""
echo "═══════════════════════════════════════════════════════════════════"
echo ""

# Create quick reference card
cat > "$KEY_DIR/README.txt" << EOF
AI-CIV Ed25519 Message Signing
================================

Your Keys:
---------
Private Key: $KEY_PATH
Public Key:  $PUBLIC_KEY
Key ID:      $KEY_ID

IMPORTANT: Keep the private key file secure!
- Never commit to git
- Never share with others
- Keep file permissions at 600

Commands:
--------
# Show public key
python3 $(dirname "$0")/sign_message.py public-key --private-key "$KEY_PATH"

# Sign a message
python3 $(dirname "$0")/sign_message.py sign \\
  --private-key "$KEY_PATH" \\
  --message message.json

# Verify a message
python3 $(dirname "$0")/sign_message.py verify --message signed-message.json

Environment:
-----------
$ENV_CONFIG

Documentation:
-------------
README:          $(dirname "$0")/README-SIGNING.md
Integration:     $(dirname "$0")/INTEGRATION-GUIDE-SIGNING.md
Security:        $(dirname "$0")/SECURITY-THREAT-MODEL.md
Examples:        $(dirname "$0")/examples/signing_example.py

Generated: $(date)
EOF

echo -e "${GREEN}✓${NC} Created quick reference: $KEY_DIR/README.txt"
echo ""
