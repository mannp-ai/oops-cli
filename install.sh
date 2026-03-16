#!/bin/bash

# oops-cli Universal Installer
# ----------------------------
# This script installs oops-cli to ~/.oops-cli and adds the shell function.

set -e

REPO_URL="https://github.com/mannp-ai/oops-cli.git"
INSTALL_DIR="$HOME/.oops-cli"
VENV_DIR="$INSTALL_DIR/venv"

echo "📟 Starting oops-cli installation..."

# 1. Dependency Check
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed. Please install it and try again."
    exit 1
fi

# 2. Setup Directory
if [ -d "$INSTALL_DIR" ]; then
    echo "♻️  Updating existing installation in $INSTALL_DIR..."
    cd "$INSTALL_DIR"
    git pull origin main
else
    echo "📂 Cloning repository to $INSTALL_DIR..."
    git clone "$REPO_URL" "$INSTALL_DIR"
    cd "$INSTALL_DIR"
fi

# 3. Create Virtual Environment
echo "🐍 Setting up Python virtual environment..."
python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"

# 4. Install oops-cli
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -e .

# 5. Shell Integration
SHELL_RC=""
if [ -n "$ZSH_VERSION" ] || [ -f "$HOME/.zshrc" ]; then
    SHELL_RC="$HOME/.zshrc"
elif [ -n "$BASH_VERSION" ] || [ -f "$HOME/.bashrc" ]; then
    SHELL_RC="$HOME/.bashrc"
fi

if [ -n "$SHELL_RC" ]; then
    echo "🐚 Adding shell function to $SHELL_RC..."
    
    # Check if already exists
    if ! grep -q "oops()" "$SHELL_RC"; then
        cat << 'EOF' >> "$SHELL_RC"

# oops-cli integration
oops() {
    # Force history sync
    history -a
    history -r
    # Capture last command that wasn't 'oops'
    local last_cmd=$(history 1 | sed 's/^[ ]*[0-9]*[ ]*//')
    # Run the explainer using the dedicated venv
    ~/.oops-cli/venv/bin/python3 -m oops.cli "$last_cmd"
}
EOF
        echo "✅ Integration added! Please run 'source $SHELL_RC' to activate."
    else
        echo "ℹ️  oops() function already exists in $SHELL_RC. Skipping."
    fi
fi

echo "🚀 Installation complete! Try running 'oops' after restarting your shell."
