from django.urls import path
from . import views

urlpatterns = [
    path("brokers/list/", views.BrokerListView.as_view(), name="broker_list"),
    path("brokers/create/", views.BrokerCreateView.as_view(), name="broker_create"),
    path("brokers/<int:pk>/details/", views.BrokerDetailsView.as_view(), name="broker_details"),
    path("brokers/<int:pk>/update/", views.BrokerUpdateView.as_view(), name="broker_update"), 
    path("brokers/<int:pk>/delete", views.BrokerDeleteView.as_view(), name="broker_delete"),
    
]