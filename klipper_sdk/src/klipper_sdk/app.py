from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
from .learning import LearningManager

app = FastAPI(title="Meta-AI Orchestrator API")
learning_manager = LearningManager()

class PredictionRequest(BaseModel):
    uuid: str
    age_in_days: float
    recency_score: float

class StarredResponse(BaseModel):
    uuid: str
    probability: float

class UsageResponse(BaseModel):
    uuid: str
    predicted_last_used_time: float

@app.get("/")
def health_check():
    return {"status": "online", "model": "Meta-AI Orchestrator"}

@app.post("/predict/starred", response_model=StarredResponse)
def predict_starred(request: PredictionRequest):
    # TAS 3.1: API Implementation
    prob = learning_manager.predict_starred(request.age_in_days, request.recency_score)
    return StarredResponse(uuid=request.uuid, probability=prob)

@app.post("/predict/usage", response_model=UsageResponse)
def predict_usage(request: PredictionRequest):
    # TAS 3.1: API Implementation
    usage_time = learning_manager.predict_usage(request.age_in_days)
    return UsageResponse(uuid=request.uuid, predicted_last_used_time=usage_time)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
