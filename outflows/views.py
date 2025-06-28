from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Outflow
from . import forms

class OuflowListView(ListView):
    model = Outflow
    template_name = "outflow_list.html"
    context_object_name = "outflows"


class OutflowDetailsView(DetailView):
    model = Outflow
    template_name = "outflow_details.html"
    

class OutflowCreateView(SuccessMessageMixin, CreateView):
    model = Outflow
    template_name = "outflow_create.html"
    form_class = forms.OutflowForms
    success_url = reverse_lazy("outflow_list")
    success_message = "Venda criada com sucesso."
    

class OutflowUpdateView(SuccessMessageMixin, UpdateView):
    model = Outflow
    template_name = "outflow_update.html"
    form_class = forms.OutflowForms
    success_url = reverse_lazy("outflow_list")
    success_message = "Atualização efetuada com sucesso."


class OutflowDeleteView(SuccessMessageMixin, DeleteView):
    model = Outflow
    template_name = "outflow_delete.html"
    success_url = reverse_lazy("outflow_list")
    success_message = "Item deletado com sucesso."