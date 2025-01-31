from django import forms
from . import models

class DividendForm(forms.ModelForm):
    
    class Meta:
        model = models.Dividend
        fields = ["ticker", "value", "date", "quantity_quote"]
        
        widgets = {
            "ticker": forms.Select(attrs={"class": "form-control mt-2"}),
            "value": forms.NumberInput(attrs={"class": "form-control mt-2"}),
            "date": forms.DateInput(attrs={"class": "form-control mt-2"}),
            "quantity_quote": forms.NumberInput(attrs={"class": "form-control mt-2"})
        }
        
        labels = {
            "ticker" : "nome do Ticker",
            "value": "Valor pago por conta", 
            "date": "Data de Pagamento", 
            "quantity_quote": "quantidade de contas"
        }