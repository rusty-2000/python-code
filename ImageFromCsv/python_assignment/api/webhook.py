import requests
from models import Webhook

def trigger_webhook(request_id):
    webhook = Webhook.query.filter_by(request_id=request_id).first()
    if webhook:
        requests.post(webhook.callback_url, json={"request_id": request_id, "status": "COMPLETED"})
