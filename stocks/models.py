from django.db import models

class Trade(models.Model):
    symbol = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=20, decimal_places=8)
    size = models.DecimalField(max_digits=20, decimal_places=8)
    taker_side = models.CharField(max_length=10)
    timestamp = models.DateTimeField()
    
    def __str__(self):
        return f"{self.symbol} - {self.price} - {self.size}"
