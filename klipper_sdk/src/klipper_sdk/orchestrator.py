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
            is_holon = config.get('type') == 'holon' or 'blueprint_path' in config
            
            if is_holon:
                from .holon import Holon
                agent = Holon(
                    name=config['name'],
                    role=config.get('role', 'Holon'),
                    goal=config.get('goal', 'Execute sub-workflow'),
                    prompt_template=config.get('prompt_engineering', ''),
                    blueprint_path=config.get('blueprint_path')
                )
                print(f"  - Registered HOLON: {agent.name}")
            else:
                agent = Agent(
                    name=config['name'],
                    role=config.get('role', 'Generalist'),
                    goal=config.get('goal', ''),
                    prompt_template=config.get('prompt_engineering', '')
                )
                print(f"  - Registered agent: {agent.name} ({agent.role})")
            
            self.agent_registry.register(agent)

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
            print(f"  > Step: {step['name']}")
            agent_name = step.get('agent')
            tool_name = step.get('tool')
            
            if not agent_name:
                continue
                
            agent = self.agent_registry.get_agent(agent_name)
            tool = self.tool_registry.get_tool(tool_name) if tool_name else None
            
            # Resolve Inputs
            inputs_config = step.get('inputs', [])
            context = {}
            
            if isinstance(inputs_config, list):
                # Direct mapping: arg name = state key
                for key in inputs_config:
                    context[key] = self.workflow_state.get(key)
            elif isinstance(inputs_config, dict):
                # Remapping: arg name = inputs_config[arg name] -> value from state
                for arg_name, state_key in inputs_config.items():
                    context[arg_name] = self.workflow_state.get(state_key)
            
            # Execute Agent
            # The Agent will use the tool if provided, passing 'context' as args.
            result = agent.execute(context, tools=[tool] if tool else None)
            
            # Store Outputs
            output_key = step.get('outputs')
            if output_key:
                self.workflow_state[output_key] = result
                # Optional: specific logging
                # if isinstance(result, list):
                #     print(f"    [{agent.role}] Produced {len(result)} items for '{output_key}'.")
                # else:
                #     print(f"    [{agent.role}] Produced result for '{output_key}'.")
