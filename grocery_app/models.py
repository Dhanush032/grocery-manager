from django.db import models

# Create your models here.

from django.db import models

class UOM(models.Model):
    uom_name = models.CharField(max_length=100)

class Product(models.Model):
    name = models.CharField(max_length=100)
    uom = models.ForeignKey(UOM, on_delete=models.CASCADE)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)

class Order(models.Model):
    customer_name = models.CharField(max_length=100)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    datetime = models.DateTimeField(auto_now_add=True)

class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
