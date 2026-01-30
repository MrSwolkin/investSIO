# URLs e Views

Documentacao dos endpoints e views do projeto.

## URLs Raiz (app/urls.py)

| Metodo | URL | View | Descricao |
|--------|-----|------|-----------|
| GET | `/` | `home()` | Dashboard principal |
| GET | `/admin/` | Admin Django | Painel administrativo |
| GET | `/negociations/` | `negociations()` | Lista todas transacoes |

---

## Brokers (brokers/urls.py)

| Metodo | URL | View | Name |
|--------|-----|------|------|
| GET | `/brokers/list/` | `BrokerListView` | `broker_list` |
| GET/POST | `/brokers/create/` | `BrokerCreateView` | `broker_create` |
| GET | `/brokers/<id>/details/` | `BrokerDetailsView` | `broker_details` |
| GET/POST | `/brokers/<id>/update/` | `BrokerUpdateView` | `broker_update` |
| GET/POST | `/brokers/<id>/delete/` | `BrokerDeleteView` | `broker_delete` |

**Filtros disponiveis:**
- `?name=<texto>` - Filtra por nome da corretora

---

## Tickers (tickers/urls.py)

| Metodo | URL | View | Name |
|--------|-----|------|------|
| GET | `/tickers/<category>/` | `TickerListView` | `ticker_list` |
| GET/POST | `/tickers/<category>/create` | `TickerCreateView` | `ticker_create` |
| GET | `/tickers/<category>/<id>/details` | `TickerDetailsView` | `ticker_details` |
| GET/POST | `/tickers/<category>/<id>/update` | `TickerUpdateView` | `ticker_update` |
| GET/POST | `/tickers/<category>/<id>/delete` | `TickerDeleteView` | `ticker_delete` |

**Parametro de rota:**
- `<category>` - Categoria do ativo (FII, Acao, Stock, ETF)

**Exemplos:**
```
/tickers/FII/
/tickers/Acao/
/tickers/Stock/
/tickers/ETF/
```

---

## Inflows (inflows/urls.py)

| Metodo | URL | View | Name |
|--------|-----|------|------|
| GET | `/inflows/list/` | `InflowListView` | `inflow_list` |
| GET/POST | `/inflows/create/` | `InflowCreateView` | `inflow_create` |
| GET | `/inflows/<id>/details/` | `InflowDetailsView` | `inflow_details` |
| GET/POST | `/inflows/<id>/update/` | `InflowUpdateView` | `inflow_update` |
| GET/POST | `/inflows/<id>/delete/` | `InflowDeleteView` | `inflow_delete` |

---

## Outflows (outflows/urls.py)

| Metodo | URL | View | Name |
|--------|-----|------|------|
| GET | `/outflow/list/` | `OutflowListView` | `outflow_list` |
| GET/POST | `/outflow/create/` | `OutflowCreateView` | `outflow_create` |
| GET | `/outflow/<id>/details/` | `OutflowDetailsView` | `outflow_details` |
| GET/POST | `/outflow/<id>/update/` | `OutflowUpdateView` | `outflow_update` |
| GET/POST | `/outflow/<id>/delete/` | `OutflowDeleteView` | `outflow_delete` |

**Nota:** O prefixo e `/outflow/` (sem 's'), diferente de `/inflows/`.

---

## Dividends (dividends/urls.py)

| Metodo | URL | View | Name |
|--------|-----|------|------|
| GET | `/dividends/list/` | `DividendListView` | `dividend_list` |
| GET/POST | `/dividends/create/` | `DividendCreateView` | `dividend_create` |
| GET/POST | `/dividends/<id>/update/` | `DividendUpdateView` | `dividend_update` |
| GET/POST | `/dividends/<id>/delete/` | `DividendDeleteView` | `dividend_delete` |

**Filtros disponiveis:**
- `?ticker=<id>` - Filtra por ticker
- `?month=<1-12>` - Filtra por mes
- `?year=<ano>` - Filtra por ano
- `?currency=<BRL|USD>` - Filtra por moeda

---

## Views Detalhadas

### home() - Dashboard

Renderiza o dashboard principal com:
- Totais investidos por moeda (BRL, USD, EUR)
- Indicadores economicos (IPCA, SELIC, CDI)
- Grafico de investimentos mensais
- Grafico de dividendos por categoria
- Graficos de diversificacao (categoria, moeda, corretora)

### negociations() - Transacoes

Lista todas as transacoes (inflows + outflows) consolidadas, ordenadas por data decrescente.

### TickerDetailsView

Exibe detalhes completos do ticker:
- Informacoes basicas do ticker
- Dados em tempo real da API (preco, icone, nome)
- Lista de compras (inflows)
- Lista de vendas (outflows)
- Transacoes consolidadas
- Metricas: total investido, quantidade, preco medio

---

## Padrao de Class-Based Views

Todas as views seguem o padrao do Django:

```python
class ModelListView(ListView):
    model = Model
    template_name = "model_list.html"
    context_object_name = "models"

class ModelCreateView(CreateView):
    model = Model
    form_class = ModelForm
    template_name = "model_create.html"
    success_url = reverse_lazy("model_list")

class ModelDetailsView(DetailView):
    model = Model
    template_name = "model_details.html"
    context_object_name = "model"

class ModelUpdateView(UpdateView):
    model = Model
    form_class = ModelForm
    template_name = "model_update.html"
    success_url = reverse_lazy("model_list")

class ModelDeleteView(DeleteView):
    model = Model
    template_name = "model_delete.html"
    success_url = reverse_lazy("model_list")
```
