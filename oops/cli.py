import sys
from .capture import get_last_command, capture_stderr
from .matcher import Matcher
from .tui import OopsTUI

def main():
    try:
        matcher = Matcher()
        
        # In a real use case, we might pass the error output directly if piped
        # or read from history.
        command = get_last_command()
        stderr = capture_stderr()
        
        # For testing/demo purposes, if no stderr found, we can try to use arguments
        if len(sys.argv) > 1:
            stderr = " ".join(sys.argv[1:])

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
