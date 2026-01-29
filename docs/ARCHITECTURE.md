# Arquitetura do Projeto

Estrutura e organizacao do projeto InvestSIO.

## Estrutura de Diretorios

```
investSIO/
├── app/                          # Projeto principal Django
│   ├── settings.py               # Configuracoes do Django
│   ├── urls.py                   # URLs raiz
│   ├── views.py                  # Views principais (home, negociations)
│   ├── metrics.py                # Funcoes de calculo e metricas
│   ├── templates/
│   │   ├── base.html             # Template base
│   │   ├── home.html             # Dashboard
│   │   ├── negociations.html     # Lista de transacoes
│   │   └── components/           # Componentes reutilizaveis
│   ├── asgi.py
│   └── wsgi.py
│
├── brokers/                      # App de Corretoras
│   ├── models.py                 # Models: Broker, Currency
│   ├── views.py                  # CBVs de CRUD
│   ├── forms.py                  # BrokerForm
│   ├── urls.py                   # URLs do app
│   ├── admin.py                  # Registro no admin
│   └── templates/                # Templates do app
│
├── tickers/                      # App de Ativos
│   ├── models.py                 # Model: Ticker
│   ├── views.py                  # CBVs de CRUD
│   ├── forms.py                  # TickerForms
│   ├── urls.py                   # URLs do app
│   └── templates/                # Templates do app
│
├── inflows/                      # App de Compras
│   ├── models.py                 # Model: Inflow
│   ├── views.py                  # CBVs de CRUD
│   ├── forms.py                  # InflowForms
│   ├── urls.py                   # URLs do app
│   └── templates/                # Templates do app
│
├── outflows/                     # App de Vendas
│   ├── models.py                 # Model: Outflow
│   ├── views.py                  # CBVs de CRUD
│   ├── forms.py                  # OutflowForms
│   ├── urls.py                   # URLs do app
│   └── templates/                # Templates do app
│
├── dividends/                    # App de Dividendos
│   ├── models.py                 # Models: Dividend, DeclaredDividend
│   ├── views.py                  # CBVs de CRUD
│   ├── forms.py                  # DividendForm
│   ├── urls.py                   # URLs do app
│   └── templates/                # Templates do app
│
├── categories/                   # App de Categorias
│   ├── models.py                 # Model: Category
│   └── admin.py                  # Registro no admin
│
├── portifolio/                   # App de Portfolio (reservado)
│   └── models.py                 # Vazio
│
├── services/                     # Servicos externos
│   ├── fees_br.py                # Consulta taxas (IPCA, SELIC, CDI)
│   └── get_ticker_details.py     # Consulta dados de tickers
│
├── manage.py
├── db.sqlite3                    # Banco de dados SQLite
├── requirements.txt              # Dependencias Python
└── venv/                         # Ambiente virtual
```

## Apps e Responsabilidades

### app (Projeto Principal)
- Configuracoes globais do Django
- URLs raiz e inclusao de URLs dos apps
- Views principais: Dashboard e Negociacoes
- Funcoes de metricas agregadas
- Template base e componentes compartilhados

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
- CRUD com 4 templates (sem details)

### categories
- Categorias de ativos (FII, Acao, Stock, ETF)
- Gerenciado via Admin Django

### services
- Integracao com BrasilAPI (taxas economicas)
- Integracao com BrAPI (dados de tickers)

## Padrao de Views

Todas as apps usam Class-Based Views (CBV) do Django:

```python
# Padrao de nomenclatura
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

## Relacionamentos entre Apps

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
