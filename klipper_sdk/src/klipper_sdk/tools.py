from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import subprocess
import os

class Tool(ABC):
    """Base class for all tools in the Klipper SDK."""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    def run(self, **kwargs) -> Any:
        pass

class ShellTool(Tool):
    """Tool to execute shell commands."""
    
    def __init__(self):
        super().__init__(
            name="shell_exec",
            description="Execute a shell command. Arguments: command (str), cwd (optional str)"
        )

    def run(self, command: str, cwd: Optional[str] = None) -> str:
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                cwd=cwd, 
                capture_output=True, 
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            return f"Error executing command: {e.stderr}"

class FileReadTool(Tool):
    """Tool to read file contents."""
    
    def __init__(self):
        super().__init__(
            name="read_file",
            description="Read content of a file. Arguments: path (str)"
        )

    def run(self, path: str) -> str:
        try:
            with open(path, 'r') as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {e}"

class FileWriteTool(Tool):
    """Tool to write to a file."""
    
    def __init__(self):
        super().__init__(
            name="write_file",
            description="Write content to a file. Arguments: path (str), content (str)"
        )

    def run(self, path: str, content: str) -> str:
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w') as f:
                f.write(content)
            return f"Successfully wrote to {path}"
        except Exception as e:
            return f"Error writing file: {e}"

class ToolRegistry:
    """Registry to manage available tools."""
    
    def __init__(self):
        self._tools: Dict[str, Tool] = {}
        # Register default tools
        self.register(ShellTool())
        self.register(FileReadTool())
        self.register(FileWriteTool())

    def register(self, tool: Tool):
        self._tools[tool.name] = tool

    def get_tool(self, name: str) -> Optional[Tool]:
        return self._tools.get(name)

    def list_tools(self) -> List[str]:
        return [f"{t.name}: {t.description}" for t in self._tools.values()]
