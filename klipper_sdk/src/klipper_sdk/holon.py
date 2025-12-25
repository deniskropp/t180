from typing import Any, Dict, List, Optional
from .agents import Agent

class Holon(Agent):
    """
    Gen 6: The Holonic Layer.
    
    A Holon is a recursive structure that acts as both a whole (an Agent)
    and a part (containing an Orchestrator).
    """
    def __init__(self, name: str, role: str = "Holonic Unit", goal: str = "Recursion", prompt_template: str = "", blueprint_path: Optional[str] = None):
        super().__init__(name=name, role=role, goal=goal, prompt_template=prompt_template)
        
        # Internally, it possesses an Orchestrator
        # Lazy import to avoid circular dependency
        from .orchestrator import Orchestrator
        self.internal_orchestrator = Orchestrator()
        self.blueprint_path = blueprint_path
        
        if self.blueprint_path:
            self.internal_orchestrator.load_blueprint(self.blueprint_path)

    def execute(self, context: Dict[str, Any], tools: List[Any] = None) -> Any:
        """
        Executes the Holon's function. Instead of just LLM generation,
        it runs an entire internal orchestration loop.
        """
        print(f"[{self.name}] Activating Holonic State... Spawning internal orchestration.")
        
        # Pass the outer context to the inner orchestrator
        # The internal orchestrator expects a dictionary context
        internal_context = context.copy() if context else {}
        
        # Execute the internal blueprint
        results = self.internal_orchestrator.execute(dynamic_context=internal_context)
        
        # Synthesize the results back into a single string response
        summary = f"Holon {self.name} completed sub-workflow. Results: {results}"
        return summary

    def set_blueprint(self, blueprint_text: str):
        """Allows dynamic setting of the internal logic"""
        self.internal_orchestrator.parse_blueprint(blueprint_text)
