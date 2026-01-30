from django import forms
from app.widgets import TailwindSelect, TailwindNumberInput, TailwindDateInput
from . import models

class DividendForm(forms.ModelForm):

    class Meta:
        model = models.Dividend
        fields = ["ticker", "value", "date", "income_type", "currency"]

        widgets = {
            "ticker": TailwindSelect(),
            "value": TailwindNumberInput(),
            "date": TailwindDateInput(),
            #"quantity_quote": TailwindNumberInput(attrs={"placeholder": "Cálculo automático"}),
            "income_type": TailwindSelect(),
            "currency": TailwindSelect(),
        }

        labels = {
            "ticker": "nome do Ticker",
            "income_type": "Tipo de rendimento",
            "value": "Valor pago por conta",
            "date": "Data de Pagamento",
            #"quantity_quote": "quantidade de contas"
            "currency": "Moeda",
        }