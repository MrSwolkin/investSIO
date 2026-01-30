from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from . import models, forms
from app.utils.validators import validate_broker_name


class BrokerListView(LoginRequiredMixin, ListView):
    model = models.Broker
    template_name = "broker_list.html"
    context_object_name = "brokers"
    paginate_by = 25

    def get_queryset(self):
        queryset = super().get_queryset()

        # Validate and sanitize input parameter
        name = validate_broker_name(self.request.GET.get("name"))
        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset


class BrokerCreateView(LoginRequiredMixin, CreateView):
    model = models.Broker
    template_name = "broker_create.html"
    form_class = forms.brokerForm
    success_url = reverse_lazy("broker_list")

class BrokerDetailsView(LoginRequiredMixin, DetailView):
    model = models.Broker
    template_name = "broker_details.html"


class BrokerUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Broker
    template_name = "broker_update.html"
    form_class = forms.brokerForm
    success_url = reverse_lazy("broker_list")

class BrokerDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Broker
    template_name = "broker_delete.html"
    success_url = reverse_lazy("broker_list")
