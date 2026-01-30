import json
import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from inflows.models import Inflow
from outflows.models import Outflow
from services.fees_br import GetFeeBr
from itertools import chain
from . import metrics

logger = logging.getLogger('app')
get_fee = GetFeeBr()


@login_required
def home(request):
    logger.info(f"Usuario {request.user.username} acessando dashboard")

    try:
        total_inflows = metrics.get_total_invested()
        inflows_datas = metrics.get_applied_value("BRL")
        last_six_months = metrics.get_last_six_month()
        total_dividends_fiis = metrics.get_total_dividends_category("FII")
        total_dividends_acoes = metrics.get_total_dividends_category("Ação")
        total_dividends_stocks = metrics.get_total_dividends_category("Stock")
        total_dividends_etfs = metrics.get_total_dividends_category("ETF")
        total_applied = metrics.get_total_applied_by_currency()
        chart_diversity = metrics.chart_total_category_invested()
        brokers = metrics.get_total_applied_by_broker()

        # Busca taxas com tratamento de erro
        ipca = get_fee.get_taxa("IPCA")
        selic = get_fee.get_taxa("SELIC")
        cdi = get_fee.get_taxa("CDI")

        context = {
            "total_inflows": total_inflows,
            "total_applied": total_applied,
            "last_six_months": json.dumps(last_six_months),
            "inflows_datas": json.dumps(inflows_datas),
            "total_fiis": json.dumps(total_dividends_fiis),
            "total_acoes": json.dumps(total_dividends_acoes),
            "total_stocks": json.dumps(total_dividends_stocks),
            "total_etfs": json.dumps(total_dividends_etfs),
            "chart_diversity": json.dumps(chart_diversity),
            "chart_total_applied": json.dumps(total_applied),
            "chart_broker": json.dumps(brokers),
            "ipca": ipca.get("valor"),
            "selic": selic.get("valor"),
            "cdi": cdi.get("valor"),
        }

        logger.debug(f"Dashboard carregado com sucesso para {request.user.username}")
        return render(request, "home.html", context)

    except Exception as e:
        logger.exception(f"Erro ao carregar dashboard para {request.user.username}: {str(e)}")
        return render(request, "errors/500.html", status=500)


@login_required
def negociations(request):
    logger.info(f"Usuario {request.user.username} acessando negociacoes")

    try:
        inflow = Inflow.objects.all()
        outflow = Outflow.objects.all()

        transactions = sorted(
            chain(inflow, outflow),
            key=lambda obj: obj.date,
            reverse=True
        )

        context = {
            "transactions": transactions,
        }

        logger.debug(f"Negociacoes carregadas: {len(transactions)} transacoes")
        return render(request, "negociations.html", context)

    except Exception as e:
        logger.exception(f"Erro ao carregar negociacoes para {request.user.username}: {str(e)}")
        return render(request, "errors/500.html", status=500)


def handler404(request, exception):
    """Handler customizado para erros 404."""
    logger.warning(f"Pagina nao encontrada: {request.path}")
    return render(request, "errors/404.html", status=404)


def handler500(request):
    """Handler customizado para erros 500."""
    logger.error(f"Erro interno do servidor: {request.path}")
    return render(request, "errors/500.html", status=500)
