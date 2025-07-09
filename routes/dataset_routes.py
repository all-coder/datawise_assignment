from flask import Blueprint, request, jsonify,current_app
from datetime import datetime, timezone
from services.datasets_services import get_all_datasets,create_new_dataset, get_dataset_by_id, update_dataset_by_id, soft_delete_dataset   
from flasgger import swag_from
dataset_route = Blueprint('dataset', __name__)

@dataset_route.route('/', methods=['GET'])
@swag_from('docs/fetch_all_datasets.yml')
def fetch_all_datasets():
    db = current_app.config['db'] 
    try:
        filters = {}
        owner = request.args.get('owner')
        tags = request.args.getlist('tags')
        is_deleted = request.args.get('is_deleted')

        if owner:
            filters['owner'] = owner
        if tags:
            filters['tags'] = tags
        if is_deleted is not None:
            filters['is_deleted'] = is_deleted.lower() == 'true'

        result = get_all_datasets(db, filters if filters else None)
        return jsonify(result), 200 if result["status"] == "success" else 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@dataset_route.route('/', methods=['POST'])
@swag_from('docs/create_dataset.yml')
def create_dataset():
    db = current_app.config['db'] 
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "No data provided"}), 400

        result = create_new_dataset(db, data)
        return jsonify(result), 201 if result["status"] == "success" else 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@dataset_route.route('/<dataset_id>', methods=['GET'])
@swag_from('docs/get_dataset.yml')
def get_dataset(dataset_id):
    db = current_app.config['db'] 
    try:
        result = get_dataset_by_id(db, dataset_id)
        return jsonify(result), 200 if result["status"] == "success" else 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@dataset_route.route('/<dataset_id>', methods=['PUT'])
@swag_from('docs/update_dataset.yml')
def update_dataset(dataset_id):
    db = current_app.config['db']
    try:
        updates = request.get_json()
        if not updates:
            return jsonify({"status": "error", "message": "No update data provided"}), 400
        updates["updated_at"] = datetime.utcnow()
        result = update_dataset_by_id(db, dataset_id, updates)
        status_code = 200 if result["status"] == "success" else 404
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    

@dataset_route.route('/<dataset_id>', methods=['DELETE'])
@swag_from('docs/delete_dataset.yml')
def delete_dataset(dataset_id):
    db = current_app.config['db'] 
    try:
        result = soft_delete_dataset(db, dataset_id)
        return jsonify(result), 200 if result["status"] == "success" else 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

