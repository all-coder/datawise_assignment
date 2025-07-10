import pytest
from unittest.mock import MagicMock
from bson import ObjectId
from services.qlogs_services import add_quality_log, get_quality_logs_by_id

def test_add_quality_log_success():
    db = MagicMock()
    db.quality_logs.insert_one.return_value.inserted_id = ObjectId()
    result = add_quality_log(db, str(ObjectId()), "PASS", "Looks good")
    assert result["status"] == "success"
    assert "log_id" in result

def test_add_quality_log_invalid_id():
    db = MagicMock()
    result = add_quality_log(db, "bad_id", "FAIL", "Details here")
    assert result["status"] == "error"
    assert "Invalid dataset_id" in result["message"]

def test_add_quality_log_insert_exception():
    db = MagicMock()
    db.quality_logs.insert_one.side_effect = Exception("DB error")
    result = add_quality_log(db, str(ObjectId()), "FAIL", "Failed check")
    assert result["status"] == "error"
    assert "DB error" in result["message"]

def test_get_quality_logs_by_id_success():
    db = MagicMock()
    fake_log = {"_id": ObjectId(), "dataset_id": "abc123", "status": "PASS", "details": "ok"}
    db.quality_logs.find.return_value = [fake_log]
    result = get_quality_logs_by_id(db, str(ObjectId()))
    assert result["status"] == "success"
    assert isinstance(result["logs"], list)
    assert "id" in result["logs"][0]

def test_get_quality_logs_by_id_invalid_id():
    db = MagicMock()
    result = get_quality_logs_by_id(db, "not_an_objectid")
    assert result["status"] == "error"
    assert "Invalid dataset_id" in result["message"]

def test_get_quality_logs_by_id_exception():
    db = MagicMock()
    db.quality_logs.find.side_effect = Exception("Cursor crash")
    result = get_quality_logs_by_id(db, str(ObjectId()))
    assert result["status"] == "error"
    assert "Cursor crash" in result["message"]
