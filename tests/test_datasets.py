import pytest
from unittest.mock import MagicMock
from bson import ObjectId
from services.datasets_services import get_all_datasets,create_new_dataset, get_dataset_by_id, update_dataset_by_id, soft_delete_dataset   

from datetime import datetime
from bson import ObjectId
from unittest.mock import MagicMock
from services.datasets_services import create_new_dataset

def test_create_new_dataset_success():
    db = MagicMock()
    db.datasets.insert_one.return_value.inserted_id = ObjectId()

    payload = {
        "_id": ObjectId(),
        "name": "Test Dataset",
        "owner": "user1",
        "description": "Sample description",
        "tags": ["tag1", "tag2"],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "is_deleted": False
    }

    result = create_new_dataset(db, payload)

    assert result["status"] == "success"
    assert "dataset_id" in result


def test_create_new_dataset_invalid_schema():
    db = MagicMock()
    result = create_new_dataset(db, {"invalid": "data"})
    assert result["status"] == "error"

def test_get_all_datasets_no_filters():
    db = MagicMock()
    db.datasets.find.return_value = [{"_id": ObjectId(), "name": "Dataset1"}]
    result = get_all_datasets(db)
    assert result["status"] == "success"
    assert isinstance(result["datasets"], list)

def test_get_all_datasets_with_filters():
    db = MagicMock()
    db.datasets.find.return_value = [{"_id": ObjectId(), "owner": "u1", "tags": ["tag1"]}]
    result = get_all_datasets(db, filters={"owner": "u1", "tags": ["tag1"]})
    assert result["status"] == "success"

def test_get_dataset_by_id_invalid():
    db = MagicMock()
    result = get_dataset_by_id(db, "invalid_id")
    assert result["status"] == "error"

def test_get_dataset_by_id_not_found():
    db = MagicMock()
    db.datasets.find_one.return_value = None
    result = get_dataset_by_id(db, str(ObjectId()))
    assert result["status"] == "error"

def test_get_dataset_by_id_success():
    oid = ObjectId()
    db = MagicMock()
    db.datasets.find_one.return_value = {"_id": oid, "name": "Data"}
    result = get_dataset_by_id(db, str(oid))
    assert result["status"] == "success"
    assert result["dataset"]["id"] == str(oid)

def test_update_dataset_by_id_invalid():
    db = MagicMock()
    result = update_dataset_by_id(db, "bad_id", {"name": "new"})
    assert result["status"] == "error"

def test_update_dataset_by_id_not_found():
    db = MagicMock()
    db.datasets.update_one.return_value.matched_count = 0
    result = update_dataset_by_id(db, str(ObjectId()), {"name": "new"})
    assert result["status"] == "error"

def test_update_dataset_by_id_no_change():
    db = MagicMock()
    mock_result = MagicMock(matched_count=1, modified_count=0)
    db.datasets.update_one.return_value = mock_result
    result = update_dataset_by_id(db, str(ObjectId()), {"name": "same"})
    assert result["message"] == "No changes made"

def test_update_dataset_by_id_success():
    db = MagicMock()
    mock_result = MagicMock(matched_count=1, modified_count=1)
    db.datasets.update_one.return_value = mock_result
    result = update_dataset_by_id(db, str(ObjectId()), {"name": "changed"})
    assert result["message"] == "Dataset updated successfully"

def test_soft_delete_dataset_invalid():
    db = MagicMock()
    result = soft_delete_dataset(db, "bad_id")
    assert result["status"] == "error"

def test_soft_delete_dataset_not_found():
    db = MagicMock()
    db.datasets.update_one.return_value.matched_count = 0
    result = soft_delete_dataset(db, str(ObjectId()))
    assert result["status"] == "error"

def test_soft_delete_dataset_success():
    db = MagicMock()
    db.datasets.update_one.return_value.matched_count = 1
    result = soft_delete_dataset(db, str(ObjectId()))
    assert result["status"] == "success"
