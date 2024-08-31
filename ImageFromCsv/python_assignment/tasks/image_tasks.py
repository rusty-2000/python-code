from celery import Celery
from PIL import Image
import requests
from io import BytesIO
from models import db, Image
from api.webhook import trigger_webhook

app = Celery('tasks')

@app.task
def process_images(product_id, image_urls):
    output_urls = []
    for url in image_urls:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        output_buffer = BytesIO()
        img.save(output_buffer, format='JPEG', quality=50)
        output_url = f"http://mock-output-url/{product_id}/{url.split('/')[-1]}"
        output_urls.append(output_url)
        db.session.add(Image(product_id=product_id, original_url=url, processed_url=output_url))
    db.session.commit()
    trigger_webhook(product_id)
