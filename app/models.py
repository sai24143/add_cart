from django.db import models

class CartItem(models.Model):
    product_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def total_price(self):
        return self.quantity * self.price
