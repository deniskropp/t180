from klipper_sdk.orchestrator import Orchestrator

# 1. Initialize Orchestrator
master = Orchestrator()

# 2. Load Main Blueprint
master.load_blueprint("holon_main.kl")

# 3. Context
context = {
    "initial_task": "Transform Data"
}

# 4. Execute
print("Starting Holon Demo...")
results = master.execute(context)
print("\nFinal Results:", results)
