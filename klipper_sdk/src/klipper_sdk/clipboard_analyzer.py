import re
from typing import List, Optional, Dict
from pydantic import BaseModel, Field
from datetime import datetime

class ClipboardItem(BaseModel):
    """Represents an item from the clipboard database."""
    uuid: str
    added_time: float
    last_used_time: Optional[float] = None
    mimetypes: str
    text: Optional[str] = None
    starred: bool = False

    @property
    def added_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.added_time)

class WorkflowPrediction(BaseModel):
    """Prediction about the user's current or next workflow."""
    name: str
    confidence: float
    reasoning: str

class ClipboardAnalyzer:
    """Analyzes clipboard items to determine user intent and workflows."""

    def __init__(self):
        self.items: List[ClipboardItem] = []

    def ingest_items(self, items: List[ClipboardItem]):
        """Load clipboard items into the analyzer."""
        self.items.extend(items)
        # Sort by added_time descending (newest first)
        self.items.sort(key=lambda x: x.added_time, reverse=True)

    def analyze_content_type(self, item: ClipboardItem) -> str:
        """Determine the primary type of content."""
        if not item.text:
            return "binary"
        
        text = item.text.strip()
        
        # URL detection
        if re.match(r'^https?://', text):
            return "url"
        
        # Code detection (heuristic)
        code_indicators = ['def ', 'class ', 'import ', 'return ', '{', '}', ';', 'SELECT ', 'FROM ']
        if any(ind in text for ind in code_indicators) and len(text.splitlines()) > 1:
            return "code_snippet"
            
        # SQL detection
        if "SELECT" in text.upper() and "FROM" in text.upper():
            return "sql_query"

        # Email detection
        if re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text):
            return "email"

        return "text"

    def cluster_by_time(self, threshold_seconds: float = 60.0) -> List[List[ClipboardItem]]:
        """Group items that were added within a short time window."""
        if not self.items:
            return []

        clusters = []
        current_cluster = [self.items[0]]
        
        for i in range(1, len(self.items)):
            prev_item = self.items[i-1]
            curr_item = self.items[i]
            
            # Note: items are sorted newest first, so prev_item is newer than curr_item
            time_diff = prev_item.added_time - curr_item.added_time
            
            if time_diff <= threshold_seconds:
                current_cluster.append(curr_item)
            else:
                clusters.append(current_cluster)
                current_cluster = [curr_item]
        
        clusters.append(current_cluster)
        return clusters

    def predict_workflow(self, recent_count: int = 5) -> WorkflowPrediction:
        """Predict the user's workflow based on recent items."""
        if not self.items:
            return WorkflowPrediction(name="Unknown", confidence=0.0, reasoning="No data")

        recent_items = self.items[:recent_count]
        types = [self.analyze_content_type(item) for item in recent_items]
        
        type_counts = {}
        for t in types:
            type_counts[t] = type_counts.get(t, 0) + 1
            
        total = len(recent_items)
        
        if type_counts.get('url', 0) / total >= 0.6:
            return WorkflowPrediction(
                name="Research", 
                confidence=0.8, 
                reasoning=f"Majority of recent items ({type_counts.get('url')} of {total}) are URLs."
            )
            
        if type_counts.get('code_snippet', 0) / total >= 0.4 or type_counts.get('sql_query', 0) > 0:
             return WorkflowPrediction(
                name="Development", 
                confidence=0.7, 
                reasoning="Recent items contain code snippets or SQL queries."
            )

        if type_counts.get('email', 0) > 0:
             return WorkflowPrediction(
                name="Communication", 
                confidence=0.6, 
                reasoning="Recent items contain email addresses."
            )

        return WorkflowPrediction(name="General", confidence=0.3, reasoning="Mixed content types.")

if __name__ == "__main__":
    # fast verification
    import time
    
    now = time.time()
    
    # Simulate a research session
    items = [
        ClipboardItem(uuid="1", added_time=now, mimetypes="text/plain", text="https://google.com"),
        ClipboardItem(uuid="2", added_time=now - 5, mimetypes="text/plain", text="https://wikipedia.org"),
        ClipboardItem(uuid="3", added_time=now - 10, mimetypes="text/plain", text="Interesting fact about LLMs"),
        ClipboardItem(uuid="4", added_time=now - 100, mimetypes="text/plain", text="def foo(): pass"),
    ]
    
    analyzer = ClipboardAnalyzer()
    analyzer.ingest_items(items)
    
    # Test Clustering
    clusters = analyzer.cluster_by_time(threshold_seconds=20)
    print(f"Clusters found: {len(clusters)}") # Should be 2 (research clump, then the older code snippet)
    
    # Test Prediction
    prediction = analyzer.predict_workflow()
    print(f"Predicted Workflow: {prediction.name} (Confidence: {prediction.confidence})")
    print(f"Reasoning: {prediction.reasoning}")
