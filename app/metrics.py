from django.utils import timezone
from django.utils.formats import number_format
from dateutil.relativedelta import relativedelta
from django.db.models import Sum
from collections import defaultdict

from categories.models import Category
from inflows.models import Inflow
from outflows.models import Outflow
from dividends.models import Dividend
from brokers.models import Broker, Currency
from tickers.models import Ticker


def get_ticker_metrics(ticker, target_date=None):
    """
    Recebe como argumento um ticker do banco de dados
    e retorna metricas como: total investido, total de cotas, e preco medio.
    """
    inflows = Inflow.objects.filter(ticker=ticker)
    outflows = Outflow.objects.filter(ticker=ticker)

    if target_date:
        inflows = inflows.filter(date__lte=target_date)
        outflows = outflows.filter(date__lte=target_date)

    # Aggregate in single query each
    inflow_totals = inflows.aggregate(
        total_price=Sum("total_price"),
        total_quantity=Sum("quantity")
    )
    outflow_totals = outflows.aggregate(
        total_price=Sum("total_price"),
        total_quantity=Sum("quantity")
    )

    total_price_inflow = inflow_totals["total_price"] or 0
    total_price_outflow = outflow_totals["total_price"] or 0
    total_price = total_price_inflow - total_price_outflow

    total_inflow = inflow_totals["total_quantity"] or 0
    total_outflow = outflow_totals["total_quantity"] or 0
    total_quantity = total_inflow - total_outflow

    avarange_price = total_price / total_quantity if total_quantity else 0

    return dict(
        total_price=round(float(total_price), 2),
        total_quantity=round(float(total_quantity), 2),
        avarange_price=round(float(avarange_price), 2)
    )


def get_total_category_invested(category):
    """
    Recebe como argumento a categoria de investimento, e
    usando a function get_ticker_metrics() para auxiliar no calculo,
    nos retorna o total investido atualmente.
    """
    category_obj = Category.objects.get(title=category)
    tickers = Ticker.objects.filter(category=category_obj).only('id', 'name')

    amount_ticker_by_category = tickers.count()
    total_invested = sum(
        get_ticker_metrics(ticker)["total_price"] for ticker in tickers
    )

    return dict(
        total_invested=number_format(total_invested, decimal_pos=2, force_grouping=True),
        amount_ticker_by_category=amount_ticker_by_category
    )


def chart_total_category_invested():
    """
    Essa funcao se utiliza da funcao 'get_total_category_invested', para nos retornar em um dicionario
    a categoria do ativos e o total investido.
    Tendo como principal objetivo alimentar graficos chartjs.
    """
    categories = Category.objects.all().only('id', 'title')
    data = {
        category.title: get_total_category_invested(category.title)["total_invested"]
        for category in categories
    }
    json_data = {
        key: float(value.replace(".", "").replace(",", "."))
        for key, value in data.items()
    }
    return json_data


def get_total_invested():
    """
    Nos retorna o total investido.
    """
    total_inflow = Inflow.objects.aggregate(
        total=Sum("total_price")
    )["total"] or 0

    return round(float(total_inflow), 2)


def get_total_applied_by_currency():
    """
    Retorna o total aplicado em cada moeda. Principal objetivo alimentar o grafico chartjs.
    """
    # Single query with annotation instead of N queries
    currency_totals = Inflow.objects.values(
        'ticker__currency__code'
    ).annotate(
        total_price=Sum("total_price")
    )

    chart_currency_data = {
        item['ticker__currency__code']: float(item['total_price'] or 0)
        for item in currency_totals
        if item['ticker__currency__code']
    }

    return chart_currency_data


def get_applied_value(currency_code):
    """
    Nos retona o volume mensal aplicado em cada moeda. Necessitando de um argumento que no caso e o codigo
    da moeda ja cadastrada pelo usuario.
    """
    months = ["0", "Jan", "Fev", "Mar", "Abr", "Maio",
              "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]

    inflows_by_year_month = (
        Inflow.objects
        .filter(ticker__currency__code=currency_code)
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
    """
    Tem como objetivo retornar os ultimos 6 meses.
    """
    today = timezone.now().date()
    dates = [(today.replace(day=1) - relativedelta(months=i)) for i in range(6, -1, -1)]
    labels = [d.strftime("%b %Y") for d in dates]
    return dict(labels=labels)


def get_total_dividends_category(category):
    """
    Retorna o total de dividendos por categoria nos ultimos 6 meses.
    """
    today = timezone.now().date()
    dates = [(today.replace(day=1) - relativedelta(months=i)) for i in range(6, -1, -1)]
    months = {d.strftime("%m-%Y"): 0 for d in dates}

    # Single query with join instead of multiple queries
    total_dividends = (
        Dividend.objects
        .filter(
            ticker__category__title=category,
            date__range=[dates[0], today]
        )
        .values("date__year", "date__month")
        .annotate(total=Sum("total_value"))
    )

    for entry in total_dividends:
        key = f"{entry['date__month']:02d}-{entry['date__year']}"
        if key in months:
            months[key] += float(entry["total"] or 0)

    values = [months[d.strftime("%m-%Y")] for d in dates]

    return dict(values=values)


def get_currency(currency):
    """
    Retorna os dividendos mensais de cada tipo de moeda.
    """
    dividends_by_years_month = (
        Dividend.objects
        .filter(currency=currency)
        .values("date__year", "date__month")
        .annotate(total_value=Sum("total_value"))
        .order_by("-date__year", "date__month")
    )

    dividends_dict = defaultdict(lambda: {month: 0 for month in range(1, 13)})
    for entry in dividends_by_years_month:
        year = entry["date__year"]
        month = entry["date__month"]
        dividends_dict[year][month] = float(entry["total_value"] or 0)

    return dict(dividends_dict)


def get_total_applied_by_broker():
    """
    Retorna o total aplicado por corretora.
    """
    # Single query with annotation instead of N queries
    broker_totals = (
        Inflow.objects
        .values('broker__name')
        .annotate(total_price=Sum("total_price"))
    )

    total_in_broker = {
        item['broker__name']: float(item['total_price'] or 0)
        for item in broker_totals
        if item['broker__name']
    }

    return total_in_broker
