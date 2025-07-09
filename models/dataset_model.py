from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from bson import ObjectId

class DatasetModel(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    name: str
    owner: str
    description: str
    tags: List[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_deleted: bool = False

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str}
    }
