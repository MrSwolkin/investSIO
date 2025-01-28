from django.urls import path
from . import views

urlpatterns = [
    path("tickers/<str:category>/", views.TickerListView.as_view(), name="ticker_list"),
    path("tickers/<str:category>/create", views.TickerCreateView.as_view(), name="ticker_create"),
    path("tickers/<str:category>/<int:pk>/details", views.TickerDetailsView.as_view(), name="ticker_details"),
    path("tickers/<str:category>/<int:pk>/update", views.TickerUpdateView.as_view(), name="ticker_update"),
]