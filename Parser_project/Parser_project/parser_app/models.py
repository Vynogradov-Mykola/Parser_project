from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=500, null=True, blank=True)

    brand = models.CharField(max_length=255, null=True, blank=True)
    color = models.CharField(max_length=255, null=True, blank=True)
    memory = models.CharField(max_length=255, null=True, blank=True)

    screen_size = models.CharField(max_length=255, null=True, blank=True)
    resolution = models.CharField(max_length=255, null=True, blank=True)

    price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    sale_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    product_code = models.CharField(max_length=100, unique=True, null=True, blank=True)

    reviews_count = models.IntegerField(null=True, blank=True)

    images = models.JSONField(default=list, blank=True)
    characteristics = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or "Product"