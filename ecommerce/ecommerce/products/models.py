from django.db import models
"""
    Model representing a product in the e-commerce application.

    Attributes:
        name (str): The name of the product.
        description (str): A description of the product.pip install drf-yasg
        price (Decimal): The price of the product.
        created_at (DateTime): The date and time when the product was created.
        updated_at (DateTime): The date and time when the product was last updated.
    """
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)