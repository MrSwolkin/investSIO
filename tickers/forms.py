from django import forms
from app.widgets import TailwindTextInput, TailwindSelect, TailwindTextarea
from . import models


class TickerForms(forms.ModelForm):

    class Meta:
        model = models.Ticker
        fields = ["name", "category", "currency", "sector", "description"]

        widgets = {
            "name": TailwindTextInput(),
            "category": TailwindSelect(),
            "currency": TailwindSelect(),
            "sector": TailwindTextInput(),
            "description": TailwindTextarea(),
        }

        labels = {
            "name": "Código do Ticker",
            "category": "Categoria",
            "currency": "Moeda",
            "sector": "Setor",
            "description": "Descrição"
        }
        
