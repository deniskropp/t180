import yaml
import time
from typing import Dict, Any, List
from .agents import Agent, AgentRegistry
from .tools import ToolRegistry
from .learning_tools import ContentAnalysisTool, WorkflowPredictionTool

class Orchestrator:
    """
    Gen 5 Orchestrator: capable of interpreting KickLang (.kl) blueprints
    and executing them using Gen 4 Agents and Gen 3 Tools.
    """
    
    def __init__(self):
        self.agent_registry = AgentRegistry()
        self.tool_registry = ToolRegistry()
        
        # Register Domain Tools (Gen 3)
        self.tool_registry.register(ContentAnalysisTool())
        self.tool_registry.register(WorkflowPredictionTool())
        
        self.execution_log: List[Dict[str, Any]] = []

    def load_blueprint(self, path: str):
        """Loads and parses a .kl file."""
        print(f"[Orchestrator] Loading blueprint from {path}...")
        with open(path, 'r') as f:
            # Skip the first line if it interacts poorly with yaml (e.g., ⫻kicklang:orchestration)
            content = f.read()
            if content.startswith("⫻"):
                content = content.split("\n", 1)[1]
            
            data = yaml.safe_load(content)
            if isinstance(data, list) and data:
                self.blueprint = data[0]
            elif isinstance(data, dict):
                self.blueprint = data
            else:
                raise ValueError("Invalid blueprint format")
            
        # Parse Planes
        self._setup_agents(self.blueprint.get('planes', {}).get('agentic', []))
        
    def _setup_agents(self, agent_configs: List[Dict[str, Any]]):
        """Initializes agents from the blueprint."""
        print(f"[Orchestrator] Setting up {len(agent_configs)} agents...")
        for config in agent_configs:
            agent = Agent(
                name=config['name'],
                role=config.get('role', 'Generalist'),
                goal=config.get('goal', ''),
                prompt_template=config.get('prompt_engineering', '')
            )
            self.agent_registry.register(agent)
            print(f"  - Registered agent: {agent.name} ({agent.role})")

    def execute(self, dynamic_context: Dict[str, Any] = None):
        """Executes the workflow defined in the structural plane."""
        print("[Orchestrator] Starting execution...")
        dynamic_context = dynamic_context or {}
        
        structural_plane = self.blueprint.get('planes', {}).get('structural', [])
        
        # Shared state across phases
        self.workflow_state = dynamic_context.copy()
        
        for phase in structural_plane:
            # print(f"\n>> Phase: {phase['name']} - {phase['description']}")
            self._execute_phase(phase)
            
        return self.workflow_state

    def _execute_phase(self, phase: Dict[str, Any]):
        steps = phase.get('steps', [])
        for step in steps:
            # print(f"  > Step: {step['name']}")
            agent_name = step.get('agent')
            tool_name = step.get('tool')
            
            if not agent_name:
                continue
                
            agent = self.agent_registry.get_agent(agent_name)
            
            # Special logic for this use case: 
            # If step is 'analyze_entries', we look for 'entries' in state and map the tool over them.
            # If step is 'predict_workflow', we use the 'types' from previous step.
            
            if step['name'] == 'analyze_entries':
                entries = self.workflow_state.get('entries', [])
                results = []
                tool = self.tool_registry.get_tool(tool_name) if tool_name else None
                
                # In a real agentic loop, the agent would decide to call the tool.
                # Here we simulate the agent "using" the tool on each item.
                for entry in entries:
                    txt = getattr(entry, 'text', '') or ''
                    res = tool.run(txt) if tool else "text"
                    results.append(res)
                
                self.workflow_state['analysis_results'] = results
                # print(f"    [Analyst] Analyzed {len(entries)} entries.")
                
            elif step['name'] == 'predict_workflow':
                types = self.workflow_state.get('analysis_results', [])
                entries = self.workflow_state.get('entries', [])
                texts = [getattr(e, 'text', '') for e in entries]
                
                tool = self.tool_registry.get_tool(tool_name) if tool_name else None
                
                if tool:
                    prediction = tool.run(types, texts)
                    self.workflow_state['prediction'] = prediction
                    # print(f"    [Predictor] Prediction: {prediction['name']}")
            
            else:
                # Fallback to generic agent execution
                pass
