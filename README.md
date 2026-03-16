# oops-cli

A sophisticated terminal error explainer for Linux. `oops` captures the context of failed commands and provides clear, actionable explanations and solutions through a specialized Terminal User Interface (TUI).

[![PyPI version](https://img.shields.io/pypi/v/oops-cli.svg)](https://pypi.org/project/oops-cli/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## Overview

Terminal errors are often cryptic and overwhelming. `oops` bridges the gap by analyzing `stderr` and command history to provide:
- **Concise Explanations**: What went wrong in plain English.
- **Root Cause Analysis**: Why the error occurred based on system context.
- **Immediate Fixes**: Actionable commands to resolve the issue.
- **Path Awareness**: Verification of file paths mentioned in error messages.

## Features

- **Extensive Pattern Library**: Built-in support for 35+ common Linux error categories including Git, Docker, SSH, Networking, and Package Managers.
- **Integrated TUI**: A responsive interface built with Textual, featuring system telemetry and interactive theme switching.
- **Efficient Workflow**: One-key copying of fix commands to the system clipboard.
- **Retro Aesthetic**: High-contrast themes including Matrix (Green), Amber (CRT), Classic (IBM), and Cyberpunk (Neon).

## Installation

### 1. Install via pip

```bash
pip install oops-cli
```

### 2. System Dependencies

`oops` requires a clipboard utility for the "copy fix" feature:

- **Debian/Ubuntu**: `sudo apt install xclip`
- **Fedora/RHEL**: `sudo dnf install xclip`
- **Arch Linux**: `sudo pacman -S xclip`

## Configuration

To use `oops` effectively on a daily basis, add the following function to your shell configuration (`~/.bashrc` or `~/.zshrc`):

```bash
oops() {
    # Get the last executed command directly from the session's history
    local last_cmd=$(history 1 | sed 's/^[ ]*[0-9]*[ ]*//')
    python3 -m oops.cli "$last_cmd"
}
```

After restarting your shell, simply type `oops` whenever a command fails.

## Usage

When a command returns an error, execute `oops`:

```bash
$ git push origin main
error: failed to push some refs...
$ oops
```

### Keyboard Shortcuts

| Key | Description |
|-----|-------------|
| `C` | Copy suggested fix to clipboard |
| `T` | Cycle through display themes |
| `Q` | Quit the application |

## Architecture

`oops` is designed with modularity in mind:
- **Capture Engine**: Retrieves command history and diagnostic logs.
- **Matching Engine**: Uses prioritized regex matching to identify specific error signatures.
- **Aesthetic TUI**: A performant rendering engine with zero-lag theme transitions.

## Contributing

Specific error patterns are defined in `oops/patterns/core.json`. Contributions for new patterns are welcome. Please ensure new patterns include:
- A unique `id`
- Robust `match` regexes
- Meaningful `what`, `why`, and `fix` sections

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
