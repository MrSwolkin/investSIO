from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Ticker
from categories.models import Category
from inflows.models import Inflow
from outflows.models import Outflow
from . import forms


class TickerListView(ListView):
    model = Ticker
    template_name = "ticker_list.html"
    context_object_name = "tickers"
    
    def get_queryset(self):
        category_title = self.kwargs["category"]
        category = Category.objects.get(title=category_title)
        return Ticker.objects.filter(category=category)
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        category_title = self.kwargs["category"]
        context["category_title"] = category_title
        return context


class TickerCreateView(CreateView):
    model = Ticker
    template_name = "ticker_create.html"
    form_class = forms.TickerForms
    success_url = reverse_lazy("tikcer_list")


class TickerDetailsView(DetailView):
    model = Ticker
    template_name = "ticker_details.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ticker_id = self.object.id
        #inflow = Inflow.objects.filter(ticker_id)
        #outflow = Outflow.objects.filter(ticker_id)
        

        
        context["category_title"] = self.kwargs["category"]
        return context


class TickerUpdateView(UpdateView):
    model = Ticker
    template_name = "ticker_update.html"
    form_class = forms.TickerForms
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.object.category.title
        context["category"] = category
        return context

    def get_success_url(self):
        return reverse_lazy("ticker_list", kwargs={"category": self.object.category.title})

class TickerDeleteview(DeleteView):
    model = Ticker
    template_name = "ticker_delete.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.object.category.title
        context["category"] = category
        return context

    def get_success_url(self):
        return reverse_lazy("ticker_list", kwargs={"category": self.object.category.title})
