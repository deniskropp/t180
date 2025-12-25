import sys
import os

# Add src to path so we can import klipper_sdk
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from klipper_sdk.orchestrator import Orchestrator

def main():
    print(">>> Initializing Klipper SDK Orchestration System (Gen 5) <<<")
    
    # 1. Initialize Orchestrator
    orchestrator = Orchestrator()
    
    # 2. Load Blueprint
    blueprint_path = os.path.join(os.path.dirname(__file__), 'klipper_sdk_orchestration.kl')
    if not os.path.exists(blueprint_path):
        print(f"Error: Blueprint file not found at {blueprint_path}")
        return

    orchestrator.load_blueprint(blueprint_path)
    
    # 3. Define Context (Simulation of Clipboard Data)
    # This represents 'Gen 1 & 2' data feeding into the system
    initial_context = {
        "entries": [
            {"text": "def hello_world(): print('hello')"},  # Should be identified as python_code
            {"text": "SELECT * FROM users WHERE id = 1"},    # Should be identified as sql_query
            {"text": "https://google.com"},                  # Should be identified as url
            {"text": "import React from 'react';"},          # Should be identified as frontend_code
        ]
    }
    
    print("\n>>> Input Context (Clipboard Entries):")
    for entry in initial_context['entries']:
        print(f" - {entry['text']}")
        
    # 4. Execute Workflow
    print("\n>>> Executing Workflow...")
    final_state = orchestrator.execute(initial_context)
    
    # 5. Report Results
    print("\n>>> Workflow Execution Complete.")
    print("Analysis Results (Gen 3 Tool Output):")
    print(final_state.get('analysis_results'))
    
    print("\nPredicted Workflow (Gen 4 Agent -> Gen 5 Decision):")
    prediction = final_state.get('prediction')
    if prediction:
        print(f"Workflow: {prediction['name']}")
        print(f"Confidence: {prediction['confidence']}")
        print(f"Reasoning: {prediction['reasoning']}")
    else:
        print("No prediction made.")

if __name__ == "__main__":
    main()
