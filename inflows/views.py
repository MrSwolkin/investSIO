from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Inflow
from . import forms


class InflowListView(ListView):
    model = Inflow
    template_name = "inflow_list.html"
    context_object_name = "inflows"
    
    def get_queryset(self):
        queryset =  super().get_queryset()
        ticker = self.request.GET.get("ticker")
        #if ticker:
        #   queryset = queryset.filter(ticker__name__icontains=ticker)
        print(ticker)
        return queryset

class InflowDetailsView(DetailView):
    model = Inflow
    template_name = "inflow_details.html"

class InflowCreateView(CreateView):
    model = Inflow
    template_name = "inflow_create.html"
    form_class = forms.InflowForms
    success_url = reverse_lazy("inflow_list")

class InflowUpdateView(UpdateView):
    model = Inflow
    template_name = "inflow_update.html"
    form_class = forms.InflowForms
    success_url = reverse_lazy("inflow_list")

class InflowDeleteView(DeleteView):
    model = Inflow
    template_name = "inflow_delete.html"
    success_url = reverse_lazy("inflow_list")
