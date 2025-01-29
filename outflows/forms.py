from django import forms
from . import models


class OutflowForms(forms.ModelForm):

    class Meta:
        model = models.Outflow
        fields = ["ticker", "broker", "cost_price", "quantity", "date", "tax"]

        widgets = {
            "ticker": forms.Select(attrs={"class": "form-control mt-2"}),
            "broker": forms.Select(attrs={"class": "form-control mt-2"}),
            "cost_price": forms.NumberInput(attrs={"class": "form-control mt-2"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control mt-2"}),
            "date": forms.DateInput(attrs={"class": "form-control mt-2", "placeholder": "MM/DD/AAAA"}),
            "tax": forms.NumberInput(attrs={"class": "form-control mt-2"}),
        }

        labels = {
            "ticker": "Ticker",
            "broker": "Corretora",
            "cost_price": "Preço por cota",
            "quantity": "Quantidade de cotas",
            "date": "Data",
            "tax": "Taxa",
        }
