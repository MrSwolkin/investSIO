from django.utils import timezone
from django.utils.formats import number_format
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.db.models import Sum
from collections import defaultdict

from categories.models import Category
from inflows.models import Inflow
from outflows.models import Outflow
from dividends.models import Dividend
from brokers.models import Currency


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
    '''Recebe como argumento a categoria de investimento, e 
        usando a function get_ticker_metris() para auxiliar no calculo, 
        nos retorna o total investido atualmente.
    '''
    category_title = Category.objects.get(title=category)
    tickers = Ticker.objects.filter(category=category_title)
    
    total_invested = sum(get_ticker_metrics(ticker)[
                "total_price"] for ticker in tickers)
    return dict(
        total_invested=number_format(total_invested, decimal_pos=2, force_grouping=True)
    )

def get_total_invested():
    inflow = Inflow.objects.all()
    total_inflow = inflow.aggregate(
        Sum("total_price"))["total_price__sum"] or 0
    
    return(round(total_inflow, 2))

def get_total_applied_by_currency():
    currencies = Currency.objects.all()
    
    return {currency.code: Inflow.objects.filter(ticker__currency=currency).aggregate(total_price=Sum("total_price"))["total_price"] or 0 for currency in currencies}


def get_applied_value(currency_code):
    months = ["0","Jan", "Fev", "Mar", "Abr", "Maio",
                "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]

    currency = Currency.objects.get(code=currency_code)    

    inflows_by_year_month = (Inflow.objects.filter(ticker__currency=currency)
        .values("date__year", "date__month")
        .annotate(total_price=Sum("total_price"))
        .order_by("date__year", "date__month")
    
    )
    labels = []
    values = []
    for item in inflows_by_year_month:
        month = months[item["date__month"]]
        year = item["date__year"]
        labels.append(f"{month} {year}")
        values.append(float(item["total_price"] or 0))
    
    return dict(
        labels=labels,
        values=values
    )

def get_last_six_month():
    today = timezone.now().date()
    dates = [(today.replace(day=1) - relativedelta(months=i)) for i in range(6, -1, -1)]
    labels = [d.strftime("%b %Y") for d in dates]
    return dict(
        labels=labels
        )

def get_total_dividends_category(category):
    today = timezone.now().date()
    dates = [(today.replace(day=1) - relativedelta(months=i)) for i in range(6, -1, -1)]
    months = {d.strftime("%m-%Y"): 0 for d in dates}


    category_title = Category.objects.get(title=category)
    #filtro dividends por ticker 
    tickers = Ticker.objects.filter(category=category_title)

    total_dividends = Dividend.objects.filter(
        ticker__in=tickers, date__range=[dates[1], today]).values("date__year", "date__month").annotate(total=Sum("total_value"))

    for entry in total_dividends:
        # Ex: "02-2025"
        key = f"{entry['date__month']:02d}-{entry['date__year']}"
        if key in months:
            months[key] += float(entry["total"])

    values = [months[d.strftime("%m-%Y")] for d in dates]


    return dict(
            values=values    
        )

def get_currency(currency):
    dividends_by_years_month = Dividend.objects.filter(currency=currency).values(
        "date__year", "date__month").annotate(total_value=Sum("total_value")).order_by("-date__year", "date__month")
    dividends_dict = defaultdict(
        lambda: {month: 0 for month in range(1, 13)})
    for entry in dividends_by_years_month:
        year = entry["date__year"]
        month = entry["date__month"]
        dividends_dict[year][month] = entry["total_value"]
    return dict(dividends_dict)
