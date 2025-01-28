from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from . import models, forms


class BrokerListView(ListView):
    model = models.Broker
    template_name = "broker_list.html"
    context_object_name = "brokers"

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get("name")
        if name:
            queryset = queryset.filter(name__icontains=name)
            
        return queryset


class BrokerCreateView(CreateView):
    model = models.Broker
    template_name = "broker_create.html"
    form_class = forms.brokerForm
    success_url = reverse_lazy("broker_list")

class BrokerDetailsView(DetailView):
    model = models.Broker
    template_name = "broker_details.html"


class BrokerUpdateView(UpdateView):
    model = models.Broker
    template_name = "broker_update.html"
    form_class = forms.brokerForm
    success_url = reverse_lazy("broker_list")

class BrokerDeleteView(DeleteView):
    model = models.Broker
    template_name = "broker_delete.html"
    success_url = reverse_lazy("broker_list")
