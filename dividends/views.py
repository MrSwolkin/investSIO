from django.db.models import Sum
from collections import defaultdict
from django.db.models.functions import ExtractMonth, ExtractYear
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from . import models, forms
from app import metrics


class DividendListView(ListView):
    model = models.Dividend
    template_name = "dividend_list.html"
    context_object_name = "dividends"

    def get_queryset(self):
        queryset = super().get_queryset()
        ticker = self.request.GET.get("ticker")
        month = self.request.GET.get("month")
        year = self.request.GET.get("year")
        currency = self.request.GET.get("currency")
        
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
        currency = self.request.GET.get("currency", "BRL")
        context["anos"] = [data.year for data in anos]
    
        context["meses"] = {
            1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
            5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
            9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
        }
        
            
        context["dividends_by_year_and_month"] = metrics.get_currency(currency)
        context["selected_currency"] = currency
        print(context["selected_currency"])
        return context


class DividendCreateView(CreateView):
    model = models.Dividend
    template_name = "dividend_create.html"
    form_class = forms.DividendForm
    success_url = reverse_lazy("dividend_list")


class DividendUpdateView(UpdateView):
    model = models.Dividend
    template_name = "dividend_update.html"
    form_class = forms.DividendForm
    success_url = reverse_lazy("dividend_list")


class DividendDeleteView(DeleteView):
    model = models.Dividend
    template_name = "dividend_delete.html"
    success_url = reverse_lazy("dividend_list")
    
