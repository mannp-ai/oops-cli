import sys
from .capture import get_last_command, capture_stderr
from .matcher import Matcher
from .tui import OopsTUI

def main():
    try:
        matcher = Matcher()
        
        command = get_last_command()
        stderr = capture_stderr()
        
        # If the user passed arguments, prioritize them
        if len(sys.argv) > 1:
            stderr = " ".join(sys.argv[1:])
        
        # If command is 'oops' itself, it's a recursive call or stale history
        if command.strip().startswith("oops"):
             # Fallback: try to see if we can get the error string from stdin/args
             pass

        match_result = matcher.match(command, stderr)
        
        if match_result:
            app = OopsTUI(match_result)
            app.run()
        else:
            print(f"oops: No match found for '{command}'.")
            print("Try searching: https://www.google.com/search?q=" + command.replace(" ", "+") + "+error")
    except KeyboardInterrupt:
        print("\n[oops] Explainer stopped.")
        sys.exit(0)

if __name__ == "__main__":
    main()
