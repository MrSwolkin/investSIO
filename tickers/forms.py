from django import forms
from . import models


class TickerForms(forms.ModelForm):
    
    class Meta:
        model = models.Ticker
        fields = ["name", "category", "currency", "sector", "description"]
        

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control mt-2"}),
            "category": forms.Select(attrs={"class": "form-control mt-2"}),
            "currency": forms.Select(attrs={"class": "form-control mt-2"}),
            "sector": forms.TextInput(attrs={"class": "form-control mt-2"}),
            "description": forms.Textarea(attrs={"class": "form-control mt-2", "rows": 3}),
        }
        
        labels = {
            "name": "Código do Ticker",
            "category": "Categoria",
            "currency": "Moeda",
            "sector": "Setor",
            "description": "Descrição"
        }