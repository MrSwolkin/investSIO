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

        return queryset

class InflowDetailsView(DetailView):
    model = Inflow
    template_name = "inflow_details.html"

class InflowCreateView(CreateView):
    model = Inflow
    template_name = "inflow_create.html"
    form_class = forms.InflowForms
    

    def get_success_url(self):
        ticker = self.object.ticker
        return reverse_lazy("ticker_details", kwargs={"category": ticker.category.title, "pk": ticker.id})


class InflowUpdateView(UpdateView):
    model = Inflow
    template_name = "inflow_update.html"
    form_class = forms.InflowForms

    def get_success_url(self):
        ticker = self.object.ticker
        return reverse_lazy("ticker_details", kwargs={"category": ticker.category.title, "pk": ticker.id})


class InflowDeleteView(DeleteView):
    model = Inflow
    template_name = "inflow_delete.html"


    def get_success_url(self):
        ticker = self.object.ticker
        return reverse_lazy("ticker_details", kwargs={"category": ticker.category.title, "pk": ticker.id})
