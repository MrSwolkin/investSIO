from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from collections import defaultdict
from django.db.models.functions import ExtractMonth, ExtractYear
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from . import models, forms
from app import metrics
from app.utils.validators import (
    validate_ticker_name,
    validate_year,
    validate_month,
    validate_currency_code,
)


class DividendListView(LoginRequiredMixin, ListView):
    model = models.Dividend
    template_name = "dividend_list.html"
    context_object_name = "dividends"

    def get_queryset(self):
        queryset = super().get_queryset().select_related(
            'ticker',
            'ticker__category',
            'ticker__currency'
        )

        # Validate and sanitize input parameters
        ticker = validate_ticker_name(self.request.GET.get("ticker"))
        year = validate_year(self.request.GET.get("year"))
        month = validate_month(self.request.GET.get("month"))
        currency = validate_currency_code(self.request.GET.get("currency"))

        if ticker:
            queryset = queryset.filter(ticker__name=ticker)

        if year:
            queryset = queryset.filter(date__year=year)

        if month:
            queryset = queryset.filter(date__month=month)

        if currency:
            queryset = queryset.filter(currency=currency)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        anos = models.Dividend.objects.dates("date", "year", order="DESC")
        currency = validate_currency_code(self.request.GET.get("currency")) or "BRL"
        context["anos"] = [data.year for data in anos]

        context["meses"] = {
            1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
            5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
            9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
        }

        context["dividends_by_year_and_month"] = metrics.get_currency(currency)
        context["selected_currency"] = currency
        return context


class DividendCreateView(LoginRequiredMixin, CreateView):
    model = models.Dividend
    template_name = "dividend_create.html"
    form_class = forms.DividendForm
    success_url = reverse_lazy("dividend_list")


class DividendUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Dividend
    template_name = "dividend_update.html"
    form_class = forms.DividendForm
    success_url = reverse_lazy("dividend_list")

    def get_queryset(self):
        return super().get_queryset().select_related('ticker')


class DividendDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Dividend
    template_name = "dividend_delete.html"
    success_url = reverse_lazy("dividend_list")

    def get_queryset(self):
        return super().get_queryset().select_related('ticker')
