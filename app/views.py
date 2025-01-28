from django.shortcuts import render
from inflows.models import Inflow
from outflows.models import Outflow
from itertools import chain

def home(request):
    return render(request, "home.html")

def negociations(request):
    inflow = Inflow.objects.all()
    outflow = Outflow.objects.all()

    transactions = sorted(
        chain(inflow, outflow),
        key=lambda obj:obj.date,
        reverse=True
    )

    context = {
        "transactions": transactions,

    }
    return render(request, "negociations.html",context)