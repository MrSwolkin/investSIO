from django.urls import path
from . import views

urlpatterns = [
    path("inflows/list/", views.InflowListView.as_view(), name="inflow_list"),
    path("inflows/create/", views.InflowCreateView.as_view(), name="inflow_create"),
    path("inflows/<int:pk>/details/", views.InflowDetailsView.as_view(), name="inflow_details"),
    path("inflows/<int:pk>/update/", views.InflowUpdateView.as_view(), name="inflow_update"),
    path("inflows/<int:pk>/delete/", views.InflowDeleteView.as_view(), name="inflow_delete"),
    
]