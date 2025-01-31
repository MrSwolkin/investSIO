from django import forms
from . import models


class InflowForms(forms.ModelForm):

    class Meta:
        model = models.Inflow
        fields = ["ticker", "date", "type", "broker", "cost_price", "quantity", "tax"]

        widgets = {
            "ticker": forms.Select(attrs={"class": "form-control mt-2"}),
            "broker": forms.Select(attrs={"class": "form-control mt-2"}),
            "type": forms.Select(attrs={"class": "form-control mt-2"}),
            "cost_price": forms.NumberInput(attrs={"class": "form-control mt-2"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control mt-2"}),
            "date": forms.DateInput(attrs={"class": "form-control mt-2", "placeholder": "DD/MM/AAAA"}),
            "tax": forms.NumberInput(attrs={"class": "form-control mt-2"}),
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
