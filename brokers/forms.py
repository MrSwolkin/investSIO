from django import forms
from . import models

class brokerForm(forms.ModelForm):
    
    class Meta:
        model = models.Broker
        fields = ["name", "account_number", "country", "currency", "description"]        

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control mt-2"}),
            "account_number": forms.NumberInput(attrs={"class": "form-control mt-2"}),
            "country": forms.TextInput(attrs={"class": "form-control mt-2"}),
            "currency": forms.Select(attrs={"class": "form-control mt-2"}),
            "description": forms.Textarea(attrs={"class": "form-control mt-2", "rows": 3}),
        }
        
        labels = {
            "name": "Nome da corretora",
            "account_number": "N° da conta", 
            "country": "Pais", 
            "currency": "Moeda", 
            "description": "Descrição"
        }