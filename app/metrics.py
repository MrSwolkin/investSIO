from django.db.models import Sum
from itertools import chain
from categories.models import Category
from inflows.models import Inflow
from outflows.models import Outflow
from django.utils.formats import number_format

from tickers.models import Ticker

# criar a metrica de ticker
def get_ticker_metrics(ticker):
    '''recebe como argumento um ticker do banco de dados
        e retorna metricas como:
        total investido, total de cotas, e preco medio.
    '''
    inflows = Inflow.objects.filter(ticker=ticker)
    outflows = Outflow.objects.filter(ticker=ticker)    
# total de cotas de um ticker
    total_price_ticker_inflow = inflows.aggregate(Sum("total_price"))["total_price__sum"] or 0
    total_price_ticker_outflow = outflows.aggregate(Sum("total_price"))[
        "total_price__sum"] or 0
    total_price = total_price_ticker_inflow - total_price_ticker_outflow 
# total investido
    total_inflow = inflows.aggregate(Sum("quantity"))["quantity__sum"] or 0
    total_outflow = outflows.aggregate(Sum("quantity"))["quantity__sum"] or 0
    total_quantity = total_inflow - total_outflow 
# preço medio
    avarange_price = total_price / total_quantity if total_quantity else 0

    return dict (
        total_price=round(total_price, 2),
        total_quantity=round(total_quantity, 2),
        avarange_price=round(avarange_price, 2)
    )

def get_total_category_invested(category):
    category_title = Category.objects.get(title=category)
    tickers = Ticker.objects.filter(category=category_title)
    
    total_invested = sum(get_ticker_metrics(ticker)[
                "total_price"] for ticker in tickers)
    return dict(
        total_invested=number_format(total_invested, decimal_pos=2, force_grouping=True)
    )

