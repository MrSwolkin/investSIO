from django import forms
from app.widgets import TailwindSelect, TailwindNumberInput, TailwindDateInput
from . import models


class OutflowForms(forms.ModelForm):

    class Meta:
        model = models.Outflow
        fields = ["ticker", "broker", "cost_price", "quantity", "date", "tax"]

        widgets = {
            "ticker": TailwindSelect(),
            "broker": TailwindSelect(),
            "cost_price": TailwindNumberInput(),
            "quantity": TailwindNumberInput(),
            "date": TailwindDateInput(attrs={"placeholder": "MM/DD/AAAA"}),
            "tax": TailwindNumberInput(),
        }

        labels = {
            "ticker": "Ticker",
            "date": "Data",
            "cost_price": "Preço por cota",
            "quantity": "Quantidade de cotas",
            "broker": "Corretora",
            "tax": "Taxa",
        }
