from django.contrib import admin
from . import models


class InflowAdmin(admin.ModelAdmin):
    list_display = ("ticker", "quantity", "total_price",)
    search_fields = ("ticker__name",)


admin.site.register(models.Inflow, InflowAdmin)
