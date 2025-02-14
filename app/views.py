import json
from django.shortcuts import render
from inflows.models import Inflow
from outflows.models import Outflow
from itertools import chain
from . import metrics

def home(request):
    total_inflows = metrics.get_total_invested()
    inflows_datas = metrics.get_applied_value()
    last_six_months = metrics.get_last_six_month()
    total_dividends_fiis = metrics.get_total_dividends_category("FII")
    total_dividends_acoes = metrics.get_total_dividends_category("Ação")
    total_dividends_stocks = metrics.get_total_dividends_category("Stock")
    print(total_dividends_fiis)
    print(total_dividends_acoes)
    print(total_dividends_stocks)
    context = {
        "last_six_months": json.dumps(last_six_months),
        "total_inflows": total_inflows,
        "inflows_datas": json.dumps(inflows_datas),
        "total_fiis": json.dumps(total_dividends_fiis),
        "total_acoes": json.dumps(total_dividends_acoes),
        "total_stocks": json.dumps(total_dividends_stocks),
        
    }

    return render(request, "home.html", context)

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