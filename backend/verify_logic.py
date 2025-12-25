import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import predict_workflow, ClipboardEntry
import time

def test_prediction():
    print("\nTesting predict_workflow (via Gen 5 Orchestrator)...")
    
    # Scene 1: Frontend Dev
    entries_frontend = [
        ClipboardEntry(uuid="1", added_time=time.time(), mimetypes="text/plain", text="import React from 'react';", starred=False),
        ClipboardEntry(uuid="2", added_time=time.time(), mimetypes="text/plain", text="<div className='App'>", starred=False),
        ClipboardEntry(uuid="3", added_time=time.time(), mimetypes="text/plain", text="const [state, setState] = useState(0);", starred=False),
        ClipboardEntry(uuid="4", added_time=time.time(), mimetypes="text/plain", text="npm start", starred=False),
        ClipboardEntry(uuid="5", added_time=time.time(), mimetypes="text/plain", text="background-color: #fff;", starred=False),
    ]
    pred = predict_workflow(entries_frontend)
    print(f"Scenario: Frontend Dev -> Predicted: {pred.name} ({pred.confidence})")
    assert pred.name == "Frontend Development"

    # Scene 2: Backend/Data
    entries_backend = [
        ClipboardEntry(uuid="1", added_time=time.time(), mimetypes="text/plain", text="SELECT * FROM users WHERE id = 1", starred=False),
        ClipboardEntry(uuid="2", added_time=time.time(), mimetypes="text/plain", text="import pandas as pd", starred=False),
        ClipboardEntry(uuid="3", added_time=time.time(), mimetypes="text/plain", text="df = pd.read_csv('data.csv')", starred=False),
        ClipboardEntry(uuid="4", added_time=time.time(), mimetypes="text/plain", text="def process_data(data):\n return data", starred=False),
    ]
    pred = predict_workflow(entries_backend)
    print(f"Scenario: Backend/Data -> Predicted: {pred.name} ({pred.confidence})")
    assert pred.name in ["Backend Development", "Data Science"]

if __name__ == "__main__":
    try:
        test_prediction()
        print("\nAll integration tests passed!")
    except AssertionError as e:
        print(f"\nTest Failed: {e}")
        exit(1)
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"\nError: {e}")
        exit(1)
