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

# Reusing Analyzer Logic (Simplified for this file)
def analyze_content_type(text: str) -> str:
    if not text: return "binary"
    text = text.strip()
    if re.match(r'^https?://', text): return "url"
    if "SELECT" in text.upper() and "FROM" in text.upper(): return "sql_query"
    code_indicators = ['def ', 'class ', 'import ', 'return ', '{', '}', ';']
    if any(ind in text for ind in code_indicators) and len(text.splitlines()) > 1: return "code_snippet"
    return "text"

def predict_workflow(entries: List[ClipboardEntry]) -> WorkflowPrediction:
    if not entries:
        return WorkflowPrediction(name="Unknown", confidence=0.0, reasoning="No data")
    
    recent = entries[:5]
    types = [analyze_content_type(e.text or "") for e in recent]
    total = len(recent)
    type_counts = {t: types.count(t) for t in set(types)}
    
    if type_counts.get('url', 0) / total >= 0.6:
        return WorkflowPrediction(name="Research", confidence=0.8, reasoning="Mostly URLs in recent history.")
    if type_counts.get('code_snippet', 0) / total >= 0.4 or type_counts.get('sql_query', 0) > 0:
        return WorkflowPrediction(name="Development", confidence=0.7, reasoning="Code or SQL detected.")
    
    return WorkflowPrediction(name="General", confidence=0.3, reasoning="Mixed content types.")

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
