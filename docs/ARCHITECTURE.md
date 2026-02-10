# Arquitetura do Projeto

Estrutura e organizacao do projeto InvestSIO.

## Estrutura de Diretorios

```
investSIO/
├── app/                          # Projeto principal Django
│   ├── settings/                 # Settings separados por ambiente
│   │   ├── __init__.py
│   │   ├── base.py               # Configuracoes comuns
│   │   ├── dev.py                # Desenvolvimento
│   │   ├── prod.py               # Producao
│   │   └── test.py               # Testes
│   ├── urls.py                   # URLs raiz
│   ├── views.py                  # Views principais (home, negociations)
│   ├── metrics.py                # Funcoes de calculo e metricas
│   ├── widgets.py                # Widgets customizados para forms
│   ├── utils/                    # Utilitarios
│   │   └── validators.py         # Validadores de input
│   ├── templates/
│   │   ├── base.html             # Template base
│   │   ├── home.html             # Dashboard
│   │   ├── negociations.html     # Lista de transacoes
│   │   ├── registration/         # Templates de autenticacao
│   │   ├── errors/               # Templates de erro (404, 500)
│   │   └── components/           # Componentes reutilizaveis
│   │       ├── _header.html
│   │       ├── _sidebar.html
│   │       ├── _footer.html
│   │       ├── _pagination.html
│   │       ├── ui/               # Componentes UI
│   │       │   ├── _button.html
│   │       │   ├── _card.html
│   │       │   ├── _metric_card.html
│   │       │   ├── _badge.html
│   │       │   ├── _table.html
│   │       │   ├── _modal.html
│   │       │   ├── _alert.html
│   │       │   └── _empty_state.html
│   │       └── forms/            # Componentes de formulario
│   │           └── _form_field.html
│   ├── tests/                    # Testes do app principal
│   │   ├── __init__.py
│   │   ├── test_views.py
│   │   └── test_auth.py
│   ├── asgi.py
│   └── wsgi.py
│
├── brokers/                      # App de Corretoras
│   ├── models.py                 # Models: Broker, Currency
│   ├── views.py                  # CBVs de CRUD
│   ├── forms.py                  # BrokerForm
│   ├── urls.py                   # URLs do app
│   ├── admin.py                  # Registro no admin
│   ├── tests.py                  # Testes do app
│   └── templates/                # Templates do app
│
├── tickers/                      # App de Ativos
│   ├── models.py                 # Model: Ticker
│   ├── views.py                  # CBVs de CRUD
│   ├── forms.py                  # TickerForms
│   ├── urls.py                   # URLs do app
│   ├── tests.py                  # Testes do app
│   └── templates/                # Templates do app
│
├── inflows/                      # App de Compras
│   ├── models.py                 # Model: Inflow
│   ├── views.py                  # CBVs de CRUD
│   ├── forms.py                  # InflowForms
│   ├── urls.py                   # URLs do app
│   ├── tests.py                  # Testes do app
│   └── templates/                # Templates do app
│
├── outflows/                     # App de Vendas
│   ├── models.py                 # Model: Outflow
│   ├── views.py                  # CBVs de CRUD
│   ├── forms.py                  # OutflowForms
│   ├── urls.py                   # URLs do app
│   ├── tests.py                  # Testes do app
│   └── templates/                # Templates do app
│
├── dividends/                    # App de Dividendos
│   ├── models.py                 # Models: Dividend, DeclaredDividend
│   ├── views.py                  # CBVs de CRUD
│   ├── forms.py                  # DividendForm
│   ├── urls.py                   # URLs do app
│   ├── tests.py                  # Testes do app
│   └── templates/                # Templates do app
│
├── categories/                   # App de Categorias
│   ├── models.py                 # Model: Category
│   ├── tests.py                  # Testes do app
│   └── admin.py                  # Registro no admin
│
├── services/                     # Servicos externos
│   ├── fees_br.py                # Consulta taxas (IPCA, SELIC, CDI)
│   └── get_ticker_details.py     # Consulta dados de tickers
│
├── theme/                        # App TailwindCSS
│   ├── static_src/
│   │   └── src/
│   │       └── styles.css        # Design System CSS
│   └── static/
│       └── css/
│           └── dist/
│               └── styles.css    # CSS compilado
│
├── logs/                         # Logs da aplicacao (git ignored)
├── docs/                         # Documentacao
│   ├── GETTING_STARTED.md
│   ├── ARCHITECTURE.md
│   ├── DESIGN_SYSTEM.md
│   ├── MODELS.md
│   └── BACKEND_IMPROVEMENTS.md
│
├── manage.py
├── pytest.ini                    # Configuracao do pytest
├── conftest.py                   # Fixtures globais
├── db.sqlite3                    # Banco de dados SQLite (dev)
├── requirements.txt              # Dependencias Python
├── CHANGELOG.md                  # Historico de mudancas
└── venv/                         # Ambiente virtual
```

## Apps e Responsabilidades

### app (Projeto Principal)
- Configuracoes globais do Django
- URLs raiz e inclusao de URLs dos apps
- Views principais: Dashboard e Negociacoes
- Funcoes de metricas agregadas
- Template base e componentes compartilhados
- Widgets customizados para formularios
- Validadores de input

### brokers
- Gerenciamento de corretoras
- Gerenciamento de moedas (Currency)
- CRUD completo com 5 templates

### tickers
- Gerenciamento de ativos (Acoes, FIIs, Stocks, ETFs)
- Integracao com API para dados em tempo real
- CRUD completo com 5 templates

### inflows
- Registro de compras e subscricoes
- Calculo automatico de total
- CRUD completo com 5 templates

### outflows
- Registro de vendas
- Calculo automatico de total
- CRUD completo com 5 templates

### dividends
- Registro de dividendos recebidos
- Calculo automatico de quantidade de cotas
- Suporte a tipos: Dividendos, JCP, Amortizacao
- CRUD completo com 5 templates

### categories
- Categorias de ativos (FII, Acao, Stock, ETF)
- Gerenciado via Admin Django

### services
- Integracao com BrasilAPI (taxas economicas)
- Integracao com BrAPI (dados de tickers)

### theme
- Configuracao do TailwindCSS
- Design System e componentes CSS

## Padrao de Views

Todas as apps usam Class-Based Views (CBV) do Django com LoginRequiredMixin:

```python
from django.contrib.auth.mixins import LoginRequiredMixin

class BrokerListView(LoginRequiredMixin, ListView):
    model = Broker
    template_name = "broker_list.html"
    context_object_name = "brokers"
    paginate_by = 25
```

Padrao de nomenclatura:
```python
<Model>ListView      # Lista de registros
<Model>CreateView    # Criacao de registro
<Model>DetailsView   # Detalhes do registro
<Model>UpdateView    # Edicao de registro
<Model>DeleteView    # Exclusao de registro
```

## Padrao de URLs

```python
# Padrao de nomenclatura de URLs
<app>/list/              # Lista
<app>/create/            # Criacao
<app>/<id>/details/      # Detalhes
<app>/<id>/update/       # Edicao
<app>/<id>/delete/       # Exclusao
```

## Padrao de Templates

```
templates/
├── <model>_list.html      # Lista de registros
├── <model>_create.html    # Formulario de criacao
├── <model>_details.html   # Detalhes do registro
├── <model>_update.html    # Formulario de edicao
└── <model>_delete.html    # Confirmacao de exclusao
```

## Componentes UI

Componentes reutilizaveis via `{% include %}`:

```django
{% include "components/ui/_button.html" with text="Salvar" variant="primary" %}
{% include "components/ui/_badge.html" with text="Ativo" variant="success" %}
{% include "components/ui/_metric_card.html" with value="R$ 1.000" label="Total" %}
```

## Relacionamentos entre Models

```
Currency (brokers)
├── → Broker
└── → Ticker

Category (categories)
└── → Ticker

Broker (brokers)
├── → Inflow
└── → Outflow

Ticker (tickers)
├── → Inflow
├── → Outflow
└── → Dividend
```

## Autenticacao

Todas as views requerem autenticacao via `LoginRequiredMixin` ou `@login_required`:

```python
# CBV
class ProtectedView(LoginRequiredMixin, View):
    login_url = '/login/'

# FBV
@login_required
def protected_view(request):
    pass
```

## Cache

O projeto usa Redis para cache em producao:

```python
# Invalidar cache apos criar/atualizar dados
from django.core.cache import cache
cache.delete('dashboard_metrics')
```

## Logging

Logs estruturados em `logs/` (development) e console (production):

```python
import logging
logger = logging.getLogger(__name__)

logger.info("Operacao realizada com sucesso")
logger.error("Erro ao processar requisicao", exc_info=True)
```
