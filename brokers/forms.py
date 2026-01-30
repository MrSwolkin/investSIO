from django import forms
from app.widgets import TailwindTextInput, TailwindSelect, TailwindTextarea
from . import models

class brokerForm(forms.ModelForm):

    class Meta:
        model = models.Broker
        fields = ["name", "account_number", "country", "currency", "description"]

        widgets = {
            "name": TailwindTextInput(),
            "account_number": TailwindTextInput(),
            "country": TailwindTextInput(),
            "currency": TailwindSelect(),
            "description": TailwindTextarea(),
        }

        labels = {
            "name": "Nome da corretora",
            "account_number": "N° da conta",
            "country": "Pais",
            "currency": "Moeda",
            "description": "Descrição"
        }