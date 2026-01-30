from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Inflow
from . import forms
from tickers.models import Ticker
from brokers.models import Broker


class InflowListView(LoginRequiredMixin, ListView):
    model = Inflow
    template_name = "inflow_list.html"
    context_object_name = "inflows"
    paginate_by = 25

    def get_queryset(self):
        queryset = super().get_queryset().select_related(
            'ticker',
            'ticker__category',
            'ticker__currency',
            'broker',
            'broker__currency'
        )

        # Filter by ticker
        ticker_id = self.request.GET.get("ticker")
        if ticker_id:
            queryset = queryset.filter(ticker_id=ticker_id)

        # Filter by broker
        broker_id = self.request.GET.get("broker")
        if broker_id:
            queryset = queryset.filter(broker_id=broker_id)

        # Filter by date range
        date_from = self.request.GET.get("date_from")
        if date_from:
            queryset = queryset.filter(date__gte=date_from)

        date_to = self.request.GET.get("date_to")
        if date_to:
            queryset = queryset.filter(date__lte=date_to)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add tickers and brokers for filter dropdowns
        context['tickers'] = Ticker.objects.all().order_by('symbol')
        context['brokers'] = Broker.objects.all().order_by('name')
        return context


class InflowDetailsView(LoginRequiredMixin, DetailView):
    model = Inflow
    template_name = "inflow_details.html"

    def get_queryset(self):
        return super().get_queryset().select_related(
            'ticker',
            'ticker__category',
            'broker'
        )


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

    def get_queryset(self):
        return super().get_queryset().select_related('ticker', 'ticker__category', 'broker')

    def get_success_url(self):
        ticker = self.object.ticker
        return reverse_lazy("ticker_details", kwargs={"category": ticker.category.title, "pk": ticker.id})


class InflowDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Inflow
    template_name = "inflow_delete.html"
    success_message = "Item deletado com sucesso."

    def get_queryset(self):
        return super().get_queryset().select_related('ticker', 'ticker__category', 'broker')

    def get_success_url(self):
        ticker = self.object.ticker
        return reverse_lazy("ticker_details", kwargs={"category": ticker.category.title, "pk": ticker.id})
