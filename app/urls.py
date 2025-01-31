from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path("admin/", admin.site.urls),
    
    path("", views.home, name="home"),
    path("negociations/", views.negociations, name="negociations"),

    path("", include("brokers.urls")),
    path("", include("tickers.urls")),
    path("", include("inflows.urls")),
    path("", include("outflows.urls")),
    path("", include("dividends.urls")),
]
