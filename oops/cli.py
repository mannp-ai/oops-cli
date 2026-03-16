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
            print("\033[1;31m[oops] No solution found.\033[0m")
            print(f"I analyzed your last command: \033[1;32m{command}\033[0m")
            if stderr:
                snippet = (stderr[:100] + '...') if len(stderr) > 100 else stderr
                print(f"and the error output: \033[1;33m{snippet.strip()}\033[0m")
            
            print("\nIf this was a typo, try running with the error message directly:")
            print("  oops \"your error message here\"")
            print("\nOr search online: https://www.google.com/search?q=" + command.replace(" ", "+") + "+error")
    except KeyboardInterrupt:
        print("\n[oops] Explainer stopped.")
        sys.exit(0)

if __name__ == "__main__":
    main()
