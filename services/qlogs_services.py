from bson import ObjectId
from datetime import datetime
from pymongo.database import Database
from typing import Literal, Dict, List, Any
from models.qlogs_model import QualityLogModel

def add_quality_log(db: Database, dataset_id: str, status: Literal["PASS", "FAIL"], details: str) -> Dict[str, Any]:
    try:
        if not ObjectId.is_valid(dataset_id):
            return {"status": "error", "message": "Invalid dataset_id"}

        log = QualityLogModel(
            dataset_id=dataset_id,
            status=status,
            details=details,
            timestamp=datetime.utcnow()
        )
        result = db.quality_logs.insert_one(log.model_dump(by_alias=True))
        return {"status": "success", "log_id": str(result.inserted_id)}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def get_quality_logs_by_id(db: Database, dataset_id: str) -> Dict[str, Any]:
    try:
        if not ObjectId.is_valid(dataset_id):
            return {"status": "error", "message": "Invalid dataset_id"}

        logs: List[Dict[str, Any]] = []
        cursor = db.quality_logs.find({"dataset_id": dataset_id})
        for doc in cursor:
            doc["id"] = str(doc["_id"])
            doc.pop("_id")
            logs.append(doc)

        return {"status": "success", "logs": logs}
    except Exception as e:
        return {"status": "error", "message": str(e)}
