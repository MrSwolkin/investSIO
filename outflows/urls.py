from django.urls import path 
from . import views

urlpatterns = [
    path("outflow/list/", views.OutflowListView.as_view(), name="outflow_list"),
    path("outflow/create/", views.OutflowCreateView.as_view(), name="outflow_create"),
    path("outflow/<int:pk>/details/", views.OutflowDetailsView.as_view(), name="outflow_details"),
    path("outflow/<int:pk>/update/", views.OutflowUpdateView.as_view(), name="outflow_update"),
    path("outflow/<int:pk>/delete", views.OutflowDeleteView.as_view(), name="outflow_delete"),
]