from django.contrib import admin
from . import models

class BrokerAdmin(admin.ModelAdmin):
    list_display = ("name", "account_number", "description",)
    search_fields = ("name",)
    

class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("name", "code")
    search_fields = ("code",)

admin.site.register(models.Broker, BrokerAdmin)
admin.site.register(models.Currency, CurrencyAdmin)
