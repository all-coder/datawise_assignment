from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime
from bson import ObjectId

class QualityLogModel(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    dataset_id: str
    status: Literal["PASS", "FAIL"]
    details: str
    timestamp: datetime

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str}
    }
