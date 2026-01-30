from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Inflow
from . import forms


class InflowListView(LoginRequiredMixin, ListView):
    model = Inflow
    template_name = "inflow_list.html"
    context_object_name = "inflows"
    
    def get_queryset(self):
        queryset =  super().get_queryset()
        ticker = self.request.GET.get("ticker")
        #if ticker:
        #   queryset = queryset.filter(ticker__name__icontains=ticker)

        return queryset

class InflowDetailsView(LoginRequiredMixin, DetailView):
    model = Inflow
    template_name = "inflow_details.html"


class InflowCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Inflow
    template_name = "inflow_create.html"
    form_class = forms.InflowForms
    success_message = "Compra criada com sucesso."

    def get_success_url(self):
        ticker = self.object.ticker
        return reverse_lazy("ticker_details", kwargs={"category": ticker.category.title, "pk": ticker.id})


class InflowUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Inflow
    template_name = "inflow_update.html"
    form_class = forms.InflowForms
    success_message = "Atualização ralizada com sucesso."

    def get_success_url(self):
        ticker = self.object.ticker
        return reverse_lazy("ticker_details", kwargs={"category": ticker.category.title, "pk": ticker.id})


class InflowDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Inflow
    template_name = "inflow_delete.html"
    success_message = "Item deletado com sucesso."

    def get_success_url(self):
        ticker = self.object.ticker
        return reverse_lazy("ticker_details", kwargs={"category": ticker.category.title, "pk": ticker.id})
