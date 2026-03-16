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
                # Read last line
                f.seek(0, os.SEEK_END)
                pos = f.tell() - 2
                while pos > 0:
                    f.seek(pos)
                    if f.read(1) == b"\n":
                        break
                    pos -= 1
                last_line = f.readline().decode("utf-8", errors="ignore").strip()
                
                # ZSH history format often has timestamps like ': 1710620000:0;command'
                if "zsh" in shell and ";" in last_line:
                    return last_line.split(";", 1)[1]
                return last_line
        except Exception:
            pass

    return "Unknown command"

def capture_stderr():
    """
    Attempts to capture stderr of the last command.
    In a real-world scenario, this might involve reading from journalctl
    or a temporary log file if a shell integration is active.
    For v0.1, we'll return a placeholder or try to read from common logs.
    """
    # Placeholder for now. Real implementation might look at journalctl -n 20
    try:
        result = subprocess.run(
            ["journalctl", "-n", "20", "--no-pager", "_COMM=" + get_last_command().split()[0]],
            capture_output=True, text=True
        )
        return result.stdout
    except Exception:
        return ""
