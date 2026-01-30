from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Outflow
from . import forms


class OutflowListView(LoginRequiredMixin, ListView):
    model = Outflow
    template_name = "outflow_list.html"
    context_object_name = "outflows"

    def get_queryset(self):
        return super().get_queryset().select_related(
            'ticker',
            'ticker__category',
            'ticker__currency',
            'broker',
            'broker__currency'
        )


class OutflowDetailsView(LoginRequiredMixin, DetailView):
    model = Outflow
    template_name = "outflow_details.html"

    def get_queryset(self):
        return super().get_queryset().select_related(
            'ticker',
            'ticker__category',
            'broker'
        )


class OutflowCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Outflow
    template_name = "outflow_create.html"
    form_class = forms.OutflowForms
    success_url = reverse_lazy("outflow_list")
    success_message = "Venda criada com sucesso."


class OutflowUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Outflow
    template_name = "outflow_update.html"
    form_class = forms.OutflowForms
    success_url = reverse_lazy("outflow_list")
    success_message = "Atualização efetuada com sucesso."

    def get_queryset(self):
        return super().get_queryset().select_related('ticker', 'broker')


class OutflowDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Outflow
    template_name = "outflow_delete.html"
    success_url = reverse_lazy("outflow_list")
    success_message = "Item deletado com sucesso."

    def get_queryset(self):
        return super().get_queryset().select_related('ticker', 'broker')
