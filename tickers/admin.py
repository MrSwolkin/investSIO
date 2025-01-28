from django.contrib import admin
from . import models

class TickerAdmin(admin.ModelAdmin):
    list_display = ("name", "quantity",)
    search_fields = ("name",)
    

admin.site.register(models.Ticker, TickerAdmin)