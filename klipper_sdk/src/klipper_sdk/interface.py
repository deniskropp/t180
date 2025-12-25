import re
from typing import Dict, Optional

class SpaceInterface:
    """
    Gen 10: The Transcendent Layer (Unity).
    Handles the 'Space' format for meta-communication across the system.
    Format: ⫻{name}/{type}:{place}/{index}
    """
    
    SPACE_PATTERN = re.compile(r"^⫻([a-z0-9_-]+)(?:/([a-z0-9_-]+))?(?::([a-z0-9_-]+))?(?:/([a-z0-9_-]+))?$", re.MULTILINE)

    def parse_section(self, text: str) -> Dict[str, str]:
        """
        Parses a Space format section header.
        Example: ⫻content/meta-summary:cell/0
        """
        lines = text.strip().split('\n')
        header = lines[0]
        match = self.SPACE_PATTERN.match(header)
        
        if not match:
            return {"error": "Invalid Space Header"}
            
        return {
            "name": match.group(1),
            "type": match.group(2),
            "place": match.group(3),
            "index": match.group(4),
            "content": "\n".join(lines[1:])
        }
        
    def generate_section(self, name: str, content: str, type_: str = None, place: str = None, index: str = None) -> str:
        """Generates a Space format block."""
        header = f"⫻{name}"
        if type_:
            header += f"/{type_}"
        if place:
            header += f":{place}"
        if index:
            header += f"/{index}"
            
        return f"{header}\n{content}"

if __name__ == "__main__":
    # Self-test
    si = SpaceInterface()
    sample = "⫻content/meta-summary:cell/0\nThis is a summary."
    parsed = si.parse_section(sample)
    print(f"Parsed: {parsed}")
    
    generated = si.generate_section("const", '{"key":"val"}', "json", "main")
    print(f"Generated:\n{generated}")
