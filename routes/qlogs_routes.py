from flask import Blueprint, request, jsonify,current_app
from services.qlogs_services import add_quality_log, get_quality_logs_by_id
from flasgger import swag_from

qlog_routes = Blueprint('qlog_routes', __name__)
@qlog_routes.route('/<dataset_id>/quality-1', methods=['POST'])
@swag_from('docs/add_quality_log.yml')
def add_qlog(dataset_id):
    db = current_app.config['db'] 
    try:
        data = request.get_json()
        if not data or 'status' not in data or 'details' not in data:
            return jsonify({"status": "error", "message": "Missing 'status' or 'details' in request"}), 400

        status = data['status']
        details = data['details']

        result = add_quality_log(db, dataset_id, status, details)
        return jsonify(result), 201 if result["status"] == "success" else 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@qlog_routes.route('/<dataset_id>/quality-1', methods=['GET'])
@swag_from('docs/get_quality_log.yml')
def get_qlogs(dataset_id):
    db = current_app.config['db'] 
    try:
        result = get_quality_logs_by_id(db, dataset_id)
        return jsonify(result), 200 if result["status"] == "success" else 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
