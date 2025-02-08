from django.db.models import Sum
from collections import defaultdict
from django.db.models.functions import ExtractMonth, ExtractYear
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from . import models, forms


class DividendListView(ListView):
    model = models.Dividend
    template_name = "dividend_list.html"
    context_object_name = "dividends"

    def get_queryset(self):
        queryset = super().get_queryset()
        ticker = self.request.GET.get("ticker")
        month = self.request.GET.get("month")
        year = self.request.GET.get("year")
        
        if ticker:
            queryset = queryset.filter(ticker__name=ticker)
            
        if year:
            queryset = queryset.filter(date__year=year)
        
        if month:
            queryset = queryset.filter(date__month=month)

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        anos = models.Dividend.objects.dates("date", "year", order="DESC")
        meses = models.Dividend.objects.dates("date", "month", order="DESC")
        context["anos"] = [data.year for data in anos]
    
        context["meses"] = {
            1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
            5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
            9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
        }
        #agregando os dividendos
        dividends_by_years_month = models.Dividend.objects.values("date__year", "date__month").annotate(total_value=Sum("total_value")).order_by("-date__year", "date__month")
        dividends_dict = defaultdict(
            lambda: {month: 0 for month in range(1, 13)})
        for entry in dividends_by_years_month:
            year = entry["date__year"]
            month = entry["date__month"]
            dividends_dict[year][month] = entry["total_value"]
        context["dividends_by_year_and_month"] = dict(dividends_dict)
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