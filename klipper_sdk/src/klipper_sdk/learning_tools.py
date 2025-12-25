import re
from typing import List, Dict, Any
from .tools import Tool
from .models import ClipboardItem

# Re-using the robust logic we created in backend/main.py, but encapsulated in a Tool
class ContentAnalysisTool(Tool):
    """Tool to analyze the content type of a text string."""
    
    def __init__(self):
        super().__init__(
            name="analyze_content_type",
            description="Analyze a text string to determine its type (url, sql_query, python_code, etc.). Args: text (str)"
        )

    def run(self, data: Any) -> Any:
        # Handle Batch
        if isinstance(data, list):
            return [self._analyze_single(item) for item in data]
        return self._analyze_single(data)

    def _analyze_single(self, item: Any) -> str:
        # Handle Dict (extract text)
        if isinstance(item, dict):
            text = item.get('text', '') or ''
        # Handle Object
        elif hasattr(item, 'text'):
            text = getattr(item, 'text', '') or ''
        else:
            text = str(item)

        if not text: return "binary"
        text = text.strip()
        
        # URL Detection
        if re.match(r'^https?://', text): return "url"
        
        # SQL
        if any(k in text.upper() for k in ["SELECT ", "INSERT INTO ", "UPDATE ", "DELETE FROM ", "CREATE TABLE", "ALTER TABLE"]) and "FROM" in text.upper():
            return "sql_query"
            
        # Python
        if any(k in text for k in ["def ", "import ", "class ", "print(", "__name__", "if __name__", "pandas", "numpy"]):
            if ":" in text or "=" in text: 
                return "python_code"

        # Frontend (React/TS/JS)
        if any(k in text for k in ["import React", "export const", "interface ", "function ", "console.log", "<div>", "className="]):
            return "frontend_code"
            
        # CSS
        if "{" in text and "}" in text and ":" in text and ";" in text and not "function" in text:
            if any(k in text for k in ["margin:", "padding:", "color:", "background:", "display:"]):
                return "css_style"

        # Shell/Bash
        if text.startswith("#!") or any(k in text for k in ["sudo ", "npm install", "pip install", "docker ", "kubectl ", "git "]):
            return "shell_command"

        # JSON
        if text.startswith("{") and text.endswith("}") and '"' in text:
            return "json_data"
            
        # Default Code fallback
        code_indicators = ['{', '}', ';', '(', ')', '[', ']', '=', 'return']
        if len(text.splitlines()) > 1 and sum(text.count(c) for c in code_indicators) > 3:
             return "code_snippet"

        return "text"

class WorkflowPredictionTool(Tool):
    """Tool to predict workflow based on content types."""
    
    def __init__(self):
        super().__init__(
            name="predict_workflow_score",
            description="Predict workflow from a list of content types. Args: types (List[str]), texts (optional List[str])"
        )

    def run(self, types: List[str], texts: List[str] = None) -> Dict[str, Any]:
        # Scores
        scores = {
            "Frontend Development": 0.0,
            "Backend Development": 0.0,
            "Data Science": 0.0,
            "DevOps/SRE": 0.0,
            "Research": 0.0
        }
        
        # Weighting logic
        for t in types:
            if t == "frontend_code": scores["Frontend Development"] += 3.0
            elif t == "css_style": scores["Frontend Development"] += 2.0
            elif t == "python_code": scores["Backend Development"] += 2.0; scores["Data Science"] += 1.0
            elif t == "sql_query": scores["Backend Development"] += 2.0; scores["Data Science"] += 2.5
            elif t == "shell_command": scores["DevOps/SRE"] += 3.0; scores["Backend Development"] += 1.0
            elif t == "json_data": scores["Backend Development"] += 1.0; scores["Frontend Development"] += 1.0
            elif t == "url": scores["Research"] += 1.5
        
        # Secondary pass if texts provided
        if texts:
            for txt_obj in texts:
                # Extract text if dict
                if isinstance(txt_obj, dict):
                    txt = txt_obj.get('text', '') or ''
                elif hasattr(txt_obj, 'text'):
                    txt = getattr(txt_obj, 'text', '') or ''
                else:
                    txt = str(txt_obj)

                txt = txt.lower() if txt else ""
                if "pandas" in txt or "notebook" in txt or "csv" in txt: scores["Data Science"] += 1.0
                if "react" in txt or "hook" in txt: scores["Frontend Development"] += 1.0
                if "docker" in txt or "aws" in txt or "deploy" in txt: scores["DevOps/SRE"] += 2.0
                if "django" in txt or "fastapi" in txt or "flask" in txt: scores["Backend Development"] += 2.0

        # Determine winner
        best_workflow = max(scores, key=scores.get)
        max_score = scores[best_workflow]
        
        total_score = sum(scores.values()) or 1
        confidence = min(max_score / (total_score * 0.5 + 2), 0.95)
        
        if max_score < 2.0:
            return {"name": "General", "confidence": 0.3, "reasoning": "Not enough specific patterns."}
            
        reasoning = f"Detected {best_workflow} patterns (score: {max_score})."
        
        return {
            "name": best_workflow,
            "confidence": round(confidence, 2),
            "reasoning": reasoning
        }
