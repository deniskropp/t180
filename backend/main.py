from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import mysql.connector
from datetime import datetime
import re

app = FastAPI()

# CORS logic
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database Configuration
DB_CONFIG = {
    'host': '127.0.0.1',
    'port': 4448,
    'user': 'root', 
    'password': '',  # Assuming no password for local dev/test as per plan
    'database': 'db'
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

# Models
class ClipboardEntry(BaseModel):
    uuid: str
    added_time: float
    last_used_time: Optional[float] = None
    mimetypes: str
    text: Optional[str] = None
    starred: bool

class WorkflowPrediction(BaseModel):
    name: str
    confidence: float
    reasoning: str

import sys
import os

# Add SDK to path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "klipper_sdk", "src"))
from klipper_sdk.orchestrator import Orchestrator

# Initialize Orchestrator (Single instance for the app)
orchestrator = Orchestrator()
blueprint_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "workflow_prediction.kl")
orchestrator.load_blueprint(blueprint_path)

def predict_workflow(entries: List[ClipboardEntry]) -> WorkflowPrediction:
    if not entries:
        return WorkflowPrediction(name="Unknown", confidence=0.0, reasoning="No data available.")
        
    # Execute Gen 5 Workflow
    # We pass the entries as dynamic context. 
    # The blueprint 'workflow_prediction.kl' defines the steps 'analyze_entries' and 'predict_workflow'.
    
    # We use a recent subset to mimic the previous logic's optimization
    recent_entries = entries[:10]
    
    result_state = orchestrator.execute(dynamic_context={"entries": recent_entries})
    
    # Extract prediction from the result state
    pred_data = result_state.get('prediction')
    
    if not pred_data:
        return WorkflowPrediction(name="Error", confidence=0.0, reasoning="Orchestration failed to produce prediction.")
        
    return WorkflowPrediction(
        name=pred_data.get('name', 'Unknown'),
        confidence=pred_data.get('confidence', 0.0),
        reasoning=pred_data.get('reasoning', '')
    )

@app.get("/api/entries", response_model=List[ClipboardEntry])
def get_entries():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        # Join main and aux to get mimetype if needed, but main has 'mimetypes' text col
        # The schema shows 'main' has all we need
        cursor.execute("SELECT uuid, added_time, last_used_time, mimetypes, text, starred FROM main ORDER BY added_time DESC")
        rows = cursor.fetchall()
        
        entries = []
        for row in rows:
            entries.append(ClipboardEntry(
                uuid=row['uuid'],
                added_time=row['added_time'],
                last_used_time=row['last_used_time'],
                mimetypes=row['mimetypes'],
                text=row['text'],
                starred=bool(row['starred'])
            ))
        
        cursor.close()
        conn.close()
        return entries
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/entries/{uuid}/star")
def toggle_star(uuid: str):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check current state
        cursor.execute("SELECT starred FROM main WHERE uuid = %s", (uuid,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Entry not found")
        
        new_state = not result[0]
        cursor.execute("UPDATE main SET starred = %s WHERE uuid = %s", (new_state, uuid))
        conn.commit()
        
        cursor.close()
        conn.close()
        return {"starred": new_state}
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/prediction", response_model=WorkflowPrediction)
def get_prediction():
    # Helper to fetch entries first
    entries = get_entries()
    return predict_workflow(entries)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
