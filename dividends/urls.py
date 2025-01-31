from django.urls import path
from . import views

urlpatterns = [
    path("dividends/list/", views.DividendListView.as_view(), name="dividend_list"),
    path("dividends/create/", views.DividendCreateView.as_view(), name="dividend_create"),
    path("dividends/<int:pk>/update/", views.DividendUpdateView.as_view(), name="dividend_update"),
    path("dividends/<int:pk>/delete/",views.DividendDeleteView.as_view(), name="dividend_delete"),
]