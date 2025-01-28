from django.contrib import admin
from . import models


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("title",)


admin.site.register(models.Category, CategoryAdmin)
