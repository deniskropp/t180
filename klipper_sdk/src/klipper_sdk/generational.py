#!/usr/bin/env python3
"""
Generational Iteration Framework for Klipper SDK

This module implements a systematic approach to generational improvement,
allowing the system to evolve through iterative cycles while maintaining
version control, performance tracking, and automated testing.
"""

import os
import json
import time
import hashlib
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import yaml

class GenerationTracker:
    """
    Tracks the evolutionary state of the system across generations.
    
    This class maintains a record of:
    - Current generation for each component
    - Performance metrics across generations
    - Version history and changelogs
    - Component dependencies and relationships
    """
    
    def __init__(self, base_path: str = "generational_data"):
        self.base_path = base_path
        self.generations: Dict[str, Dict[str, Any]] = {}
        self.current_generation: Dict[str, int] = {}
        self.metrics_history: Dict[str, List[Dict[str, Any]]] = {}
        
        # Ensure data directory exists
        os.makedirs(self.base_path, exist_ok=True)
        
        # Load existing data
        self._load_generational_data()
    
    def _load_generational_data(self):
        """Load generational data from persistent storage."""
        try:
            # Load generations
            generations_file = os.path.join(self.base_path, "generations.json")
            if os.path.exists(generations_file):
                with open(generations_file, 'r') as f:
                    self.generations = json.load(f)
            
            # Load current generation state
            current_gen_file = os.path.join(self.base_path, "current_generation.json")
            if os.path.exists(current_gen_file):
                with open(current_gen_file, 'r') as f:
                    self.current_generation = json.load(f)
            
            # Load metrics history
            metrics_file = os.path.join(self.base_path, "metrics_history.json")
            if os.path.exists(metrics_file):
                with open(metrics_file, 'r') as f:
                    self.metrics_history = json.load(f)
                    
        except (FileNotFoundError, json.JSONDecodeError):
            # Initialize with default values if files don't exist or are corrupted
            self.generations = {}
            self.current_generation = {}
            self.metrics_history = {}
    
    def _save_generational_data(self):
        """Save generational data to persistent storage."""
        # Save generations
        with open(os.path.join(self.base_path, "generations.json"), 'w') as f:
            json.dump(self.generations, f, indent=2)
        
        # Save current generation state
        with open(os.path.join(self.base_path, "current_generation.json"), 'w') as f:
            json.dump(self.current_generation, f, indent=2)
        
        # Save metrics history
        with open(os.path.join(self.base_path, "metrics_history.json"), 'w') as f:
            json.dump(self.metrics_history, f, indent=2)
    
    def register_component(self, component_name: str, initial_generation: int = 1, 
                         description: str = "", dependencies: List[str] = None):
        """Register a new component in the generational tracking system."""
        if component_name in self.generations:
            return False  # Already registered
            
        self.generations[component_name] = {
            "generations": {},
            "current_generation": initial_generation,
            "description": description,
            "dependencies": dependencies or [],
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        }
        
        self.current_generation[component_name] = initial_generation
        self._save_generational_data()
        return True
    
    def advance_generation(self, component_name: str, changes: Dict[str, Any], 
                          metrics: Dict[str, Any] = None) -> bool:
        """Advance a component to the next generation with recorded changes and metrics."""
        if component_name not in self.generations:
            return False
            
        current_gen = self.current_generation[component_name]
        next_gen = current_gen + 1
        
        # Record the current generation's final state
        generation_data = {
            "version": current_gen,
            "changes": changes,
            "metrics": metrics or {},
            "timestamp": datetime.now().isoformat(),
            "checksum": self._calculate_checksum(changes)
        }
        
        # Store the generation data
        self.generations[component_name]["generations"][current_gen] = generation_data
        
        # Update to next generation
        self.generations[component_name]["current_generation"] = next_gen
        self.current_generation[component_name] = next_gen
        self.generations[component_name]["last_updated"] = datetime.now().isoformat()
        
        # Record metrics
        if metrics:
            if component_name not in self.metrics_history:
                self.metrics_history[component_name] = []
            
            metrics_record = {
                "generation": current_gen,
                "timestamp": datetime.now().isoformat(),
                **metrics
            }
            self.metrics_history[component_name].append(metrics_record)
        
        self._save_generational_data()
        return True
    
    def _calculate_checksum(self, data: Dict[str, Any]) -> str:
        """Calculate a checksum for the generation data."""
        data_str = json.dumps(data, sort_keys=True)
        return hashlib.md5(data_str.encode('utf-8')).hexdigest()
    
    def get_component_info(self, component_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific component."""
        return self.generations.get(component_name)
    
    def get_current_generation(self, component_name: str) -> Optional[int]:
        """Get the current generation of a component."""
        return self.current_generation.get(component_name)
    
    def get_generation_history(self, component_name: str) -> Optional[Dict[int, Dict[str, Any]]]:
        """Get the complete generation history of a component."""
        if component_name in self.generations:
            return self.generations[component_name]["generations"]
        return None
    
    def get_metrics_trend(self, component_name: str, metric_name: str) -> List[Tuple[int, Any]]:
        """Get the trend of a specific metric across generations."""
        trend = []
        if component_name in self.metrics_history:
            for record in self.metrics_history[component_name]:
                if metric_name in record:
                    trend.append((record["generation"], record[metric_name]))
        return trend
    
    def generate_report(self, component_name: str = None) -> Dict[str, Any]:
        """Generate a comprehensive report of generational progress."""
        report = {
            "timestamp": datetime.now().isoformat(),
            "components": {}
        }
        
        components_to_report = [component_name] if component_name else self.generations.keys()
        
        for comp_name in components_to_report:
            if comp_name in self.generations:
                comp_data = self.generations[comp_name]
                report["components"][comp_name] = {
                    "current_generation": comp_data["current_generation"],
                    "total_generations": len(comp_data["generations"]),
                    "description": comp_data["description"],
                    "dependencies": comp_data["dependencies"],
                    "created_at": comp_data["created_at"],
                    "last_updated": comp_data["last_updated"],
                    "generations": comp_data["generations"]
                }
                
                # Add metrics trend if available
                if comp_name in self.metrics_history:
                    report["components"][comp_name]["metrics_trend"] = self.metrics_history[comp_name]
        
        return report

class GenerationalImprovementLoop:
    """
    Implements the core generational improvement loop.
    
    This class orchestrates the iterative improvement process by:
    1. Running tests on current generation
    2. Analyzing performance metrics
    3. Identifying improvement opportunities
    4. Applying changes to create next generation
    5. Validating the new generation
    """
    
    def __init__(self, tracker: GenerationTracker):
        self.tracker = tracker
        self.test_results: Dict[str, Any] = {}
        self.improvement_opportunities: Dict[str, List[str]] = {}
    
    def run_improvement_cycle(self, component_name: str, 
                             test_function: callable, 
                             improvement_function: callable,
                             validation_function: callable) -> bool:
        """
        Execute a complete generational improvement cycle.
        
        Args:
            component_name: Name of the component to improve
            test_function: Function that tests the current generation and returns metrics
            improvement_function: Function that applies improvements based on test results
            validation_function: Function that validates the new generation
            
        Returns:
            bool: True if the cycle completed successfully, False otherwise
        """
        print(f"🔄 Starting generational improvement cycle for {component_name}")
        
        # Step 1: Test current generation
        print(f"🧪 Testing generation {self.tracker.get_current_generation(component_name)}...")
        test_results = test_function()
        self.test_results[component_name] = test_results
        
        # Step 2: Analyze results and identify improvements
        print(f"🔍 Analyzing test results...")
        improvements = improvement_function(test_results)
        self.improvement_opportunities[component_name] = improvements
        
        if not improvements:
            print(f"✅ No improvements needed for {component_name}")
            return True
            
        print(f"📋 Identified {len(improvements)} improvement opportunities:")
        for i, improvement in enumerate(improvements, 1):
            print(f"  {i}. {improvement}")
        
        # Step 3: Apply improvements to create next generation
        print(f"🛠️ Applying improvements...")
        changes = {
            "improvements_applied": improvements,
            "test_results": test_results,
            "timestamp": datetime.now().isoformat()
        }
        
        # Step 4: Advance to next generation
        success = self.tracker.advance_generation(
            component_name, 
            changes=changes,
            metrics=test_results.get("metrics", {})
        )
        
        if not success:
            print(f"❌ Failed to advance generation for {component_name}")
            return False
            
        # Step 5: Validate the new generation
        print(f"🔍 Validating new generation {self.tracker.get_current_generation(component_name)}...")
        validation_result = validation_function()
        
        if validation_result:
            print(f"✅ Successfully completed generational improvement cycle for {component_name}")
            print(f"   Advanced from generation {changes['test_results'].get('generation', 'unknown')} to {self.tracker.get_current_generation(component_name)}")
        else:
            print(f"❌ Validation failed for new generation of {component_name}")
            return False
            
        return True
    
    def run_batch_improvement(self, components: List[str], 
                             test_functions: Dict[str, callable],
                             improvement_functions: Dict[str, callable],
                             validation_functions: Dict[str, callable]) -> Dict[str, bool]:
        """
        Run improvement cycles for multiple components.
        
        Args:
            components: List of component names
            test_functions: Dictionary mapping component names to test functions
            improvement_functions: Dictionary mapping component names to improvement functions
            validation_functions: Dictionary mapping component names to validation functions
            
        Returns:
            Dictionary mapping component names to success status
        """
        results = {}
        
        for component in components:
            if (component in test_functions and 
                component in improvement_functions and 
                component in validation_functions):
                
                success = self.run_improvement_cycle(
                    component,
                    test_functions[component],
                    improvement_functions[component],
                    validation_functions[component]
                )
                results[component] = success
            else:
                print(f"⚠️  Missing functions for component {component}")
                results[component] = False
        
        return results

class GenerationalBlueprintManager:
    """
    Manages the evolution of KickLang blueprints across generations.
    
    This class handles:
    - Version control for blueprints
    - Generational diffing
    - Blueprint optimization
    - Dependency management across generations
    """
    
    def __init__(self, tracker: GenerationTracker, blueprints_dir: str = "blueprints"):
        self.tracker = tracker
        self.blueprints_dir = blueprints_dir
        os.makedirs(self.blueprints_dir, exist_ok=True)
    
    def register_blueprint(self, blueprint_name: str, content: str, 
                          initial_generation: int = 1, 
                          description: str = ""):
        """Register a new blueprint in the generational system."""
        # Register with tracker
        self.tracker.register_component(
            blueprint_name, 
            initial_generation=initial_generation,
            description=description or f"KickLang blueprint: {blueprint_name}"
        )
        
        # Save initial version
        self._save_blueprint_version(blueprint_name, initial_generation, content)
    
    def _save_blueprint_version(self, blueprint_name: str, generation: int, content: str):
        """Save a specific version of a blueprint."""
        # Create component directory if it doesn't exist
        component_dir = os.path.join(self.blueprints_dir, blueprint_name)
        os.makedirs(component_dir, exist_ok=True)
        
        # Save the blueprint file
        blueprint_file = os.path.join(component_dir, f"gen_{generation}.kl")
        with open(blueprint_file, 'w') as f:
            f.write(content)
        
        # Also save as YAML for easier parsing
        try:
            # Parse and re-serialize to ensure valid YAML
            if content.strip().startswith("⫻"):
                # Skip the first line for KickLang files
                yaml_content = content.split("\n", 1)[1] if "\n" in content else ""
            else:
                yaml_content = content
                
            parsed = yaml.safe_load(yaml_content)
            yaml_file = os.path.join(component_dir, f"gen_{generation}.yaml")
            with open(yaml_file, 'w') as f:
                yaml.dump(parsed, f, sort_keys=False)
        except yaml.YAMLError:
            pass  # Skip YAML serialization if parsing fails
    
    def evolve_blueprint(self, blueprint_name: str, new_content: str, 
                        changes: Dict[str, Any], metrics: Dict[str, Any] = None) -> bool:
        """Evolve a blueprint to the next generation."""
        current_gen = self.tracker.get_current_generation(blueprint_name)
        if current_gen is None:
            return False
            
        next_gen = current_gen + 1
        
        # Save the new version
        self._save_blueprint_version(blueprint_name, next_gen, new_content)
        
        # Advance generation in tracker
        success = self.tracker.advance_generation(
            blueprint_name,
            changes=changes,
            metrics=metrics
        )
        
        return success
    
    def get_blueprint_version(self, blueprint_name: str, generation: int) -> Optional[str]:
        """Get a specific version of a blueprint."""
        component_dir = os.path.join(self.blueprints_dir, blueprint_name)
        blueprint_file = os.path.join(component_dir, f"gen_{generation}.kl")
        
        if os.path.exists(blueprint_file):
            with open(blueprint_file, 'r') as f:
                return f.read()
        return None
    
    def get_latest_blueprint(self, blueprint_name: str) -> Optional[str]:
        """Get the latest version of a blueprint."""
        current_gen = self.tracker.get_current_generation(blueprint_name)
        if current_gen:
            return self.get_blueprint_version(blueprint_name, current_gen)
        return None
    
    def compare_generations(self, blueprint_name: str, gen1: int, gen2: int) -> Dict[str, Any]:
        """Compare two generations of a blueprint."""
        content1 = self.get_blueprint_version(blueprint_name, gen1)
        content2 = self.get_blueprint_version(blueprint_name, gen2)
        
        if not content1 or not content2:
            return {"error": "One or both generations not found"}
            
        # Simple line-based diff for now
        lines1 = content1.split('\n')
        lines2 = content2.split('\n')
        
        return {
            "blueprint": blueprint_name,
            "generation_1": gen1,
            "generation_2": gen2,
            "lines_added": len(lines2) - len(lines1),
            "content_length_diff": len(content2) - len(content1),
            "content_1_length": len(content1),
            "content_2_length": len(content2)
        }