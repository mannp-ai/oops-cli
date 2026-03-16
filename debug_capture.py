from oops.capture import get_last_command, capture_stderr
import sys

print(f"DEBUG: Last Command: '{get_last_command()}'")
print(f"DEBUG: Captured Stderr:\n{capture_stderr()}")
