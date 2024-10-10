from typing import Dict
from fastapi import APIRouter, HTTPException
from model.garbage_model import classify_object
from pydantic import BaseModel

class GarbageRequest(BaseModel):
    object_name: str
    probability: float

router = APIRouter()

@router.post("/classify")
async def classify(garbageRequest: GarbageRequest):
    """
    Classify an object into a bin type.
    """
    object_name = garbageRequest.object_name
    probability = garbageRequest.probability
    
    # Routine checks to ensure it works
    if not object_name or probability is None:
        raise HTTPException(status_code=400, detail="Invalid Request")
    
    if probability < 0.5:
        raise HTTPException(status_code=400, detail="Probability must be at least 0.5")
    
    # Classify the object
    result: Dict[str, str] = await classify_object(object_name)

    return result