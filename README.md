# oops — Linux Error Explainer (Retro CRT Edition) 🚀

`oops` is a premium, nerdy terminal explainer that turns cryptic Linux errors into plain English. Built with a retro CRT aesthetic, it captures your last failed command and tells you **What** went wrong, **Why**, and **How** to fix it instantly.

![Aesthetic](https://img.shields.io/badge/Aesthetic-CRT_Retro-00ff41?style=for-the-badge&logo=linux)
![License](https://img.shields.io/badge/License-MIT-white?style=for-the-badge)

## 📺 Retro Aesthetics 2.0
- **Matrix / Amber / Classic / Cyberpunk**: Press **'T'** to switch between 4 classic tube themes.
- **Hacker Boot Animation**: Fast-scroll loading sequence simulating kernel log scanning.
- **Compact Technical Headers**: Box-drawing characters for that 80s server look.
- **System Telemetry**: Real-time CPU, RAM, and Kernel status tracking.

## 🛠 Features
- **30+ Error Patterns**: Intelligent matching for Git, Docker, SSH, Networking, Pip, Apt, and more.
- **Smart Path Awareness**: Automatically detects and verifies if file paths in errors actually exist.
- **Instant Fix Copy**: Press **'C'** to copy the suggested fix directly to your clipboard.
- **Performance Optimized**: Zero-lag theme switching and lightweight resource footprint.

## 🚀 Daily Usage (Installation)

### 1. Install via Pip
```bash
python3 -m pip install .
```

### 2. System Dependencies
Required for the clipboard functionality:
- **Ubuntu/Debian**: `sudo apt install xclip`
- **Fedora**: `sudo dnf install xclip`

### 3. Shell Integration (The "Pro" Way)
To use `oops` seamlessly on a daily basis, add the following function to your `~/.bashrc` or `~/.zshrc`:

```bash
# Put this in your .bashrc or .zshrc
oops() {
    # This function captures the output of the last command and passes it to oops
    # For now, it simply runs the oops explainer on the last history entry
    local last_cmd=$(fc -ln -1)
    python3 -m oops.cli "$last_cmd"
}
```

After adding this, you can simply type `oops` whenever a command fails!

## ⌨️ TUI Shortcuts
| Key | Action |
|-----|--------|
| `C` | Copy Fix Command |
| `T` | Cycle Retro Themes |
| `Q` | Quit Explainer |

## 📖 Pattern Library
The tool matches against a comprehensive library in `oops/patterns/core.json`. You can easily add your own patterns by following the JSON structure.

## ⚖️ License
MIT - Created with 💚 for the Linux community.
