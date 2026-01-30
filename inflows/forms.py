from django import forms
from app.widgets import TailwindSelect, TailwindNumberInput, TailwindDateInput
from . import models


class InflowForms(forms.ModelForm):

    class Meta:
        model = models.Inflow
        fields = ["ticker", "date", "type", "broker", "cost_price", "quantity", "tax"]

        widgets = {
            "ticker": TailwindSelect(),
            "broker": TailwindSelect(),
            "type": TailwindSelect(),
            "cost_price": TailwindNumberInput(),
            "quantity": TailwindNumberInput(),
            "date": TailwindDateInput(attrs={"placeholder": "DD/MM/AAAA"}),
            "tax": TailwindNumberInput(),
        }

        labels = {
            "ticker": "Ticker",
            "date": "Data",
            "type": "Compra ou Subscrição",
            "cost_price": "Preço por cota",
            "quantity": "Quantidade de cotas",
            "broker": "Corretora",
            "tax": "Taxa",
        }
