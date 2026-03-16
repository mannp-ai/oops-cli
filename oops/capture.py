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
    Attempts to capture stderr of last command using journalctl with strict time limit.
    """
    # Priority 1: Environment variable override
    env_stderr = os.environ.get("OOPS_STDERR", "")
    if env_stderr:
        return env_stderr

    # Priority 2: Precise journalctl lookup (last 10 seconds only)
    try:
        # We look for the last 10 seconds of logs to ensure relevance
        result = subprocess.run(
            ["journalctl", "--since", "10 seconds ago", "-n", "20", "--no-pager"],
            capture_output=True, text=True, check=False
        )
        return result.stdout
    except Exception:
        return ""
