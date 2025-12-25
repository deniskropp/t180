import sys
import os

# Add src to path so we can import klipper_sdk
sys.path.append(os.path.join(os.path.dirname(__file__), "klipper_sdk/src"))

from klipper_sdk.orchestrator import Orchestrator

def main():
    print("Beginning 5-Generation Klipper SDK Transformation...")
    
    blueprint_path = "klipper_sdk_orchestration.kl"
    
    if not os.path.exists(blueprint_path):
        print(f"Error: Blueprint {blueprint_path} not found.")
        return

    orch = Orchestrator()
    try:
        orch.load_blueprint(blueprint_path)
        orch.execute()
        print("\nSUCCESS: Orchestration completed successfully.")
    except Exception as e:
        print(f"\nFAILURE: Orchestration failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
