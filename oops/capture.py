import os
import subprocess

def get_last_command():
    """Attempts to get the last command from shell history."""
    shell = os.environ.get("SHELL", "")
    history_file = ""
    
    if "zsh" in shell:
        history_file = os.path.expanduser("~/.zsh_history")
    elif "bash" in shell:
        history_file = os.path.expanduser("~/.bash_history")
    
    if history_file and os.path.exists(history_file):
        try:
            with open(history_file, "rb") as f:
                lines = f.readlines()
                for line in reversed(lines):
                    cmd = line.decode("utf-8", errors="ignore").strip()
                    if "zsh" in shell and ";" in cmd:
                        cmd = cmd.split(";", 1)[1]
                    
                    # Ignore meta-commands that pollute history
                    if any(cmd.startswith(x) for x in ["oops", "source", "alias", "export"]):
                        continue
                    return cmd
        except Exception:
            pass

    return "Unknown command"

def capture_stderr():
    """
    Attempts to capture stderr of the last command.
    In v0.1, we primarily rely on the OOPS_STDERR environment variable
    passed by the shell alias, or manual input.
    """
    return os.environ.get("OOPS_STDERR", "")
