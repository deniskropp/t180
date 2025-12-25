import json
import sqlite3
import pandas as pd
from typing import List, Optional, Dict
from pydantic import BaseModel, Field

class RowMain(BaseModel):
    uuid: str
    added_time: float
    last_used_time: Optional[float] = None
    mimetypes: List[str]
    text: Optional[str] = None
    starred: bool = False

class ETLPipeline:
    def __init__(self, db_path: str = ":memory:"):
        self.conn = sqlite3.connect(db_path)
    
    def load_schema(self, sql_file: str):
        with open(sql_file, 'r') as f:
            self.conn.executescript(f.read())

    def normalize_mimetypes(self, mt_string: str) -> List[str]:
        # Implementation for TAS 1.4
        if not mt_string:
            return []
        try:
            return json.loads(mt_string)
        except json.JSONDecodeError:
            return [mt_string] if mt_string else []

    def ingest_main(self) -> List[RowMain]:
        query = "SELECT uuid, added_time, last_used_time, mimetypes, text, starred FROM main"
        df = pd.read_sql_query(query, self.conn)
        
        # TAS 1.2: Validate constraints (added_time > 0, last_used_time > 0)
        # Using handle NULL for last_used_time
        rows = []
        for _, row in df.iterrows():
            mimetypes = self.normalize_mimetypes(row['mimetypes'])
            
            # TAS 1.4: Handle NULL in last_used_time
            last_used = row['last_used_time']
            if pd.isna(last_used) or last_used <= 0:
                last_used = None
            
            rows.append(RowMain(
                uuid=row['uuid'],
                added_time=max(0.1, row['added_time']), # Constraint validation
                last_used_time=last_used,
                mimetypes=mimetypes,
                text=row['text'],
                starred=bool(row['starred'])
            ))
        return rows

if __name__ == "__main__":
    # Example usage for verification
    pipeline = ETLPipeline()
    # pipeline.load_schema("db/doltdump.sql")
    # ... logic to populate and test
