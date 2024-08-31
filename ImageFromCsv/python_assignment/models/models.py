from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    serial_number = db.Column(db.Integer, nullable=False)
    product_name = db.Column(db.String(255), nullable=False)

class ImageProcessingRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    request_id = db.Column(db.String(36), nullable=False, unique=True)
    status = db.Column(db.Enum('PENDING', 'PROCESSING', 'COMPLETED', 'FAILED'), nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    original_url = db.Column(db.Text, nullable=False)
    processed_url = db.Column(db.Text)

class Webhook(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    request_id = db.Column(db.String(36), db.ForeignKey('image_processing_request.request_id'))
    callback_url = db.Column(db.Text, nullable=False)
