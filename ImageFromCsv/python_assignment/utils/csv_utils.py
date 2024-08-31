import csv
from models import Image, Product


# Existing function to validate CSV
def validate_csv(csv_data):
    data = []
    reader = csv.DictReader(csv_data)
    for row in reader:
        if not row.get('S. No.') or not row.get('Product Name') or not row.get('Input Image Urls'):
            return False, []
        image_urls = row['Input Image Urls'].split(',')
        data.append({
            'serial_number': row['S. No.'],
            'product_name': row['Product Name'],
            'image_urls': image_urls
        })
    return True, data


# New function to generate the output CSV
def generate_output_csv(request_id):
    products = Product.query.all()

    with open(f'{request_id}_output.csv', 'w', newline='') as csvfile:
        fieldnames = ['Serial Number', 'Product Name', 'Input Image Urls', 'Output Image Urls']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for product in products:
            images = Image.query.filter_by(product_id=product.id).all()
            input_urls = ', '.join([img.original_url for img in images])
            output_urls = ', '.join([img.processed_url for img in images])
            writer.writerow({
                'Serial Number': product.serial_number,
                'Product Name': product.product_name,
                'Input Image Urls': input_urls,
                'Output Image Urls': output_urls
            })

    print(f"Output CSV {request_id}_output.csv generated successfully!")
