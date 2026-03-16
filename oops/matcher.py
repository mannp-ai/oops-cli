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
        
        return None

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
