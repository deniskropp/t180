from datetime import datetime
from typing import List, Optional
import pandas as pd
import numpy as np
# from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import MultiLabelBinarizer

from .etl import RowMain

class ModelFeatures(pd.DataFrame):
    """Container for engineered features."""
    pass

class LearningManager:
    def __init__(self):
        self.mlb = None # For mimetypes encoding
        self.model_starred = None
        self.model_usage = None

    def engineer_features(self, rows: List[RowMain]) -> pd.DataFrame:
        now = datetime.now().timestamp()
        
        data = []
        for r in rows:
            data.append({
                "uuid": r.uuid,
                "age_in_days": (now - r.added_time) / (24 * 3600),
                "recency_score": (now - r.last_used_time) / (24 * 3600) if r.last_used_time else 999.0,
                "mimetypes": r.mimetypes,
                "starred": int(r.starred),
                "last_used_time": r.last_used_time or 0.0
            })
        
        df = pd.DataFrame(data)
        
        # TAS 2.1: Simple encoding for mimetypes (dimensionality reduction if needed later)
        # Note: In a real scenario, use MultiLabelBinarizer or embeddings
        return df

    def train_models(self, df: pd.DataFrame):
        # TAS 2.2: Mock training logic
        print(f"Training models on {len(df)} rows...")
        # X = df[['age_in_days', 'recency_score']]
        # y_starred = df['starred']
        # self.model_starred = RandomForestClassifier().fit(X, y_starred)
        pass

    def predict_starred(self, age: float, recency: float) -> float:
        # Mock prediction
        return 0.75

    
    def predict_usage(self, age: float) -> float:
        # Mock prediction
        return datetime.now().timestamp() + 3600

class TemporalPredictor:
    """
    Gen 7: Temporal Layer.
    Predicts *when* an event will occur based on historical rhythm.
    """
    def __init__(self):
        self.history = []

    def add_event(self, timestamp: float):
        self.history.append(timestamp)
        self.history.sort()

    def predict_next(self) -> float:
        """
        Simple rhythm analysis: Average Interval.
        """
        if len(self.history) < 2:
            # Default to 1 hour from now if insufficient data
            return datetime.now().timestamp() + 3600
            
        intervals = [t2 - t1 for t1, t2 in zip(self.history[:-1], self.history[1:])]
        avg_interval = sum(intervals) / len(intervals)
        
        last_event = self.history[-1]
        next_event = last_event + avg_interval
        
        # Ensure prediction is in the future
        now = datetime.now().timestamp()
        if next_event < now:
            # If the predicted time is already past, project forward by intervals
            while next_event < now:
                next_event += avg_interval
                
        return next_event

if __name__ == "__main__":
    manager = LearningManager()
    
    # Gen 7 Test
    print("Testing Temporal Predictor...")
    pred = TemporalPredictor()
    # Simulate an event happening every hour for the last 5 hours
    base_time = datetime.now().timestamp() - (5 * 3600)
    for i in range(5):
        pred.add_event(base_time + (i * 3600))
    
    next_time = pred.predict_next()
    print(f"Last Event: {datetime.fromtimestamp(pred.history[-1])}")
    print(f"Predicted Next: {datetime.fromtimestamp(next_time)}")
    
    diff = next_time - pred.history[-1]
    print(f"Gap: {diff} seconds (Expected ~3600)")
