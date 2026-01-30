from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from itertools import chain
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from services.get_ticker_details import Get_ticker_data
from .models import Ticker
from app import metrics
from app.utils.validators import validate_category_title
from categories.models import Category
from inflows.models import Inflow
from outflows.models import Outflow
from . import forms

get_ticker_details = Get_ticker_data()


class TickerListView(LoginRequiredMixin, ListView):
    model = Ticker
    template_name = "ticker_list.html"
    context_object_name = "tickers"

    def get_queryset(self):
        # Validate category parameter and get object or 404
        category_title = validate_category_title(self.kwargs.get("category"))
        category = get_object_or_404(Category, title=category_title)
        return Ticker.objects.filter(category=category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_title = validate_category_title(self.kwargs.get("category"))

        context["category_title"] = category_title
        context["metrics_category"] = metrics.get_total_category_invested(category_title)

        return context


class TickerCreateView(LoginRequiredMixin, CreateView):
    model = Ticker
    template_name = "ticker_create.html"
    form_class = forms.TickerForms

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Validate category parameter
        category = validate_category_title(self.kwargs.get("category"))
        context["category"] = category

        return context

    def get_success_url(self):
        category = validate_category_title(self.kwargs.get("category"))
        return reverse_lazy("ticker_list", kwargs={"category": category})


class TickerDetailsView(LoginRequiredMixin, DetailView):
    model = Ticker
    template_name = "ticker_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Validate category parameter
        category_title = validate_category_title(self.kwargs.get("category"))

        inflows = Inflow.objects.filter(ticker=self.object)
        outflows = Outflow.objects.filter(ticker=self.object)
        ticker_details_api = get_ticker_details.get_ticker(code_ticekr=self.object)

        transactions = sorted(
            chain(inflows, outflows),
            key=lambda obj: obj.date,
            reverse=True
        )

        context["category_title"] = category_title
        context["inflows"] = inflows
        context["outflows"] = outflows
        context["transactions"] = transactions
        context["ticker_metrics"] = metrics.get_ticker_metrics(self.object)
        context["ticker_price"] = ticker_details_api["regularMarketPrice"]
        context["ticker_icon_url"] = ticker_details_api["logourl"]
        context["ticker_long_name"] = ticker_details_api["longName"]
        return context


class TickerUpdateView(LoginRequiredMixin, UpdateView):
    model = Ticker
    template_name = "ticker_update.html"
    form_class = forms.TickerForms
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.object.category.title
        context["category"] = category
        return context

    def get_success_url(self):
        return reverse_lazy("ticker_details", kwargs={"category": self.object.category.title, "pk": self.object.id})

class TickerDeleteView(LoginRequiredMixin, DeleteView):
    model = Ticker
    template_name = "ticker_delete.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.object.category.title
        context["category"] = category
        return context

    def get_success_url(self):
        return reverse_lazy("ticker_details", kwargs={"category": self.object.category.title, "pk": self.object.id})
