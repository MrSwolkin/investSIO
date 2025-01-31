from django.contrib import admin
from . import models

class DividendAdmin(admin.ModelAdmin):
    list_display = ("ticker", "date", "value", "total_value")
    search_fields = ("ticker", )


admin.site.register(models.Dividend, DividendAdmin)
