# Klipper SDK: The Meta-AI Orchestration Platform

> **Hyper View Manifest**: This document serves as the architectural blueprint for the Klipper SDK, tracking its evolution from a simple utility to a cognitive orchestration engine.

The **Klipper SDK** is a 5-Generation Python framework designed to bridge the gap between desktop data (starting with the clipboard) and autonomous AI agents. It orchestrates a "Meta-AI" workflow where agents don't just answer questions—they observe, learn from, and predict user intent to automate complex tasks.

---

## 🏛 The Five Generations Architecture

The SDK is structured into five evolutionary layers ("Generations"), each building upon the last to increase cognitive capability.

### **Gen 1: System Interop (The Foundation)**
* **Focus**: Raw data access and OS integration.
* **Component**: `client.py`
* **Status**: ✅ Active
* **Function**: Connects to KDE Klipper via D-Bus to read/write clipboard history (the "short-term memory" of the user).

### **Gen 2: Metrics & Logic (The Observer)**
* **Focus**: Data structuring and pattern recognition.
* **Component**: `etl.py`, `learning.py`
* **Status**: ✅ Active
* **Function**:
    *   **ETL**: Transforms raw clipboard text into structured `Entry` objects.
    *   **Learning**: Tracks usage frequency (star count) to identify important data.

### **Gen 3: The Tools Layer (The Body)**
* **Focus**: Actionable capabilities for agents.
* **Component**: `tools.py`, `learning_tools.py`
* **Status**: ✅ Active
* **Function**: Defines standard interfaces (`BaseTool`) for code execution, file manipulation, and content analysis.
    *   *Example*: `ContentAnalysisTool` determines if a clipboard entry is Python code, SQL, or JSON.

### **Gen 4: The Agentic Layer (The Mind)**
* **Focus**: Role-based decision making.
* **Component**: `agents.py`
* **Status**: ✅ Active
* **Function**: Abstract agents with specific personas and goals.
    *   **Analyst**: Analyzing data structure.
    *   **Planner**: Creating workflows.
    *   **Coder**: Implementing solutions.
    *   *Powered by*: Flexible LLM backends (Mock/Real).

### **Gen 5: Orchestration (The Conductor)**
* **Focus**: Meta-cognitive workflow management.
* **Component**: `orchestrator.py`
* **Status**: 🚧 **Current Focus**
* **Function**:
    *   **KickLang**: Consumes `.kl` blueprints to define multi-agent workflows.
    *   **Dynamic Execution**: Adapts the plan based on real-time data analysis (e.g., "If data is SQL, trigger the SQL Optimization Agent").

### Gen 6: The Holonic Layer (Structure)
* **Focus**: Recursive self-similarity.
* **Component**: `holon.py`
* **Status**: 🚧 **Implementation**
* **Function**: Allows agents to contain entire orchestration loops, and orchestrators to act as agents. Enables fractal scaling of the system.

### Gen 7: The Temporal Layer (Time)
* **Focus**: Time-series prediction and 4D context.
* **Component**: `learning.py` (Temporal Extension)
* **Status**: ✅ Active
* **Function**: Predicts *when* a user will need specific data or agents based on historical rhythm.

### Gen 8: The Spatial Layer (Topology)
* **Focus**: Graph-based knowledge representation.
* **Component**: `memory.py`
* **Status**: 
* **Function**: Maps relationships between data points in a persistent graph, enabling "Spatial" reasoning about concepts.

### Gen 9: The Consciousness Layer (Reflection)
* **Focus**: Self-optimization and critique.
* **Component**: `meta_critic.py`
* **Status**: 
* **Function**: Analyzes execution traces to rewrite its own blueprints (`.kl` files) for better future performance.

### Gen 10: The Transcendent Layer (Unity)
* **Focus**: Human-AI symbiosis.
* **Component**: `interface.py` (Space Format)
* **Status**: 
* **Function**: A unified interface where user intent and AI execution merge seamlessly, likely using the "Space" format standards.

---

## 📂 Directory Structure Map

```text
src/klipper_sdk/
├── client.py            # [Gen 1] D-Bus Client
├── etl.py               # [Gen 2] Transform Logic
├── learning.py          # [Gen 2] Usage Metrics
├── tools.py             # [Gen 3] Tool Interfaces
├── learning_tools.py    # [Gen 3] Domain Tools
├── agents.py            # [Gen 4] Agent Abstractions
└── orchestrator.py      # [Gen 5] KickLang Executor
```

---

## 🛠 Prerequisites

Before running the SDK, ensure you have the following:

- **Linux OS** with KDE Plasma (for Klipper).
- **Python 3.8+**.
- **Klipper Service** running on D-Bus.

---

## 🚀 Quick Start (Gen 5 Workflow)

To run the full orchestration loop with the provided blueprint:

```python
from klipper_sdk.orchestrator import Orchestrator

# 1. Initialize the Gen 5 Orchestrator
orchestrator = Orchestrator()

# 2. Load the KickLang Blueprint
# Ensure 'klipper_sdk_orchestration.kl' is in your working directory
orchestrator.load_blueprint("klipper_sdk_orchestration.kl")

# 3. Inject Runtime Context (Simulated Gen 1 Data)
context = {
    "entries": [
        {"text": "SELECT * FROM users", "type": "sql"},
        {"text": "def hello(): pass", "type": "python"}
    ]
}

# 4. Execute the Agentic Workflow
results = orchestrator.execute(dynamic_context=context)

print("\nOrchestration Results:", results)
```

## 📦 Installation

```bash
pip install .
```

---
*Maintained by the Klipper SDK Team*
