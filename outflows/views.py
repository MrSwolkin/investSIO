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
    

class OutflowCreateView(CreateView):
    model = Outflow
    template_name = "outflow_create.html"
    form_class = forms.OutflowForms
    success_url = reverse_lazy("outflow_list")
    

class OutflowUpdateView(UpdateView):
    model = Outflow
    template_name = "outflow_update.html"
    form_class = forms.OutflowForms
    success_url = reverse_lazy("outflow_list")

class OutflowDeleteView(DeleteView):
    model = Outflow
    template_name = "outflow_delete.html"
    success_url = reverse_lazy("outflow_list")