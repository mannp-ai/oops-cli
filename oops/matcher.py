import json
import re
import os

class Matcher:
    def __init__(self, patterns_file=None):
        if patterns_file is None:
            # Default path relative to this file
            base_path = os.path.dirname(__file__)
            patterns_file = os.path.join(base_path, "patterns", "core.json")
        
        self.patterns = []
        if os.path.exists(patterns_file):
            with open(patterns_file, "r") as f:
                data = json.load(f)
                self.patterns = data.get("patterns", [])

    def match(self, command, stderr):
        """Matches a command and its stderr against the pattern library."""
        # Smart Path Awareness: Look for potential file paths in stderr
        path_matches = re.findall(r'(/[a-zA-Z0-9._/-]+)', stderr)
        missing_paths = [p for p in path_matches if not os.path.exists(p) and '/' in p]

        combined_context = f"{command}\n{stderr}"

        # First pass: try matching only against stderr for cleaner results
        for p in self.patterns:
            for regex in p.get("match", []):
                # We prioritize stderr matching to avoid pollution from command history
                if re.search(regex, stderr, re.IGNORECASE):
                    return self._build_result(p, command, missing_paths)

        # Second pass: fallback to combined context if no specific stderr match found
        for p in self.patterns:
            for regex in p.get("match", []):
                if re.search(regex, combined_context, re.IGNORECASE):
                    return self._build_result(p, command, missing_paths)
        
        # Third pass: Universal Fallback if no specific pattern matched
        # but we have some error output or command context.
        if stderr.strip() or (command and command != "Unknown command"):
             return self._build_generic_result(command, stderr, missing_paths)

        return None

    def _build_generic_result(self, command, stderr, missing_paths):
        # We try to clean up the command for a better search link
        search_query = command.split()[0] if command else "linux+command"
        
        result = {
            "id": "generic-error",
            "command": command,
            "what": "An unrecognized error occurred.",
            "why": "The command returned a non-zero exit status or error output that doesn't match our known patterns.",
            "fix": f"Google Search: 'linux {search_query} error'",
            "learn": "Try running the command with '--help' or checking the 'man' pages for usage details."
        }
        
        if missing_paths:
             result["why"] += f"\nNote: The path '{missing_paths[0]}' was not found."
             
        return result

    def _build_result(self, p, command, missing_paths):
        result = {
            "id": p["id"],
            "command": command,
            "what": p["what"],
            "why": p["why"],
            "fix": p["fix"].get("default", ""),
            "learn": p["learn"]
        }
        
        # If we found missing paths and this is a file-related error
        if missing_paths and any(tag in p.get("tags", []) for tag in ["file", "disk", "path"]):
            result["why"] += f"\nNote: The path '{missing_paths[0]}' does not seem to exist."
        
        return result
