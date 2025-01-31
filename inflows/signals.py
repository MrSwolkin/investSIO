from django.db.models.signals import post_save
from django.dispatch import receiver
from inflows.models import Inflow

@receiver(post_save, sender=Inflow)
def update_ticker_quantity(sender, instance, created, **kwargs):
    if created:
        if instance.quantity > 0:
            ticker = instance.ticker
            ticker.quantity += instance.quantity
            ticker.save()