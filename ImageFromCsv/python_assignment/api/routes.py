from flask import Blueprint, request, jsonify
import uuid
from models import db, ImageProcessingRequest
from tasks.image_tasks import process_images
from utils.csv_utils import validate_csv

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/upload', methods=['POST'])
def upload_csv():
    file = request.files['file']
    if not file:

        return jsonify({"error": "No file provided"}), 400

    csv_data = file.read().decode('utf-8').splitlines()
    valid, data = validate_csv(csv_data)
    if not valid:
        return jsonify({"error": "Invalid CSV format"}), 400

    request_id = str(uuid.uuid4())
    db.session.add(ImageProcessingRequest(request_id=request_id, status='PENDING'))
    db.session.commit()

    for row in data:
        process_images.delay(row['product_id'], row['image_urls'])

    return jsonify({"request_id": request_id}), 200

@api_blueprint.route('/status/<request_id>', methods=['GET'])
def check_status(request_id):
    request_entry = ImageProcessingRequest.query.filter_by(request_id=request_id).first()
    if not request_entry:
        return jsonify({"error": "Invalid request ID"}), 404

    return jsonify({"status": request_entry.status}), 200
