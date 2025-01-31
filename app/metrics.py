from django.db.models import Sum
from itertools import chain
from inflows.models import Inflow
from outflows.models import Outflow

# criar a metrica de 
def get_ticker_metrics(ticker):
    inflows = Inflow.objects.filter(ticker=ticker)
    outflows = Outflow.objects.filter(ticker=ticker)    

    total_inflow = inflows.aggregate(Sum("quantity"))["quantity__sum"] or 0
    total_outflow = outflows.aggregate(Sum("quantity"))["quantity__sum"] or 0
    total_quantity = total_inflow - total_outflow
    

    return {
        "total_quantity": total_quantity,
    }

#total de cotas de um ticker
#total investido 
# preço medio