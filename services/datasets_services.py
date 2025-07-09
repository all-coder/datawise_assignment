from models.dataset_model import DatasetModel
from typing import Optional, Dict, Any
from pymongo.database import Database
from bson import ObjectId

def create_new_dataset(db: Database, dataset: Dict[str, Any]) -> Dict[str, Any]:
    try:
        validated = DatasetModel(**dataset)
        result = db.datasets.insert_one(validated.model_dump(by_alias=True))
        return {"status": "success", "dataset_id": str(result.inserted_id)}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def get_all_datasets(db: Database, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    try:
        query = {}
        if filters:
            if "owner" in filters:
                query["owner"] = filters["owner"]
            if "tags" in filters:
                query["tags"] = {"$in": filters["tags"]}
            if "is_deleted" in filters:
                query["is_deleted"] = filters["is_deleted"]

        datasets = []
        for doc in db.datasets.find(query):
            doc["id"] = str(doc["_id"])
            doc.pop("_id")
            datasets.append(doc)

        return {"status": "success", "datasets": datasets}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
def get_dataset_by_id(db: Database, dataset_id: str) -> Dict[str, Any]:
    try:
        if not ObjectId.is_valid(dataset_id):
            return {"status": "error", "message": "Invalid dataset_id"}

        doc = db.datasets.find_one({"_id": ObjectId(dataset_id)})
        if not doc:
            return {"status": "error", "message": "Dataset not found"}
        doc["id"] = str(doc["_id"])
        doc.pop("_id")
        return {"status": "success", "dataset": doc}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
def update_dataset_by_id(db: Database, dataset_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
    try:
        if not ObjectId.is_valid(dataset_id):
            return {"status": "error", "message": "Invalid dataset_id"}

        updates.pop("_id", None)
        updates.pop("id", None)

        result = db.datasets.update_one(
            {"_id": ObjectId(dataset_id)},
            {"$set": updates}
        )

        if result.matched_count == 0:
            return {"status": "error", "message": "Dataset not found"}

        if result.modified_count == 0:
            return {"status": "success", "message": "No changes made"}

        return {"status": "success", "message": "Dataset updated successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    

def soft_delete_dataset(db: Database, dataset_id: str) -> dict:
    try:
        if not ObjectId.is_valid(dataset_id):
            return {"status": "error", "message": "Invalid dataset_id"}

        oid = ObjectId(dataset_id)

        result = db.datasets.update_one(
            {"_id": oid},
            {"$set": {"is_deleted": True}}
        )

        if result.matched_count == 0:
            return {"status": "error", "message": "Dataset not found"}

        return {"status": "success", "message": "Dataset soft deleted"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
