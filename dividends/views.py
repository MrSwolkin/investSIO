from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from . import models, forms


class DividendListView(ListView):
    model = models.Dividend
    template_name = "dividend_list.html"
    context_object_name = "dividends"
    
    def get_queryset(self):
        queryset =  super().get_queryset()
        ticker = self.request.GET.get("ticker")
        if ticker:
            queryset = queryset.filter(ticker__icontains=ticker)

        return queryset


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