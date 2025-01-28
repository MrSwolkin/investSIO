from django.db import models

class Currency(models.Model):
    code = models.CharField(max_length=5)
    name = models.CharField(max_length=50)
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)

    class Meta:
        ordering = ["code"]

    def __str__(self):
        return self.code


class Broker(models.Model):
    name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=500, null=True, blank=True)
    country = models.CharField(max_length=20, null=True, blank=True)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, null=True, blank=True, related_name="brokers")
    description = models.TextField(null=True, blank=True)
    
    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name

